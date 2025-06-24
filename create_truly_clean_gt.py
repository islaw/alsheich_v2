import os
import json

# --- הגדרות ---
SOURCE_DIR = "downloaded_json_parts/"
TARGET_DIR = "truth_test/truly_cleaned_parts/"
HEADER_Y_BOUNDARY_PT = 178.6  # 6.3 cm * 28.3465 points/cm
TOTAL_CHUNKS = 12
# ----------------

def main():
    print("--- Starting creation of 'Truly Clean' Ground Truth files ---")
    os.makedirs(TARGET_DIR, exist_ok=True)

    for i in range(TOTAL_CHUNKS):
        source_filename = f"full_ground_truth_protocol-{i}.json"
        target_filename = f"TRULY_CLEANED_full_ground_truth_protocol-{i}.json"
        
        source_path = os.path.join(SOURCE_DIR, source_filename)
        target_path = os.path.join(TARGET_DIR, target_filename)

        print(f"Processing '{source_path}'...")

        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"  - WARNING: Source file not found. Skipping.")
            continue
        except json.JSONDecodeError:
            print(f"  - WARNING: Could not parse source JSON. Skipping.")
            continue

        cleaned_pages = []
        for page in data.get("pages", []):
            page_number = page.get("pageNumber")
            
            # אם זה לא העמוד הראשון, בצע ניקוי
            if page_number != 1:
                original_lines = page.get("lines", [])
                cleaned_lines = [
                    line for line in original_lines 
                    if not (line.get("layout", {}).get("boundingPoly", {}).get("normalizedVertices", [{}, {}, {}, {}])[0].get("y", 1.0) * 842 < HEADER_Y_BOUNDARY_PT)
                ]
                page["lines"] = cleaned_lines
            
            cleaned_pages.append(page)
        
        data["pages"] = cleaned_pages

        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"  - Saved cleaned file to '{target_path}'")

    print("\n--- 'Truly Clean' Ground Truth creation finished ---")


if __name__ == "__main__":
    main()