# llm_extraction_bakeoff_v0.6.py
import os
import json
import time
from datetime import datetime
import csv
import sys

# --- ייבוא חבילות חיצוניות ---
try:
    # התקנה: pip install google-cloud-documentai
    from google.cloud import documentai
except ImportError:
    print("Error: google-cloud-documentai is not installed. Please run 'pip install google-cloud-documentai'")
    sys.exit(1)

# --- הגדרות ---
# !!! עדכן את הפרטים הבאים בהתאם לפרויקט שלך ב-Google Cloud !!!
PROJECT_ID = "alsheich"  # החלף ב-Project ID שלך
LOCATION = "eu"          # החלף במיקום המעבד שלך (למשל, 'us' או 'eu')
PROCESSOR_ID = "efb92619c5d2957f" # החלף ב-ID של המעבד שיצרת (Form Parser)

# הגדרות קבצים
INPUT_PDF_FILE = 'full_ground_truth_protocol.pdf'
OUTPUT_DIR_BASE = 'test_results_doc_ai'

def process_document_with_doc_ai(
    project_id: str, location: str, processor_id: str, file_path: str
) -> tuple[documentai.Document | None, str | None]:
    """
    מעבד קובץ PDF באמצעות Document AI ומחזיר את אובייקט התוצאה.
    """
    print(f"Connecting to Document AI service...")
    try:
        # הגדרת נקודת הגישה ל-API בהתאם למיקום
        opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
        client = documentai.DocumentProcessorServiceClient(client_options=opts)

        # הרכבת שם המעבד המלא
        name = client.processor_path(project_id, location, processor_id)

        print(f"Reading PDF file: {file_path}")
        # קריאת הקובץ כבינארי
        with open(file_path, "rb") as f:
            image_content = f.read()

        # הגדרת הבקשה
        raw_document = documentai.RawDocument(
            content=image_content, mime_type="application/pdf"
        )
        request = documentai.ProcessRequest(name=name, raw_document=raw_document)

        print("Sending request to Document AI... (This may take a moment)")
        # שליחת הבקשה וקבלת התשובה
        result = client.process_document(request=request)
        print("Successfully received response from Document AI.")
        return result.document, None
    except Exception as e:
        error_message = f"Document AI API Error: {type(e).__name__}: {e}"
        print(f"CRITICAL ERROR: {error_message}")
        return None, error_message

def main():
    """
    הפונקציה הראשית שמנהלת את תהליך העיבוד.
    """
    if not all([PROJECT_ID, LOCATION, PROCESSOR_ID]):
        print("CRITICAL: PROJECT_ID, LOCATION, or PROCESSOR_ID are not set in the script.")
        return
        
    if not os.path.exists(INPUT_PDF_FILE):
        print(f"CRITICAL: Input PDF file not found at '{INPUT_PDF_FILE}'")
        return

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    run_dir = os.path.join(OUTPUT_DIR_BASE, f"run_{timestamp}_doc_ai")
    os.makedirs(run_dir, exist_ok=True)
    print(f"Results will be saved in: {run_dir}")

    csv_file_path = os.path.join(run_dir, "summary_results.csv")
    csv_headers = [
        "Processor_Name", "File_Name", "Total_Pages", "Status", 
        "Processing_Duration_s", "Error_Details"
    ]
    
    row_data = {
        "Processor_Name": f"DocAI_{PROCESSOR_ID[:8]}",
        "File_Name": INPUT_PDF_FILE,
        "Status": "Unknown Error"
    }

    start_time = time.time()
    
    # --- ליבת העיבוד ---
    document_obj, error = process_document_with_doc_ai(
        project_id=PROJECT_ID,
        location=LOCATION,
        processor_id=PROCESSOR_ID,
        file_path=INPUT_PDF_FILE
    )
    
    duration = time.time() - start_time
    row_data["Processing_Duration_s"] = round(duration, 2)

    if error or not document_obj:
        row_data["Status"] = "Failed"
        row_data["Error_Details"] = error
    else:
        row_data["Status"] = "Success"
        row_data["Total_Pages"] = len(document_obj.pages)
        
        # שמירת התוכן המלא כ-JSON
        # אובייקט התוצאה של Document AI הוא מורכב, לכן נמיר אותו למילון
        # באמצעות כלי מובנה של הספרייה.
        try:
            json_output_path = os.path.join(run_dir, f"{os.path.basename(INPUT_PDF_FILE)}_full_output.json")
            # המרת האובייקט המורכב לייצוג JSON סטנדרטי
            json_string = documentai.Document.to_json(document_obj)
            
            # טעינה מחדש כדי שיהיה קריא (pretty-print)
            parsed_json = json.loads(json_string)
            
            with open(json_output_path, "w", encoding='utf-8') as f:
                json.dump(parsed_json, f, ensure_ascii=False, indent=2)
            print(f"Full Document AI JSON response saved to: {json_output_path}")

        except Exception as e:
            print(f"Error saving JSON output: {e}")
            row_data["Status"] = "Success (with JSON save error)"
            row_data["Error_Details"] = f"JSON save error: {e}"

        # שמירת הטקסט שחולץ לקובץ נפרד לנוחות
        try:
            text_output_path = os.path.join(run_dir, f"{os.path.basename(INPUT_PDF_FILE)}_extracted_text.txt")
            with open(text_output_path, "w", encoding='utf-8') as f:
                f.write(document_obj.text)
            print(f"Extracted text saved to: {text_output_path}")
        except Exception as e:
            print(f"Error saving plain text output: {e}")


    # כתיבת שורת הסיכום לקובץ ה-CSV
    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_headers, extrasaction='ignore')
            writer.writeheader()
            writer.writerow(row_data)
        print(f"\n--- All operations completed. Results summary saved to '{csv_file_path}' ---")
    except IOError as e:
        print(f"Error writing to CSV file: {e}")

if __name__ == "__main__":
    main()