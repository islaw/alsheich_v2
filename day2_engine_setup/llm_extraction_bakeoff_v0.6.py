import os
import json
import time
from datetime import datetime
import csv
import sys
import difflib

# --- תלות חדשה (כלולה בפייתון) ---
# difflib משמש להשוואה מתקדמת בין טקסטים

# --- ייבוא חבילות חיצוניות ---
try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: python-dotenv is not installed. Please run 'pip install python-dotenv'")
    sys.exit(1)
try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF is not installed. Please run 'pip install PyMuPDF'")
    sys.exit(1)
try:
    from PIL import Image
except ImportError:
    print("Error: Pillow is not installed. Please run 'pip install Pillow'")
    sys.exit(1)
try:
    import google.generativeai as genai
except ImportError:
    print("Error: 'google-generativeai' is not installed. Please run 'pip install google-generativeai'")
    sys.exit(1)

load_dotenv()

# --- הגדרות ---
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
INPUT_PDF_FILE = 'protocol_sample_5_pages.pdf'
GROUND_TRUTH_FILE = 'ground_truth.json' # קובץ האמת להשוואה
OUTPUT_DIR_BASE = 'test_results'
IMAGE_DPI = 300

MODELS_TO_TEST = [
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro-latest",
    "gemini-2.0-flash",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite-preview-06-17"
]

PROMPT_TEXT = """
You are an expert Israeli legal-tech AI assistant. Your task is to accurately transcribe and structure the content of an image of a court protocol page into a structured JSON format.
( ... תוכן הפרומפט המלא כפי שהוגדר קודם ... )
"""

# --- פונקציות עזר קיימות (ללא שינוי) ---
def pdf_to_pil_images(pdf_path: str, dpi: int) -> list:
    # ... (הקוד נשאר זהה) ...
    if not os.path.exists(pdf_path):
        print(f"Error: Input file '{pdf_path}' not found.")
        return []
    
    images = []
    print(f"Converting '{pdf_path}' to images...")
    try:
        doc = fitz.open(pdf_path)
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=dpi)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append({"page_num": i + 1, "image_data": img, "page_obj": page})
            print(f"  - Page {i+1} converted.")
        doc.close()
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
    return images

def clean_json_response(raw_text: str) -> tuple[dict, bool]:
    # ... (הקוד נשאר זהה) ...
    if not raw_text or not raw_text.strip():
        return {"error": "Empty response from model"}, False

    json_str = raw_text.strip()
    if json_str.startswith("```json"):
        json_str = json_str[7:]
    if json_str.endswith("```"):
        json_str = json_str[:-3]
    
    try:
        parsed_json = json.loads(json_str)
        return parsed_json, True
    except json.JSONDecodeError as e:
        error_info = {"error": f"JSON parsing failed: {e}", "raw_response": raw_text}
        return error_info, False

