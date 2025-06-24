import os
import json
import base64
import google.generativeai as genai
import difflib
import re

# --- Configuration ---
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")
genai.configure(api_key=API_KEY)

# --- Constants ---
IMAGE_INPUT_DIR = 'protocol_images'
GROUND_TRUTH_JSON_DIR = 'downloaded_json_parts'
PROMPT_FILE_PATH = 'prompts/main_extraction_prompt_v4.2.txt'
ERROR_TRAPS_PATH = 'error_traps_v1.1.json'
RESULTS_DIR = 'truth_test/test_harness_results'
JSON_OUTPUTS_DIR = os.path.join(RESULTS_DIR, 'json_outputs')
REPORTS_DIR = os.path.join(RESULTS_DIR, 'reports')

MODEL_NAME = "gemini-2.5-pro"
CHUNK_INDEX_TO_TEST = 0
PAGES_PER_CHUNK = 5
ROUND_NUMBER = 51 # Incremented round number

# Geometric Constants
HEADER_Y_THRESHOLD = 480

# --- Setup Directories ---
os.makedirs(JSON_OUTPUTS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

def load_error_traps(file_path):
    """Loads the error correction map from the JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"מלכודות שגיאה נטענו בהצלחה מגרסה: {data.get('version', 'N/A')}")
            return data.get('correction_map', {})
    except FileNotFoundError:
        print(f"אזהרה: קובץ מלכודות שגיאה לא נמצא בנתיב {file_path}. ממשיך ללא תיקונים.")
        return {}
    except json.JSONDecodeError:
        print(f"אזהרה: קובץ מלכודות שגיאה בנתיב {file_path} אינו תקין. ממשיך ללא תיקונים.")
        return {}

def apply_error_traps(text, correction_map):
    """Applies the corrections from the error traps map to the text."""
    if not correction_map:
        return text
    
    corrected_text = text
    for correct_value, errors in correction_map.items():
        for error in errors:
            corrected_text = re.sub(r'\b' + re.escape(error) + r'\b', correct_value, corrected_text)
    return corrected_text

def load_images_for_chunk(chunk_index, pages_per_chunk):
    """Loads and encodes all images for a given chunk index."""
    encoded_images = []
    start_page = (chunk_index * pages_per_chunk) + 1
    end_page = start_page + pages_per_chunk
    
    print(f"טוען תמונות עבור עמודים {start_page} עד {end_page - 1}...")
    
    for page_num in range(start_page, end_page):
        path = os.path.join(IMAGE_INPUT_DIR, f"page_{page_num}.jpg")
        if not os.path.exists(path):
            print(f"שגיאה: התמונה לא נמצאה בנתיב {path}. עוצר.")
            return None
        with open(path, "rb") as image_file:
            encoded_data = base64.b64encode(image_file.read()).decode('utf-8')
            encoded_images.append({"mime_type": "image/jpeg", "data": encoded_data})
    return encoded_images

def get_text_from_gt_json(file_path):
    """
    Extracts the raw body text from the Document AI JSON, applying geometric filtering.
    Returns a single string.
    """
    print(f"מעבד אמת מידה מהקובץ: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        full_text_content = data.get('text', '')
        page_texts = []

        for i, page in enumerate(data.get('pages', [])):
            page_height = page.get('dimension', {}).get('height', 1)
            
            page_body_paragraphs = []
            for paragraph in page.get('paragraphs', []):
                vertices = paragraph.get('layout', {}).get('boundingPoly', {}).get('normalizedVertices', [])
                if not vertices: continue
                
                y_coords = [v.get('y', 0) for v in vertices]
                avg_y = sum(y_coords) / len(y_coords) if y_coords else 0
                pixel_y = avg_y * page_height

                if pixel_y > HEADER_Y_THRESHOLD:
                    paragraph_text = ""
                    text_anchor = paragraph.get('layout', {}).get('textAnchor', {})
                    for segment in text_anchor.get('textSegments', []):
                        start = int(segment.get('startIndex', 0))
                        end = int(segment.get('endIndex', 0))
                        paragraph_text += full_text_content[start:end]
                    
                    cleaned_para = re.sub(r'^\s*\d+\s*', '', paragraph_text).strip()
                    if cleaned_para:
                        page_body_paragraphs.append(cleaned_para)
            
            page_texts.append("\n".join(page_body_paragraphs))
        
        return "\n".join(page_texts)

    except Exception as e:
        print(f"שגיאה קריטית בעיבוד קובץ אמת המידה {file_path}: {e}")
        return ""

def get_model_response(prompt, images):
    """Sends the request to the Generative AI model."""
    generation_config = {"temperature": 0.0, "response_mime_type": "application/json"}
    model = genai.GenerativeModel(model_name=MODEL_NAME, generation_config=generation_config)
    content_parts = [prompt] + images
    try:
        print(f"שולח בקשה אל {MODEL_NAME}...")
        response = model.generate_content(content_parts)
        return response.text
    except Exception as e:
        print(f"אירעה שגיאה במהלך קריאת ה-API: {e}")
        return f'{{"error": "API call failed: {str(e)}"}}'

def get_text_from_model_output(raw_output):
    """
    Parses the model's multi-page JSON and returns a single string of the combined body text.
    """
    cleaned_output = re.sub(r'```json\s*|\s*```', '', raw_output).strip()
    page_texts = []
    try:
        data = json.loads(cleaned_output)
        pages = data.get("document_content", {}).get("pages", [])
        
        for page in pages:
            body_text = page.get("body_text", "")
            if body_text:
                page_texts.append(body_text)
            
        return "\n".join(page_texts)
        
    except json.JSONDecodeError as e:
        print(f"שגיאה בפענוח פלט הג'ייסון של המודל: {e}")
        return f"JSON_PARSE_ERROR: {raw_output}"
    except Exception as e:
        print(f"שגיאה לא צפויה בפענוח פלט המודל: {e}")
        return f"PARSE_ERROR: {raw_output}"

def word_based_diff_report(gt_text, model_text, report_path):
    """
    Generates a word-based diff report that preserves the original structure
    and highlights only content changes.
    """
    # Normalize for a quick check if texts are identical
    gt_flat_for_check = re.sub(r'\s+', '', gt_text)
    model_flat_for_check = re.sub(r'\s+', '', model_text)
    if gt_flat_for_check == model_flat_for_check:
        print("השוואה לוגית: לא נמצאו הבדלי תוכן. אין צורך בהפקת דוח.")
        return

    print("השוואה לוגית: נמצאו הבדלי תוכן. מתחיל תהליך יישור והפקת דוח...")

    # Split texts into words
    gt_words = re.split(r'(\s+)', gt_text)
    model_words = re.split(r'(\s+)', model_text)

    # Use SequenceMatcher on the word lists
    s = difflib.SequenceMatcher(None, gt_words, model_words)
    
    # Start building the HTML report
    html = [
        '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">',
        '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>Word-based Diff</title>',
        '<style type="text/css">',
        'table.diff {font-family: Menlo, Consolas, Monaco, Liberation Mono, Lucida Console, monospace; border:medium; direction: rtl;}',
        '.diff_header {background-color:#e0e0e0; text-align: center;}',
        'td {padding: 1px 4px; white-space: pre-wrap; vertical-align: top;}',
        '.diff_add {background-color:#aaffaa;}',
        '.diff_chg {background-color:#ffff77;}',
        '.diff_sub {background-color:#ffaaaa;}',
        '</style></head><body><table class="diff" cellspacing="0" cellpadding="0" rules="groups">',
        '<colgroup></colgroup><colgroup></colgroup>',
        '<thead><tr><th colspan="2" class="diff_header">אמת מידה (מתוקן)</th><th colspan="2" class="diff_header">פלט המודל (מתוקן)</th></tr></thead><tbody>'
    ]

    gt_out = ""
    model_out = ""

    for tag, i1, i2, j1, j2 in s.get_opcodes():
        gt_chunk = "".join(gt_words[i1:i2])
        model_chunk = "".join(model_words[j1:j2])

        if tag == 'equal':
            gt_out += gt_chunk
            model_out += model_chunk
        elif tag == 'replace':
            gt_out += f'<span class="diff_sub">{gt_chunk}</span>'
            model_out += f'<span class="diff_add">{model_chunk}</span>'
        elif tag == 'delete':
            gt_out += f'<span class="diff_sub">{gt_chunk}</span>'
        elif tag == 'insert':
            model_out += f'<span class="diff_add">{model_chunk}</span>'

    # Combine into a single row for the table
    html.append(f'<tr><td>{gt_out}</td><td></td><td>{model_out}</td></tr>')
    html.append('</tbody></table></body></html>')

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(html))
    print(f"דוח השוואה מבוסס מילים נוצר בנתיב: {report_path}")


def main():
    print(f"--- מתחיל הרצה של רתמת בדיקות v3.5, סבב מספר {ROUND_NUMBER} ---")
    
    error_correction_map = load_error_traps(ERROR_TRAPS_PATH)

    # --- Ground Truth Processing ---
    gt_path = os.path.join(GROUND_TRUTH_JSON_DIR, f"full_ground_truth_protocol-{CHUNK_INDEX_TO_TEST}.json")
    raw_gt_text = get_text_from_gt_json(gt_path)
    if not raw_gt_text:
        print("לא ניתן היה לקבל טקסט מאמת המידה. עוצר.")
        return
    corrected_gt_text = apply_error_traps(raw_gt_text, error_correction_map)
    print("טקסט אמת המידה עבר תיקון באמצעות מלכודות השגיאה.")

    # --- Model Processing ---
    try:
        with open(PROMPT_FILE_PATH, 'r', encoding='utf-8') as f:
            prompt = f.read()
    except FileNotFoundError:
        print(f"קובץ הפרומפט לא נמצא בנתיב {PROMPT_FILE_PATH}. עוצר.")
        return

    images = load_images_for_chunk(CHUNK_INDEX_TO_TEST, PAGES_PER_CHUNK)
    if not images:
        return

    model_raw_output = get_model_response(prompt, images)
    
    prompt_name = os.path.splitext(os.path.basename(PROMPT_FILE_PATH))[0]
    base_filename = f"round{ROUND_NUMBER}_chunk{CHUNK_INDEX_TO_TEST}_model_{MODEL_NAME}_prompt_{prompt_name}"
    
    json_output_path = os.path.join(JSON_OUTPUTS_DIR, f"{base_filename}.json")
    with open(json_output_path, 'w', encoding='utf-8') as f:
        f.write(model_raw_output)
    print(f"הפלט הגולמי של המודל נשמר ב: {json_output_path}")
    
    raw_model_text = get_text_from_model_output(model_raw_output)
    corrected_model_text = apply_error_traps(raw_model_text, error_correction_map)
    print("פלט המודל עבר תיקון באמצעות מלכודות השגיאה.")
    
    # --- Comparison ---
    report_path = os.path.join(REPORTS_DIR, f"{base_filename}_word_based_diff.html")
    word_based_diff_report(corrected_gt_text, corrected_model_text, report_path)
    
    print(f"--- הרצה מספר {ROUND_NUMBER} הסתיימה. ---")

if __name__ == "__main__":
    main()