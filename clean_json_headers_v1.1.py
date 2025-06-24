import os
import json
import shutil
import re  # <-- תיקון #1: ייבוא ספריית re

# ודא שהספרייה מותקנת: pip install google-cloud-documentai
try:
    from google.cloud import documentai
except ImportError:
    print("Error: google-cloud-documentai library not found.")
    print("Please run 'pip install google-cloud-documentai'")
    exit()

# --- הגדרות ---
STITCHED_FILE_PATH = os.path.join('test_results_doc_ai_batch', 'run_20250620_111716_stitched', 'full_stitched_output.json')
PARTS_DIR = 'downloaded_json_parts'
CLEANED_OUTPUT_DIR = 'truth_test'

HEADER_THRESHOLD_POINTS = 178.6

def clean_document_headers_by_points(input_path: str, output_path: str):
    """
    Loads a Document AI JSON file, removes header elements based on a fixed point threshold,
    rebuilds the main text field, and saves the cleaned JSON.
    """
    print(f"Processing '{os.path.basename(input_path)}'...")

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            json_string = f.read()

        # <-- תיקון #2: שימוש ב-from_json במקום from_dict
        doc = documentai.Document.from_json(json_string)

        for i, page in enumerate(doc.pages):
            if i > 0: # החל מהעמוד השני
                clean_paragraphs = [p for p in page.paragraphs if max(v.y for v in p.layout.bounding_poly.vertices) > HEADER_THRESHOLD_POINTS]
                clean_lines = [l for l in page.lines if max(v.y for v in l.layout.bounding_poly.vertices) > HEADER_THRESHOLD_POINTS]
                clean_tokens = [t for t in page.tokens if max(v.y for v in t.layout.bounding_poly.vertices) > HEADER_THRESHOLD_POINTS]
                
                page.paragraphs = clean_paragraphs
                page.lines = clean_lines
                page.tokens = clean_tokens
        
        rebuilt_text_segments = []
        for page in doc.pages:
            for token in page.tokens:
                rebuilt_text_segments.append(token.layout.text_anchor.content)
        
        doc.text = "".join(rebuilt_text_segments)

        cleaned_json_string = documentai.Document.to_json(doc)
        cleaned_json_dict = json.loads(cleaned_json_string)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(cleaned_json_dict, f, ensure_ascii=False, indent=2)
        
        print(f"  -> Saved cleaned file to '{output_path}'")

    except Exception as e:
        print(f"  -> ERROR processing file {os.path.basename(input_path)}: {e}")

def main():
    if os.path.exists(CLEANED_OUTPUT_DIR):
        shutil.rmtree(CLEANED_OUTPUT_DIR)
    os.makedirs(CLEANED_OUTPUT_DIR)
    print(f"Created output directory: {CLEANED_OUTPUT_DIR}")

    if os.path.exists(STITCHED_FILE_PATH):
        stitched_output_path = os.path.join(CLEANED_OUTPUT_DIR, "CLEANED_full_stitched_output.json")
        clean_document_headers_by_points(STITCHED_FILE_PATH, stitched_output_path)
    else:
        print(f"Warning: Stitched file not found at '{STITCHED_FILE_PATH}'")

    if os.path.exists(PARTS_DIR):
        parts_output_dir = os.path.join(CLEANED_OUTPUT_DIR, "cleaned_parts")
        os.makedirs(parts_output_dir)
        print(f"\nProcessing individual parts from '{PARTS_DIR}'...")
        
        try:
            filenames = sorted(os.listdir(PARTS_DIR), key=lambda x: int(re.search(r'-(\d+)\.json$', x).group(1)))
            for filename in filenames:
                if filename.endswith(".json"):
                    input_file = os.path.join(PARTS_DIR, filename)
                    output_file = os.path.join(parts_output_dir, f"CLEANED_{filename}")
                    clean_document_headers_by_points(input_file, output_file)
        except (AttributeError, ValueError): # Handle cases where regex fails
             print("  -> Could not sort files numerically, falling back to alphabetical sort.")
             filenames = sorted(os.listdir(PARTS_DIR))
             for filename in filenames:
                if filename.endswith(".json"):
                    input_file = os.path.join(PARTS_DIR, filename)
                    output_file = os.path.join(parts_output_dir, f"CLEANED_{filename}")
                    clean_document_headers_by_points(input_file, output_file)

    else:
        print(f"Warning: Parts directory not found at '{PARTS_DIR}'")
    
    print("\nCleaning process complete.")

if __name__ == "__main__":
    main()