import os
import json

# --- הגדרות ---
CHUNK_INDEX = 1 # שינוי הצ'אנק הנבדק ל-1
DIRTY_JSON_DIR = "downloaded_json_parts/"
CLEAN_JSON_DIR = "truth_test/cleaned_parts/"
# ----------------

def count_lines_in_json(file_path):
    """טוען קובץ JSON וסופר את המספר הכולל של רשומות 'lines'."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        total_lines = 0
        for page in data.get("pages", []):
            total_lines += len(page.get("lines", []))
            
        return total_lines
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")
        return None

def main():
    print("--- Starting Cleaning Effect Diagnosis ---")

    # הרכבת נתיבים מלאים
    dirty_filename = f"full_ground_truth_protocol-{CHUNK_INDEX}.json"
    clean_filename = f"CLEANED_full_ground_truth_protocol-{CHUNK_INDEX}.json"
    
    dirty_filepath = os.path.join(DIRTY_JSON_DIR, dirty_filename)
    clean_filepath = os.path.join(CLEAN_JSON_DIR, clean_filename)

    # ספירת שורות בשני הקבצים
    dirty_line_count = count_lines_in_json(dirty_filepath)
    clean_line_count = count_lines_in_json(clean_filepath)

    if dirty_line_count is not None and clean_line_count is not None:
        print(f"\nAnalysis for Chunk {CHUNK_INDEX}:")
        print(f"  - Lines in DIRTY file ('{dirty_filepath}'): {dirty_line_count}")
        print(f"  - Lines in CLEAN file ('{clean_filepath}'): {clean_line_count}")
        
        difference = dirty_line_count - clean_line_count
        print(f"  - Difference (lines removed by cleaning script): {difference}")
    
    print("\n--- Diagnosis Finished ---")


if __name__ == "__main__":
    main()