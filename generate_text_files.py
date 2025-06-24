import os
import json
import shutil

# --- הגדרות נתיבים ---

# קלט: קבצי JSON גולמיים
DIRTY_STITCHED_JSON = os.path.join('test_results_doc_ai_batch', 'run_20250620_111716_stitched', 'full_stitched_output.json')
DIRTY_PARTS_DIR = 'downloaded_json_parts'

# קלט: קבצי JSON נקיים
CLEANED_STITCHED_JSON = os.path.join('truth_test', 'CLEANED_full_stitched_output.json')
CLEANED_PARTS_DIR = os.path.join('truth_test', 'cleaned_parts')

# פלט: תיקיות עבור קבצי הטקסט
DIRTY_TEXT_OUTPUT_DIR = 'dirty_text_files'
CLEANED_TEXT_OUTPUT_DIR = os.path.join('truth_test', 'cleaned_text_files')

def extract_text_from_json(json_path: str, txt_path: str):
    """
    Reads a Document AI JSON file, extracts the 'text' field, and saves it to a .txt file.
    """
    if not os.path.exists(json_path):
        print(f"  -> Warning: Input JSON not found at '{json_path}'. Skipping.")
        return

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        text_content = data.get('text', '') # Get text, or empty string if not found

        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        print(f"  -> Created text file: '{txt_path}'")

    except Exception as e:
        print(f"  -> ERROR processing '{json_path}': {e}")


def main():
    """
    Main function to generate all corresponding text files from JSON files.
    """
    print("--- Starting Text File Generation ---")

    # יצירת תיקיות פלט
    os.makedirs(DIRTY_TEXT_OUTPUT_DIR, exist_ok=True)
    os.makedirs(CLEANED_TEXT_OUTPUT_DIR, exist_ok=True)
    print(f"Ensured output directories exist: '{DIRTY_TEXT_OUTPUT_DIR}' and '{CLEANED_TEXT_OUTPUT_DIR}'")

    # 1. יצירת קבצי טקסט "מלוכלכים"
    print("\n[1/2] Generating 'dirty' text files...")
    # קובץ מאוחד
    dirty_stitched_txt_path = os.path.join(DIRTY_TEXT_OUTPUT_DIR, 'DIRTY_full_stitched_text.txt')
    extract_text_from_json(DIRTY_STITCHED_JSON, dirty_stitched_txt_path)
    
    # קבצים מחולקים
    if os.path.exists(DIRTY_PARTS_DIR):
        for filename in sorted(os.listdir(DIRTY_PARTS_DIR)):
            if filename.endswith(".json"):
                json_part_path = os.path.join(DIRTY_PARTS_DIR, filename)
                txt_part_path = os.path.join(DIRTY_TEXT_OUTPUT_DIR, filename.replace('.json', '.txt'))
                extract_text_from_json(json_part_path, txt_part_path)
    else:
        print(f"Warning: Directory with dirty parts not found: '{DIRTY_PARTS_DIR}'")


    # 2. יצירת קבצי טקסט "נקיים"
    print("\n[2/2] Generating 'clean' text files...")
    # קובץ מאוחד
    clean_stitched_txt_path = os.path.join(CLEANED_TEXT_OUTPUT_DIR, 'CLEANED_full_stitched_text.txt')
    extract_text_from_json(CLEANED_STITCHED_JSON, clean_stitched_txt_path)

    # קבצים מחולקים
    if os.path.exists(CLEANED_PARTS_DIR):
        for filename in sorted(os.listdir(CLEANED_PARTS_DIR)):
            if filename.endswith(".json"):
                json_part_path = os.path.join(CLEANED_PARTS_DIR, filename)
                txt_part_path = os.path.join(CLEANED_TEXT_OUTPUT_DIR, filename.replace('.json', '.txt'))
                extract_text_from_json(json_part_path, txt_part_path)
    else:
        print(f"Warning: Directory with cleaned parts not found: '{CLEANED_PARTS_DIR}'")

    print("\n--- Text file generation complete. ---")


if __name__ == "__main__":
    main()