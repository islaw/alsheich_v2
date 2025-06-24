# main_processor.py (v45.0 - Final, Definitive Version)
# Implements the user's final, precise coordinate-based rule for header removal.

import os
import sqlite3
import logging
import re
from datetime import datetime
from typing import Dict, Tuple, List, Any
import fitz  # PyMuPDF
import requests
from dotenv import load_dotenv
import time
import math

# --- Local module imports ---
from parse_filename import parse_filename
from find_witness_id_by_alias import find_witness_id_by_alias
from get_or_create_session import get_or_create_session, update_session_status
from allocate_global_id_range import allocate_global_id_range
from db_operations import add_document_record, log_api_call

# --- Load Environment Variables & Configurations ---
load_dotenv()
DB_PATH = 'data/alsheich_project.db'
INPUT_DIR = '0_DATA/input_files'
OUTPUT_DIR = '0_DATA/output_files'
LOG_FILE = 'logs/main_processor.log'
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
CHUNK_SIZE_PAGES = 10
TEST_PAGE_LIMIT = 24

# --- V23.0 PROMPT (Minimalist Polishing) ---
V23_0_PROMPT = {
    "system_instruction": { "parts": { "text": """אתה מומחה לליטוש פרוטוקולים משפטיים. אתה מקבל טקסט גולמי שעבר ניקוי טכני.
משימותיך הן אך ורק ליטושים קלים מאוד:
1.  תקן שמות שחוברו יחד, למשל "פרידמןפלדמן" צריך להיות "פרידמן-פלדמן".
2.  תקן פורמט דוברים: הסר רווח לפני נקודתיים (למשל, "עד :" -> "עד:").
**חוקי ברזל - קרא בעיון:**
- **החוק החשוב ביותר: אסור בתכלית האיסור לאחד שורות או לשנות את סדר השורות. הפלט חייב להכיל את אותו מספר שורות כמו הקלט.**
- אסור להוסיף, להסיר, או לשנות סימני פיסוק.
- אסור לשנות את משמעות הדברים.""" } },
    "contents": { "role": "user", "parts": { "text": "לטש את הטקסט הבא תוך שמירה על מבנה השורות המקורי:\n---\n{text_to_clean}\n---" } }
}


# --- Logging Setup ---
os.makedirs('logs', exist_ok=True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(LOG_FILE, 'w', 'utf-8'), logging.StreamHandler()])

def call_gemini_api(text_to_clean: str) -> Dict:
    """Calls the Gemini API with the minimalist prompt."""
    if not text_to_clean.strip():
        return { "cleaned_text": "", "prompt_token_count": 0, "candidates_token_count": 0, "total_token_count": 0, "finish_reason": "NO_INPUT", "cost": 0.0 }
    payload = { "system_instruction": V23_0_PROMPT["system_instruction"], "contents": [{"role": "user", "parts": [{"text": V23_0_PROMPT["contents"]["parts"]["text"].format(text_to_clean=text_to_clean)}]}], "generationConfig": {"temperature": 0.0} }
    headers = {"Content-Type": "application/json"}
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, json=payload, headers=headers, timeout=120)
            response.raise_for_status()
            data = response.json()
            usage = data.get('usageMetadata', {})
            cost = ((usage.get('promptTokenCount', 0) * 0.5) + (usage.get('candidatesTokenCount', 0) * 1.5)) / 1_000_000
            raw_cleaned_text = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
            final_text = raw_cleaned_text.replace("לטשתי את הטקסט הבא תוך שמירה על מבנה השורות המקורי:", "").strip()
            return { "cleaned_text": final_text, "prompt_token_count": usage.get('promptTokenCount', 0), "candidates_token_count": usage.get('candidatesTokenCount', 0), "total_token_count": usage.get('totalTokenCount', 0), "finish_reason": data.get('candidates', [{}])[0].get('finishReason', 'UNKNOWN'), "cost": cost }
        except (requests.exceptions.RequestException, KeyError, IndexError) as e:
            logging.warning(f"API call or parsing failed on attempt {attempt + 1}/{max_retries}. Retrying... Error: {e}")
            time.sleep(2 ** attempt)
    raise ConnectionError(f"Failed to connect to Gemini API after {max_retries} attempts.")

