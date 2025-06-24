import os
import json
import time
from datetime import datetime
import csv
import sys
import re

# --- ייבוא חבילות חיצוניות ---
try:
    from google.cloud import documentai
    from google.cloud import storage
except ImportError:
    print("Error: Required Google Cloud libraries not installed.")
    print("Please run 'pip install google-cloud-documentai google-cloud-storage'")
    sys.exit(1)

# --- הגדרות ---
PROJECT_ID = "alsheich"
LOCATION = "eu"
PROCESSOR_ID = "efb92619c5d2957f"
GCS_BUCKET_NAME = "alsheich-protocols-bucket-2025"
GCS_INPUT_FILE_NAME = "full_ground_truth_protocol.pdf" # ודא שזו גרסת ה-60 עמודים
GCS_OUTPUT_PREFIX = "batch_results_60_pages/" # תיקיית פלט חדשה כדי לא להתבלבל

OUTPUT_DIR_BASE = 'test_results_doc_ai_batch'

def process_batch_with_doc_ai(
    project_id: str, location: str, processor_id: str,
    bucket: str, input_file: str, output_prefix: str
) -> tuple[str | None, str | None]:
    """
    מתחיל משימת עיבוד אצווה א-סינכרונית ב-Document AI וממתין לסיומה.
    """
    print("Connecting to Document AI service for BATCH processing...")
    try:
        opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
        client = documentai.DocumentProcessorServiceClient(client_options=opts)

        gcs_input_uri = f"gs://{bucket}/{input_file}"
        gcs_output_uri = f"gs://{bucket}/{output_prefix}"

        gcs_document = documentai.GcsDocument(
            gcs_uri=gcs_input_uri, mime_type="application/pdf"
        )
        gcs_documents = documentai.GcsDocuments(documents=[gcs_document])
        input_config = documentai.BatchDocumentsInputConfig(gcs_documents=gcs_documents)

        output_config = documentai.DocumentOutputConfig(
            gcs_output_config=documentai.DocumentOutputConfig.GcsOutputConfig(
                gcs_uri=gcs_output_uri
            )
        )
        
        name = client.processor_path(project_id, location, processor_id)
        request = documentai.BatchProcessRequest(
            name=name,
            input_documents=input_config,
            document_output_config=output_config,
        )

        print(f"Starting batch operation for '{gcs_input_uri}'.")
        print("This may take several minutes. The script will wait for completion...")
        operation = client.batch_process_documents(request)
        
        operation.result(timeout=1800)
        
        print("Batch operation completed successfully in the cloud.")
        
        metadata = documentai.BatchProcessMetadata(operation.metadata)
        first_process = metadata.individual_process_statuses[0]
        output_gcs_path = first_process.output_gcs_destination
        
        return output_gcs_path, None

    except Exception as e:
        error_message = f"Document AI Batch API Error: {type(e).__name__}: {e}"
        print(f"CRITICAL ERROR: {error_message}")
        return None, error_message

def download_and_stitch_results(gcs_path: str, local_run_dir: str) -> tuple[str | None, str | None]:
    """
    מוריד את כל קבצי ה-JSON מתיקיית הפלט, מאחד אותם, ושומר את התוצאה.
    """
    print(f"Downloading and stitching results from: {gcs_path}")
    try:
        match = re.match(r"gs://(.*?)/(.*)", gcs_path)
        if not match:
            return None, f"Could not parse GCS path: {gcs_path}"
        
        bucket_name, blob_prefix = match.groups()
        
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        blob_list = list(bucket.list_blobs(prefix=blob_prefix))
        json_blobs = [b for b in blob_list if b.name.endswith(".json")]

        if not json_blobs:
            return None, f"Could not find any .json files in the output path: {blob_prefix}"
        
        print(f"Found {len(json_blobs)} JSON parts to stitch.")

        stitched_document = None
        
        # מיון הקבצים כדי להבטיח סדר נכון (0, 1, 2... 10, 11)
        # המיון הזה מטפל בבעיה שמיון טקסט רגיל היה שם את '10' לפני '2'.
        json_blobs.sort(key=lambda x: int(re.search(r'-(\d+)\.json$', x.name).group(1)))

        for blob in json_blobs:
            print(f"  - Processing part: {blob.name}")
            json_string = blob.download_as_text()
            doc_part = documentai.Document.from_json(json_string)

            if stitched_document is None:
                stitched_document = doc_part
            else:
                stitched_document.pages.extend(doc_part.pages)
                stitched_document.text += doc_part.text

        final_json_string = documentai.Document.to_json(stitched_document)
        final_json_dict = json.loads(final_json_string)

        local_json_filename = os.path.join(local_run_dir, "full_stitched_output.json")
        with open(local_json_filename, "w", encoding='utf-8') as f:
            json.dump(final_json_dict, f, ensure_ascii=False, indent=2)
        print(f"Successfully saved stitched JSON to '{local_json_filename}'")

        local_text_filename = os.path.join(local_run_dir, "full_stitched_text.txt")
        with open(local_text_filename, 'w', encoding='utf-8') as f:
            f.write(stitched_document.text)
        print(f"Extracted full text saved to '{local_text_filename}'")
        
        return local_json_filename, None

    except Exception as e:
        error_message = f"GCS Download/Stitch Error: {type(e).__name__}: {e}"
        print(f"CRITICAL ERROR: {error_message}")
        return None, error_message

def main():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    run_dir = os.path.join(OUTPUT_DIR_BASE, f"run_{timestamp}_stitched")
    os.makedirs(run_dir, exist_ok=True)
    print(f"Local results will be saved in: {run_dir}")

    csv_file_path = os.path.join(run_dir, "summary_results.csv")
    csv_headers = ["File_Name", "Total_Pages", "Status", "Processing_Duration_s", "Error_Details"]
    
    row_data = {"File_Name": GCS_INPUT_FILE_NAME, "Status": "Unknown Error"}

    start_time = time.time()
    
    output_path, error = process_batch_with_doc_ai(
        project_id=PROJECT_ID, location=LOCATION, processor_id=PROCESSOR_ID,
        bucket=GCS_BUCKET_NAME, input_file=GCS_INPUT_FILE_NAME, output_prefix=GCS_OUTPUT_PREFIX
    )
    
    if error or not output_path:
        row_data["Status"] = "Failed - Batch Process"
        row_data["Error_Details"] = error
    else:
        local_file, stitch_error = download_and_stitch_results(output_path, run_dir)
        if stitch_error:
            row_data["Status"] = "Failed - Download/Stitch"
            row_data["Error_Details"] = stitch_error
        else:
            row_data["Status"] = "Success"
            row_data["Total_Pages"] = 60
    
    duration = time.time() - start_time
    row_data["Processing_Duration_s"] = round(duration, 2)

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