# --- לוגיקת השוואת QA חדשה ---
def compare_outputs(ground_truth_page: dict, model_output_page: dict) -> dict:
    """
    Compares a model's output JSON for a single page against the ground truth.
    Returns a dictionary with a summary of discrepancies and an accuracy score.
    """
    discrepancies = []
    total_items = 0
    mismatched_items = 0

    # 1. Compare Metadata
    total_items += 1
    gt_page_num = ground_truth_page.get("page_metadata", {}).get("visual_page_number")
    model_page_num = model_output_page.get("page_metadata", {}).get("visual_page_number")
    if gt_page_num != model_page_num:
        mismatched_items += 1
        discrepancies.append(f"PageNumber Mismatch: Expected '{gt_page_num}', Got '{model_page_num}'")

    # 2. Compare Header (simplified check)
    total_items += 1
    if ground_truth_page.get("header_content") != model_output_page.get("header_content"):
         mismatched_items += 1
         discrepancies.append("Header Content Mismatch")

    # 3. Compare Protocol Body
    gt_body = ground_truth_page.get("protocol_body", [])
    model_body = model_output_page.get("protocol_body", [])
    
    gt_dict = {item['line_number']: item for item in gt_body}
    model_dict = {item['line_number']: item for item in model_body}

    all_line_numbers = sorted(list(set(gt_dict.keys()) | set(model_dict.keys())), key=lambda x: int(x) if x and x.isdigit() else float('inf'))

    for line_num in all_line_numbers:
        total_items += 1
        gt_item = gt_dict.get(line_num)
        model_item = model_dict.get(line_num)

        if not gt_item:
            mismatched_items += 1
            discrepancies.append(f"Line {line_num}: Extra line found in model output.")
            continue
        if not model_item:
            mismatched_items += 1
            discrepancies.append(f"Line {line_num}: Line missing from model output.")
            continue
        
        error_in_line = False
        if gt_item.get('speaker') != model_item.get('speaker'):
            error_in_line = True
            discrepancies.append(f"Line {line_num} Speaker Mismatch: Expected '{gt_item.get('speaker')}', Got '{model_item.get('speaker')}'")
        
        if gt_item.get('text').strip() != model_item.get('text').strip():
            error_in_line = True
            diff = difflib.unified_diff(
                gt_item.get('text').strip().splitlines(), 
                model_item.get('text').strip().splitlines(), 
                fromfile='expected', tofile='got', lineterm=''
            )
            discrepancies.append(f"Line {line_num} Text Mismatch: {' | '.join(list(diff))}")

        if error_in_line:
            mismatched_items += 1

    accuracy = ((total_items - mismatched_items) / total_items) * 100 if total_items > 0 else 100

    return {
        "accuracy_score": round(accuracy, 2),
        "discrepancy_count": mismatched_items,
        "discrepancies": " | ".join(discrepancies) if discrepancies else "None"
    }