def advanced_parser(page: fitz.Page, page_index: int) -> Tuple[List[Dict[str, Any]], int]:
    """
    Parses a page using a precise, coordinate-based approach for all elements.
    """
    page_rect = page.rect
    # User-defined header boundary: 6.3 cm from the top. 1 cm = 28.3465 points.
    header_y_boundary = 6.3 * 28.3465

    # User-defined footer search box
    x0_cm, y0_cm = 9.5, 27.0
    x1_cm, y1_cm = 11.5, 28.0
    footer_search_rect = fitz.Rect(x0_cm * 28.3465, y0_cm * 28.3465, x1_cm * 28.3465, y1_cm * 28.3465)

    left_margin_limit = page_rect.width * 0.15
    visual_page_num = None

    page_dict = page.get_text("dict", sort=True)

    line_structures = []
    last_line_num = 0
    for block in page_dict.get("blocks", []):
        if block.get("type") == 0: # Is a text block
            # Remove header blocks on pages 2+
            if page_index > 0 and block["bbox"][3] < header_y_boundary:
                continue

            for line in block.get("lines", []):
                line_bbox = fitz.Rect(line["bbox"])

                # Check for page number within the precise user-defined rectangle
                if line_bbox.intersects(footer_search_rect):
                    line_text = "".join([span["text"] for span in line.get("spans", [])])
                    if line_text.strip().isdigit():
                        visual_page_num = int(line_text.strip())
                    continue # Skip this line from content regardless

                spans = line.get("spans", [])
                if not spans: continue

                # Assemble line text and check for line number
                first_span = spans[0]
                line_num = None
                line_text_spans = spans

                if first_span["origin"][0] < left_margin_limit and first_span["text"].strip().isdigit():
                    num = int(first_span["text"].strip())
                    if 1 <= num <= 29:
                        if num == 1 or num == last_line_num + 1:
                            line_num = first_span["text"].strip()
                            last_line_num = num
                            line_text_spans = spans[1:] # Exclude the line number span

                # Re-assemble RTL line correctly by reversing the visual order of spans
                line_text = " ".join(s["text"] for s in reversed(line_text_spans))
                line_structures.append({"ln": line_num, "text": line_text})

    return line_structures, visual_page_num


def process_and_chunk_pdf(doc: fitz.Document, session_id: str, db_conn: sqlite3.Connection) -> Tuple[List[str], List[str], float, int, int]:
    cursor = db_conn.cursor()
    all_cleaned_pages = []
    total_cost, total_input_tokens, total_output_tokens = 0.0, 0, 0

    for page_num_idx, page in enumerate(doc):
        if 'TEST_PAGE_LIMIT' in globals() and page_num_idx >= globals()['TEST_PAGE_LIMIT']:
            logging.warning(f"Stopping at test page limit: {globals()['TEST_PAGE_LIMIT']} pages.")
            break

        logging.info(f"Session {session_id}: Parsing page index {page_num_idx}...")
        original_structures, visual_page_num = advanced_parser(page, page_num_idx)
        page_tag = f"\n\n[עמוד {visual_page_num or f'(לא זוהה - אינדקס {page_num_idx+1})'}]\n\n"
        text_to_clean = "\n".join([item["text"] for item in original_structures if item["text"].strip()])

        if text_to_clean.strip():
            logging.info(f"Session {session_id}: Cleaning page index {page_num_idx} (Visual Page: {visual_page_num or 'N/A'})...")
            api_result = call_gemini_api(text_to_clean)
            log_api_call(cursor, session_id, page_num_idx + 1, api_result)
            cleaned_lines = api_result['cleaned_text'].split('\n')

            final_text_lines = []
            text_only_structures = [s for s in original_structures if s["text"].strip()]

            if len(cleaned_lines) == len(text_only_structures):
                for i, structure in enumerate(text_only_structures):
                    line_num = structure.get("ln")
                    cleaned_line = cleaned_lines[i]
                    if line_num:
                        final_text_lines.append(f"{line_num} {cleaned_line}")
                    else:
                        final_text_lines.append(cleaned_line)
                cleaned_page_text = "\n".join(final_text_lines)
            else:
                logging.error(f"CRITICAL: Line count mismatch on page {page_num_idx+1}. LLM may have violated prompt rules. Reverting to original text for this page.")
                reverted_text = []
                for structure in original_structures:
                    line_num = structure.get("ln")
                    text = structure.get("text")
                    if line_num:
                        reverted_text.append(f"{line_num} {text}")
                    else:
                        reverted_text.append(text)
                cleaned_page_text = "\n".join(reverted_text)

            total_cost += api_result.get('cost', 0.0)
            total_input_tokens += api_result.get('prompt_token_count', 0)
            total_output_tokens += api_result.get('candidates_token_count', 0)
        else:
            cleaned_page_text = ""
            logging.info(f"Session {session_id}: Page index {page_num_idx} is empty after parsing, skipping cleaning.")

        all_cleaned_pages.append(page_tag + cleaned_page_text)

    num_chunks = math.ceil(len(all_cleaned_pages) / CHUNK_SIZE_PAGES)
    chunk_ids = []
    if num_chunks > 0:
        start_id = allocate_global_id_range(cursor, num_chunks)
        chunk_ids = [f"ALS-{(start_id + i):07d}" for i in range(num_chunks)]

    return all_cleaned_pages, chunk_ids, total_cost, total_input_tokens, total_output_tokens

