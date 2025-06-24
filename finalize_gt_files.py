import os
import json

# --- הגדרות ---
SOURCE_DIR = "truth_test/truly_cleaned_parts/" # קוראים מהנקיים-באמת
TARGET_DIR = "truth_test/final_gt_parts/" # שומרים בתיקייה חדשה וסופית
HEADER_Y_BOUNDARY_PT = 178.6  # 6.3 cm
FOOTER_Y_BOUNDARY_PT = 780 # אזור החתימות התחתון
TOTAL_CHUNKS = 12
# ----------------

def main():
    print("--- Starting Final Ground Truth Cleaning Script ---")
    os.makedirs(TARGET_DIR, exist_ok=True)

    for i in range(TOTAL_CHUNKS):
        source_filename = f"TRULY_CLEANED_full_ground_truth_protocol-{i}.json"
        target_filename = f"FINAL_full_ground_truth_protocol-{i}.json"
        
        source_path = os.path.join(SOURCE_DIR, source_filename)
        target_path = os.path.join(TARGET_DIR, target_filename)

        print(f"Processing '{source_path}'...")

        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"  - ERROR reading or parsing file: {e}")
            continue

        cleaned_pages = []
        full_text = data.get('text', '')

        for page in data.get("pages", []):
            original_lines = page.get("lines", [])
            
            # סינון כותרות וחתימות לפי מיקום
            final_lines = []
            for line in original_lines:
                y_coord = line.get("layout", {}).get("boundingPoly", {}).get("normalizedVertices", [{}, {}, {}, {}])[0].get("y", 0.0) * 842
                if not (y_coord < HEADER_Y_BOUNDARY_PT or y_coord > FOOTER_Y_BOUNDARY_PT):
                    final_lines.append(line)
            
            page["lines"] = final_lines
            cleaned_pages.append(page)
        
        data["pages"] = cleaned_pages

        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"  - Saved final GT file to '{target_path}'")

    print("\n--- Final GT cleaning finished ---")

if __name__ == "__main__":
    main()