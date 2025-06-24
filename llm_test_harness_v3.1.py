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
ROUND_NUMBER = 47 # Incremented round number

# Geometric constant: Final calibrated value based on diagnostic run.
# Last header element is at ~403px. First body element is at ~550px.
# 480 is a safe, data-driven threshold.
HEADER_Y_THRESHOLD = 480

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

def get_clean_body_text_from_rich_gt(file_path):
    """
    Extracts and cleans the body text from the RICH Document AI JSON file
    using the final, calibrated geometric threshold.
    """
    print(f"מעבד אמת מוחלטת עשירה מהקובץ: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        full_text_content = data.get('text', '')
        all_body_text_parts = []

        for page in data.get('pages', []):
            # The actual page height from the JSON is used for calculations.
            page_height = page.get('dimension', {}).get('height', 1) 

            for paragraph in page.get('paragraphs', []):
                vertices = paragraph.get('layout', {}).get('boundingPoly', {}).get('normalizedVertices', [])
                if not vertices: continue
                
                # Calculate pixel_y based on the AVERAGE of the y-coordinates.
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
                    
                    # Clean the extracted text (remove leading numbers etc.)
                    cleaned_paragraph = re.sub(r'^\s*\d+\s*', '', paragraph_text).strip()
                    if cleaned_paragraph:
                        all_body_text_parts.append(cleaned_paragraph)

        return "\n".join(all_body_text_parts)

    except Exception as e:
        print(f"שגיאה קריטית בעיבוד קובץ האמת המוחלטת העשיר {file_path}: {e}")
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
    """Parses the model's multi-page JSON and combines body_text fields."""
    cleaned_output = re.sub(r'```json\s*|\s*```', '', raw_output).strip()
    try:
        data = json.loads(cleaned_output)
        pages = data.get("document_content", {}).get("pages", [])
        all_body_texts = [page.get("body_text", "") for page in pages]
        return "\n".join(all_body_texts)
    except json.JSONDecodeError as e:
        print(f"שגיאה בפענוח פלט ה-JSON של המודל: {e}")
        return f"JSON_PARSE_ERROR: {raw_output}"

def create_diff_report(gt_text, model_text, file_path):
    """Generates and saves an HTML diff report."""
    diff = difflib.HtmlDiff(wrapcolumn=80).make_file(
        fromlines=gt_text.splitlines(), tolines=model_text.splitlines(),
        fromdesc='אמת מוחלטת (סינון גיאומטרי סופי)', todesc='פלט המודל (טקסט נקי)'
    )
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(diff)
    print(f"דוח השוואה נוצר בנתיב: {file_path}")

def main():
    print(f"--- מתחיל הרצה של רתמת בדיקות v3.1, סבב מספר {ROUND_NUMBER} ---")
    
    gt_path = os.path.join(GROUND_TRUTH_JSON_DIR, f"full_ground_truth_protocol-{CHUNK_INDEX_TO_TEST}.json")
    ground_truth_text = get_clean_body_text_from_rich_gt(gt_path)
    if not ground_truth_text:
        print("לא ניתן היה לקבל טקסט נקי מהאמת המוחלטת העשירה. עוצר.")
        return

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
    
    model_text = parse_model_output(model_raw_output)
    
    report_path = os.path.join(REPORTS_DIR, f"{base_filename}_text_diff_report.html")
    create_diff_report(ground_truth_text, model_text, report_path)
    
    print(f"--- הרצה מספר {ROUND_NUMBER} הסתיימה. הדוח נמצא ב: {report_path} ---")

if __name__ == "__main__":
    main()