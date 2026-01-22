import os
import time
import shutil
import requests
import pandas as pd
import os


# ===== CONFIGURATION =====
WATCH_FOLDER = "shared/uploads"
COMPLETED_FOLDER = "shared/completed"
ARCHIVE_FOLDER = "shared/archive"
API_ENDPOINT = "https://your-server.com/api/upload"
API_TOKEN = "YOUR_API_TOKEN"

SCAN_INTERVAL = 300   # 300 seconds = 5 minutes

os.makedirs(ARCHIVE_FOLDER, exist_ok=True)
os.makedirs(COMPLETED_FOLDER, exist_ok=True)

def is_file_ready(filepath):
    """Check file is fully uploaded by verifying size stability."""
    print("is_file_ready")
    size1 = os.path.getsize(filepath)
    print(size1)
    time.sleep(2)
    size2 = os.path.getsize(filepath)
    print(size2)
    return size1 == size2


def convert_excel_to_lr(excel_path):
    filename = os.path.splitext(os.path.basename(excel_path))[0]
    lr_path = os.path.join(os.path.dirname(excel_path), filename + ".lr")

    # Read Excel file into DataFrame
    df = pd.read_excel(excel_path, engine="openpyxl")

    # Save as comma-separated text with .lr extension
    df.to_csv(lr_path, index=False)

    return lr_path


def upload_file(file_path):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(API_ENDPOINT, headers=headers, files=files)

    if response.status_code == 200:
        print(f"Uploaded: {file_path}")
        return True
    else:
        print(f"Upload failed: {file_path} → {response.text}")
        return False

def process_files():
    print("In process_files")
    for filename in os.listdir(WATCH_FOLDER):
        print(filename)
        if not filename.lower().endswith(".xlsx"):
            continue

        csv_path = os.path.join(WATCH_FOLDER, filename)

        if not is_file_ready(csv_path):
            continue

        print(f"Processing: {filename}")

        try:
            lr_path = convert_excel_to_lr(csv_path)


            #if upload_file(lr_path):
                #shutil.move(csv_path, os.path.join(ARCHIVE_FOLDER, filename))
                #shutil.move(lr_path, os.path.join(ARCHIVE_FOLDER, os.path.basename(lr_path)))

            
       
            shutil.move(csv_path, os.path.join(ARCHIVE_FOLDER, filename))
            shutil.move(lr_path, os.path.join(COMPLETED_FOLDER, os.path.basename(lr_path)))

            print("Processing completed for:", filename)

        except Exception as e:
            print(f"Error processing {filename}: {e}")

def main():
    print("Folder watcher started. Scanning every 5 minutes...")

    while True:
        process_files()
        time.sleep(SCAN_INTERVAL)
        

if __name__ == "__main__":
    main()
