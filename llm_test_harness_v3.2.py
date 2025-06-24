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
ROUND_NUMBER = 48 # Incremented round number

# Geometric Constants
HEADER_Y_THRESHOLD = 480 

# Page number box constants (normalized) based on user's measurements
# Box: 2cm wide, 1cm high. Top-left corner: 9.5cm from left, 26.8cm from top.
# A4 Page: 21.0cm x 29.7cm
PAGE_NUM_X_START = 9.5 / 21.0   # ~0.452
PAGE_NUM_X_END = (9.5 + 2) / 21.0 # ~0.547
PAGE_NUM_Y_START = 26.8 / 29.7  # ~0.902
PAGE_NUM_Y_END = (26.8 + 1) / 29.7 # ~0.936


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

def get_structured_and_cleaned_gt(file_path):
    """
    NEW: Extracts structured text (with speakers) and page numbers from the
    Document AI JSON, applying geometric filtering.
    Returns a list of strings, including page separators.
    """
    print(f"מעבד אמת מוחלטת עשירה מהקובץ: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        full_text_content = data.get('text', '')
        output_lines = []

        for i, page in enumerate(data.get('pages', [])):
            page_height = page.get('dimension', {}).get('height', 1) 
            page_width = page.get('dimension', {}).get('width', 1)
            
            page_body_paragraphs = []
            page_number_text = f"Page {i+1} (GT)" # Default page number

            for paragraph in page.get('paragraphs', []):
                vertices = paragraph.get('layout', {}).get('boundingPoly', {}).get('normalizedVertices', [])
                if not vertices: continue
                
                y_coords = [v.get('y', 0) for v in vertices]
                x_coords = [v.get('x', 0) for v in vertices]
                avg_y = sum(y_coords) / len(y_coords) if y_coords else 0
                avg_x = sum(x_coords) / len(x_coords) if x_coords else 0
                pixel_y = avg_y * page_height

                paragraph_text = ""
                text_anchor = paragraph.get('layout', {}).get('textAnchor', {})
                for segment in text_anchor.get('textSegments', []):
                    start = int(segment.get('startIndex', 0))
                    end = int(segment.get('endIndex', 0))
                    paragraph_text += full_text_content[start:end]
                
                # Check for page number within the geometric box
                if (PAGE_NUM_Y_START <= avg_y <= PAGE_NUM_Y_END and
                    PAGE_NUM_X_START <= avg_x <= PAGE_NUM_X_END):
                    page_number_text = paragraph_text.strip()
                    continue # Don't add page number to body

                if pixel_y > HEADER_Y_THRESHOLD:
                    page_body_paragraphs.append(paragraph_text)

            # Process the collected body paragraphs for the current page
            for para_text in page_body_paragraphs:
                cleaned_para = re.sub(r'^\s*\d+\s*', '', para_text).strip()
                if cleaned_para:
                    # Simple heuristic for speaker detection
                    speaker_match = re.match(r'^\s*([^:\n]+:\s*)', cleaned_para)
                    if speaker_match:
                        # If a speaker is found, keep the line as is
                        output_lines.append(cleaned_para)
                    else:
                        # If no speaker, split by newlines to respect paragraph breaks
                        output_lines.extend([line for line in cleaned_para.split('\n') if line.strip()])

            output_lines.append(f"--- סוף עמוד {page_number_text} ---")

        return output_lines

    except Exception as e:
        print(f"שגיאה קריטית בעיבוד קובץ האמת המוחלטת העשיר {file_path}: {e}")
        return []

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

def parse_model_output_structured(raw_output):
    """
    NEW: Parses the model's multi-page JSON and creates a structured
    list of lines with page separators.
    """
    cleaned_output = re.sub(r'```json\s*|\s*```', '', raw_output).strip()
    output_lines = []
    try:
        data = json.loads(cleaned_output)
        pages = data.get("document_content", {}).get("pages", [])
        
        for page in pages:
            page_num = page.get("page_number", "N/A")
            body_text = page.get("body_text", "")
            
            # Add the body text, splitting by newlines to respect paragraphs
            output_lines.extend([line for line in body_text.split('\n') if line.strip()])
            
            # Add the page separator
            output_lines.append(f"--- סוף עמוד {page_num} ---")
            
        return output_lines
        
    except json.JSONDecodeError as e:
        print(f"שגיאה בפענוח פלט ה-JSON של המודל: {e}")
        return [f"JSON_PARSE_ERROR: {raw_output}"]
    except Exception as e:
        print(f"שגיאה לא צפויה בפענוח פלט המודל: {e}")
        return [f"PARSE_ERROR: {raw_output}"]

def create_diff_report(gt_lines, model_lines, file_path):
    """Generates and saves an HTML diff report from lists of strings."""
    diff = difflib.HtmlDiff(wrapcolumn=80).make_file(
        fromlines=gt_lines, tolines=model_lines,
        fromdesc='אמת מוחלטת (מובנה)', todesc='פלט המודל (מובנה)'
    )
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(diff)
    print(f"דוח השוואה נוצר בנתיב: {file_path}")

def main():
    print(f"--- מתחיל הרצה של רתמת בדיקות v3.2, סבב מספר {ROUND_NUMBER} ---")
    
    gt_path = os.path.join(GROUND_TRUTH_JSON_DIR, f"full_ground_truth_protocol-{CHUNK_INDEX_TO_TEST}.json")
    ground_truth_lines = get_structured_and_cleaned_gt(gt_path)
    if not ground_truth_lines:
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
    
    model_lines = parse_model_output_structured(model_raw_output)
    
    report_path = os.path.join(REPORTS_DIR, f"{base_filename}_text_diff_report.html")
    create_diff_report(ground_truth_lines, model_lines, report_path)
    
    print(f"--- הרצה מספר {ROUND_NUMBER} הסתיימה. הדוח נמצא ב: {report_path} ---")

if __name__ == "__main__":
    main()