# --- פונקציה ראשית משודרגת ---
def main():
    if not GOOGLE_API_KEY:
        print("CRITICAL: GOOGLE_API_KEY not set.")
        return
        
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # --- טעינת קובץ האמת ---
    try:
        with open(GROUND_TRUTH_FILE, 'r', encoding='utf-8') as f:
            ground_truth_data_list = json.load(f)
        # המרת רשימה למילון לגישה מהירה לפי מספר עמוד
        ground_truth_data = {
            item.get("page_metadata", {}).get("visual_page_number"): item
            for item in ground_truth_data_list
        }
        print(f"Successfully loaded ground truth file: {GROUND_TRUTH_FILE}")
    except FileNotFoundError:
        print(f"CRITICAL: Ground truth file '{GROUND_TRUTH_FILE}' not found. QA will be skipped.")
        ground_truth_data = None
    except (json.JSONDecodeError, KeyError) as e:
        print(f"CRITICAL: Error parsing ground truth file: {e}. QA will be skipped.")
        ground_truth_data = None

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    run_dir = os.path.join(OUTPUT_DIR_BASE, f"run_{timestamp}")
    os.makedirs(run_dir, exist_ok=True)
    print(f"Results will be saved in: {run_dir}")

    images = pdf_to_pil_images(INPUT_PDF_FILE, IMAGE_DPI)
    if not images:
        print("Could not generate images from PDF. Aborting.")
        return

    csv_file_path = os.path.join(run_dir, "summary_results.csv")
    # --- הוספת עמודות QA לקובץ הסיכום ---
    csv_headers = [
        "Model_Name", "Page_Number", "Status", "Processing_Duration_s",
        "Accuracy_Score", "Discrepancy_Count", "Discrepancies_Details",
        "Input_Tokens", "Output_Tokens", "Total_Tokens", "Error_Details"
    ]

    all_results = []

    for model_name in MODELS_TO_TEST:
        print(f"\n{'='*50}\n--- Testing Model: {model_name} ---\n{'='*50}")

        safe_model_name = model_name.replace("/", "_")
        model_output_dir = os.path.join(run_dir, safe_model_name)
        os.makedirs(model_output_dir, exist_ok=True)

        try:
            model = genai.GenerativeModel(model_name)
        except Exception as e:
            print(f"--> FAILED TO INITIALIZE MODEL: {model_name}. Error: {e}")
            for image_data in images:
                all_results.append({
                    "Model_Name": model_name, "Page_Number": image_data['page_num'], "Status": "Model Init Failed",
                    "Error_Details": str(e)
                })
            continue

        for image_data in images:
            page_num_physical = image_data['page_num']
            print(f"  > Analyzing page {page_num_physical}...")
            
            start_time = time.time()
            
            row_data = {
                "Model_Name": model_name, "Page_Number": page_num_physical, "Status": "Unknown Error",
                "Accuracy_Score": "N/A", "Discrepancy_Count": "N/A", "Discrepancies_Details": "N/A"
            }

            try:
                generation_config = genai.types.GenerationConfig(temperature=0.0)
                response = model.generate_content([PROMPT_TEXT, image_data['image_data']], generation_config=generation_config)
                duration = time.time() - start_time
                row_data["Processing_Duration_s"] = round(duration, 2)

                raw_response_text = getattr(response, 'text', None)
                if raw_response_text is None:
                    row_data["Status"] = "Failed - Blocked"
                    row_data["Error_Details"] = f"Response blocked, reason: {response.prompt_feedback}"
                    all_results.append(row_data)
                    print(f"    - Page {page_num_physical} processing BLOCKED.")
                    continue

                structured_data, is_valid = clean_json_response(raw_response_text)
                output_filepath = os.path.join(model_output_dir, f"{safe_model_name}_page_{page_num_physical}_output.json")
                
                if not is_valid:
                    row_data["Status"] = "Failed - JSON Parse Error"
                    row_data["Error_Details"] = structured_data.get('error', 'Unknown')
                    with open(output_filepath.replace(".json", "_error.txt"), 'w', encoding='utf-8') as f:
                        f.write(raw_response_text)
                    print(f"    - Page {page_num_physical} failed JSON parsing.")
                else:
                    row_data["Status"] = "Success"
                    json_string_for_file = json.dumps(structured_data, ensure_ascii=False, indent=2)
                    with open(output_filepath, 'w', encoding='utf-8') as f:
                        f.write(json_string_for_file)
                    print(f"    - Page {page_num_physical} processed successfully.")

                    # --- ביצוע השוואת QA ---
                    if ground_truth_data:
                        page_key = structured_data.get("page_metadata", {}).get("visual_page_number")
                        if page_key and page_key in ground_truth_data:
                            gt_page = ground_truth_data[page_key]
                            qa_results = compare_outputs(gt_page, structured_data)
                            row_data.update({
                                "Accuracy_Score": qa_results["accuracy_score"],
                                "Discrepancy_Count": qa_results["discrepancy_count"],
                                "Discrepancies_Details": qa_results["discrepancies"]
                            })
                            print(f"    - QA Results: Score={qa_results['accuracy_score']}%, Discrepancies={qa_results['discrepancy_count']}")
                        else:
                             row_data.update({"Discrepancies_Details": f"No ground truth found for page key '{page_key}'"})
                             print(f"    - QA Warning: No ground truth found for page key '{page_key}'")

                usage = getattr(response, 'usage_metadata', None)
                if usage:
                    row_data.update({
                        "Input_Tokens": usage.prompt_token_count,
                        "Output_Tokens": usage.candidates_token_count,
                        "Total_Tokens": usage.total_token_count
                    })
                all_results.append(row_data)

            except Exception as e:
                error_message = f"API Call Error: {type(e).__name__}: {e}"
                print(f"    - CRITICAL ERROR on page {page_num_physical}: {error_message}")
                row_data.update({"Status": "Failed - API Error", "Error_Details": error_message})
                all_results.append(row_data)

    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_headers, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(all_results)
        print(f"\n--- All operations completed. Results summary saved to '{csv_file_path}' ---")
    except IOError as e:
        print(f"Error writing to CSV file: {e}")

if __name__ == "__main__":
    main()