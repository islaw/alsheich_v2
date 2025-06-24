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
PROMPT_FILE_PATH = 'prompts/main_extraction_prompt_v4.1.txt'
RESULTS_DIR = 'truth_test/test_harness_results'
JSON_OUTPUTS_DIR = os.path.join(RESULTS_DIR, 'json_outputs')
REPORTS_DIR = os.path.join(RESULTS_DIR, 'reports')

MODEL_NAME = "gemini-2.5-pro"
CHUNK_INDEX_TO_TEST = 0
PAGES_PER_CHUNK = 5
ROUND_NUMBER = 41 # Incremented round number for the new geometric logic

# Geometric Constants
A4_HEIGHT_CM = 29.7
HEADER_THRESHOLD_CM = 6.3
NORMALIZED_HEADER_THRESHOLD = HEADER_THRESHOLD_CM / A4_HEIGHT_CM # Approximately 0.212

# --- Setup Directories ---
os.makedirs(JSON_OUTPUTS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

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

def get_clean_body_text_from_gt(file_path):
    """
    Extracts and cleans the body text from the raw Document AI JSON file
    using a strict geometric rule.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        all_text_elements = []
        # The structure is data -> pages -> blocks -> paragraphs -> words -> symbols
        # We can simplify by just getting all text anchors and their bounds.
        for page in data.get('pages', []):
            for block in page.get('blocks', []):
                for paragraph in block.get('paragraphs', []):
                    for word in paragraph.get('words', []):
                        # Reconstruct word from symbols
                        word_text = ''.join([s.get('text', '') for s in word.get('symbols', [])])
                        
                        # Get bounding box for the word
                        vertices = word.get('layout', {}).get('boundingPoly', {}).get('normalizedVertices', [])
                        if vertices:
                            # Get the Y coordinate of the top-left vertex
                            top_y = vertices[0].get('y', 0)
                            all_text_elements.append({'y': top_y, 'text': word_text})

        # Filter out elements that are in the header zone
        body_elements = [elem for elem in all_text_elements if elem['y'] >= NORMALIZED_HEADER_THRESHOLD]

        # Reconstruct the text. This is a simplified approach. A more advanced one would handle line breaks.
        # For now, we join with spaces.
        full_body_text = " ".join([elem['text'] for elem in body_elements])
        
        # Apply final cleaning rules (remove line numbers, etc.) as a post-processing step
        # This part is less critical now as we are selecting geometrically, but good for cleanup.
        lines = full_body_text.split('\n')
        processed_lines = []
        for line in lines:
            cleaned_line = re.sub(r'^\s*\d+\s*', '', line)
            if re.fullmatch(r'\s*\d+\s*', cleaned_line):
                continue
            if cleaned_line.strip():
                processed_lines.append(cleaned_line.strip())

        return "\n".join(processed_lines)

    except Exception as e:
        print(f"שגיאה בעיבוד גיאומטרי של קובץ האמת המוחלטת {file_path}: {e}")
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

def parse_model_output(raw_output):
    """
    Parses the model's raw multi-page JSON output and combines
    the body_text from all pages into a single string.
    """
    cleaned_output = re.sub(r'```json\s*|\s*```', '', raw_output).strip()
    try:
        data = json.loads(cleaned_output)
        pages = data.get("document_content", {}).get("pages", [])
        
        all_body_texts = []
        for page in pages:
            all_body_texts.append(page.get("body_text", ""))
            
        return "\n".join(all_body_texts)
        
    except json.JSONDecodeError as e:
        print(f"שגיאה בפענוח פלט ה-JSON של המודל: {e}")
        print("--- פלט גולמי מהמודל ---")
        print(raw_output)
        print("------------------------")
        return f"JSON_PARSE_ERROR: {raw_output}"

def create_diff_report(gt_text, model_text, file_path):
    """Generates and saves an HTML diff report between two text blocks."""
    diff = difflib.HtmlDiff(wrapcolumn=80).make_file(
        fromlines=gt_text.splitlines(), tolines=model_text.splitlines(),
        fromdesc='אמת מוחלטת (טקסט נקי גיאומטרית)', todesc='פלט המודל (טקסט נקי)'
    )
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(diff)
    print(f"דוח השוואה נוצר בנתיב: {file_path}")

def main():
    print(f"--- מתחיל הרצה של רתמת בדיקות v2.5, סבב מספר {ROUND_NUMBER} ---")
    
    # 1. Load and Clean Ground Truth using geometric rules
    gt_file_index = CHUNK_INDEX_TO_TEST
    gt_path = os.path.join(GROUND_TRUTH_JSON_DIR, f"full_ground_truth_protocol-{gt_file_index}.json")
    if not os.path.exists(gt_path):
         print(f"שגיאה: קובץ האמת המוחלטת לא נמצא בנתיב {gt_path}. עוצר.")
         return

    print(f"טוען ומנקה את קובץ האמת המוחלטת {gt_path} באמצעות כלל גיאומטרי...")
    ground_truth_text = get_clean_body_text_from_gt(gt_path)
    if not ground_truth_text:
        print("לא ניתן היה לקבל טקסט נקי מהאמת המוחלטת לאחר סינון גיאומטרי. עוצר.")
        return

    # 2. Load Prompt
    try:
        with open(PROMPT_FILE_PATH, 'r', encoding='utf-8') as f:
            prompt = f.read()
    except FileNotFoundError:
        print(f"קובץ הפרומפט לא נמצא בנתיב {PROMPT_FILE_PATH}. עוצר.")
        return

    # 3. Load Images
    images = load_images_for_chunk(CHUNK_INDEX_TO_TEST, PAGES_PER_CHUNK)
    if not images:
        return

    # 4. Get Model Response
    model_raw_output = get_model_response(prompt, images)
    
    # 5. Save Raw Output & Parse
    prompt_name = os.path.splitext(os.path.basename(PROMPT_FILE_PATH))[0]
    base_filename = f"round{ROUND_NUMBER}_chunk{CHUNK_INDEX_TO_TEST}_model_{MODEL_NAME}_prompt_{prompt_name}"
    
    json_output_path = os.path.join(JSON_OUTPUTS_DIR, f"{base_filename}.json")
    with open(json_output_path, 'w', encoding='utf-8') as f:
        f.write(model_raw_output)
    print(f"הפלט הגולמי של המודל נשמר ב: {json_output_path}")
    
    model_text = parse_model_output(model_raw_output)
    
    # 6. Generate Diff Report
    report_path = os.path.join(REPORTS_DIR, f"{base_filename}_text_diff_report.html")
    create_diff_report(ground_truth_text, model_text, report_path)
    
    print(f"--- הרצה מספר {ROUND_NUMBER} הסתיימה. הדוח נמצא ב: {report_path} ---")

if __name__ == "__main__":
    main()