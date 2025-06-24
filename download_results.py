import os
import re
from datetime import datetime

# ודא שהספרייה מותקנת: pip install google-cloud-storage
try:
    from google.cloud import storage
except ImportError:
    print("Error: google-cloud-storage library not found.")
    print("Please run 'pip install google-cloud-storage'")
    exit()

# --- הגדרות ---
# ודא שהפרטים הבאים נכונים
GCS_BUCKET_NAME = "alsheich-protocols-bucket-2025"
# זהו הנתיב המלא לתיקייה בענן שבה נמצאים קבצי ה-JSON מהריצה האחרונה
GCS_RESULTS_PREFIX = "batch_results_60_pages/5337763716943116234/0/"

# תיקייה מקומית חדשה שבה יישמרו הקבצים
LOCAL_OUTPUT_DIR = "downloaded_json_parts"

def download_gcs_folder_contents(bucket_name, prefix, local_dir):
    """
    Downloads all files from a specified GCS folder to a local directory.
    """
    print(f"Preparing to download from gs://{bucket_name}/{prefix}")
    
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
        print(f"Created local directory: {local_dir}")

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        blob_list = list(bucket.list_blobs(prefix=prefix))
        
        if not blob_list:
            print(f"Error: No files found at the specified path: {prefix}")
            return

        print(f"Found {len(blob_list)} files to download.")

        for blob in blob_list:
            # יצירת שם קובץ מקומי פשוט (רק שם הקובץ עצמו)
            file_name = os.path.basename(blob.name)
            destination_file_name = os.path.join(local_dir, file_name)
            
            print(f"  - Downloading {blob.name} to {destination_file_name}...")
            blob.download_to_filename(destination_file_name)

        print("\nDownload complete.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_gcs_folder_contents(GCS_BUCKET_NAME, GCS_RESULTS_PREFIX, LOCAL_OUTPUT_DIR)