def process_pdf_pipeline(pdf_path: str, db_conn: sqlite3.Connection):
    """Main pipeline for processing a single PDF file."""
    cursor = db_conn.cursor()
    session_id = None
    try:
        filename = os.path.basename(pdf_path)
        logging.info(f"--- Starting pipeline for {filename} (v45) ---")
        file_info = parse_filename(filename)
        witness_id = find_witness_id_by_alias(db_conn, file_info['witness_name'])
        session_id, _ = get_or_create_session(cursor, witness_id, file_info['date'])
        parent_doc_id = f"ALS-{(allocate_global_id_range(cursor, 1)):07d}"
        add_document_record(cursor, parent_doc_id, session_id, 'original_pdf', pdf_path)
        doc = fitz.open(pdf_path)
        output_dir = os.path.join(OUTPUT_DIR, file_info['witness_name'].replace(" ", "_"), file_info['date'])
        os.makedirs(output_dir, exist_ok=True)
        all_pages, chunk_ids, cost, in_tokens, out_tokens = process_and_chunk_pdf(doc, session_id, db_conn)
        for i, chunk_id in enumerate(chunk_ids):
            start_page_index = i * CHUNK_SIZE_PAGES
            end_page_index = start_page_index + CHUNK_SIZE_PAGES
            chunk_content = "".join(all_pages[start_page_index:end_page_index])
            chunk_filename = f"chunk_{chunk_id}.txt"
            chunk_filepath = os.path.join(output_dir, chunk_filename)
            with open(chunk_filepath, 'w', encoding='utf-8') as f:
                f.write(chunk_content.strip())
            logging.info(f"Saved chunk {i+1}/{len(chunk_ids)} to {chunk_filepath}")
            add_document_record(cursor, chunk_id, session_id, 'cleaned_chunk', chunk_filepath, parent_doc_id)
        update_session_status(cursor, session_id, 'completed', cost, len(chunk_ids), in_tokens, out_tokens)
        db_conn.commit()
        logging.info(f"--- Successfully completed pipeline for {filename} (v45) ---")
    except Exception as e:
        logging.error(f"An unexpected error occurred in pipeline for {pdf_path}. Rolling back. Session ID: {session_id}. Error: {e}", exc_info=True)
        if db_conn:
            db_conn.rollback()

if __name__ == "__main__":
    logging.info("Main processor script (v45 Architecture) started.")
    try:
        conn = sqlite3.connect(DB_PATH)
        pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.pdf')]
        for pdf_file in pdf_files:
            pdf_filepath = os.path.join(INPUT_DIR, pdf_file)
            try:
                process_pdf_pipeline(pdf_filepath, conn)
            except Exception as e:
                logging.error(f"FATAL: Pipeline for {pdf_file} failed and was rolled back.")
    except Exception as e:
        logging.critical(f"A critical error stopped the main script execution: {e}", exc_info=True)
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            logging.info("Database connection closed.")