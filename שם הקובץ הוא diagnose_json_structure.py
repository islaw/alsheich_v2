import os
import json

# --- הגדרות ---
# נבדוק את קובץ האמת המוחלטת החדש והנקי
FILE_TO_INSPECT = "truth_test/truly_cleaned_parts/TRULY_CLEANED_full_ground_truth_protocol-0.json"
# ----------------

def main():
    print(f"--- Inspecting JSON structure of: {FILE_TO_INSPECT} ---")

    try:
        with open(FILE_TO_INSPECT, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Could not read or parse the file. Error: {e}")
        return

    # הדפסת המפתחות ברמה העליונה
    print("\nTop-level keys:")
    print(list(data.keys()))

    # בדיקה אם קיים המפתח 'pages'
    if "pages" in data and isinstance(data["pages"], list) and len(data["pages"]) > 0:
        # לקיחת העמוד הראשון כדוגמה
        first_page = data["pages"][0]
        print("\nKeys in the first page object:")
        print(list(first_page.keys()))

        # בדיקה אם קיים המפתח 'lines' בעמוד
        if "lines" in first_page and isinstance(first_page["lines"], list) and len(first_page["lines"]) > 0:
            # לקיחת השורה הראשונה כדוגמה
            first_line = first_page["lines"][0]
            print("\nKeys in the first line object of the first page:")
            print(list(first_line.keys()))
        else:
            print("\n'lines' key not found or is empty in the first page.")

    else:
        print("\n'pages' key not found or is not a non-empty list.")

    print("\n--- Inspection Finished ---")


if __name__ == "__main__":
    main()