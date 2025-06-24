import os
import json
import re

# --- Constants ---
# הנתיב לקובץ ה-JSON הגולמי מ-Document AI שיש לאבחן
GROUND_TRUTH_JSON_DIR = 'downloaded_json_parts'
INPUT_JSON_FILENAME = 'full_ground_truth_protocol-0.json'

def diagnose_geometry(file_path):
    """
    Analyzes the geometric layout of a Document AI JSON file.
    Instead of filtering, it prints the calculated vertical position (pixel_y)
    for each paragraph to help determine the correct header threshold.
    """
    print(f"--- מתחיל אבחון גיאומטרי לקובץ: {file_path} ---")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        full_text_content = data.get('text', '')
        
        if not full_text_content:
            print("שגיאה: לא נמצא מפתח 'text' בקובץ ה-JSON.")
            return

        # The 'pages' key is at the top level of the JSON object.
        for i, page in enumerate(data.get('pages', [])):
            print(f"\n--- עמוד מספר {i + 1} ---")
            page_height = page.get('dimension', {}).get('height', 1122) # Default A4 height in pixels

            for paragraph in page.get('paragraphs', []):
                # Calculate the average Y-coordinate for the paragraph
                avg_y = 0
                vertices = paragraph.get('layout', {}).get('boundingPoly', {}).get('normalizedVertices', [])
                if not vertices:
                    continue
                
                y_coords = [v.get('y', 0) for v in vertices]
                avg_y = sum(y_coords) / len(y_coords) if y_coords else 0
                
                # Convert normalized Y to pixel Y
                pixel_y = avg_y * page_height

                # Extract the text content of the paragraph
                paragraph_text = ""
                text_anchor = paragraph.get('layout', {}).get('textAnchor', {})
                for segment in text_anchor.get('textSegments', []):
                    start = int(segment.get('startIndex', 0))
                    end = int(segment.get('endIndex', 0))
                    paragraph_text += full_text_content[start:end]
                
                # Print the diagnostic information
                print(f"Pixel Y: {int(pixel_y):<5} | Text: {paragraph_text.strip()[:80]}")

    except FileNotFoundError:
        print(f"שגיאה: הקובץ לא נמצא בנתיב {file_path}")
    except json.JSONDecodeError:
        print(f"שגיאה: לא ניתן לפענח את קובץ ה-JSON. ייתכן שהוא פגום.")
    except Exception as e:
        print(f"אירעה שגיאה לא צפויה: {e}")

def main():
    """Main function to run the diagnosis."""
    file_to_diagnose = os.path.join(GROUND_TRUTH_JSON_DIR, INPUT_JSON_FILENAME)
    diagnose_geometry(file_to_diagnose)
    print("\n--- אבחון הסתיים ---")

if __name__ == "__main__":
    main()