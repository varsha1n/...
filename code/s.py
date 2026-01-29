import os
import time
import subprocess
import sqlite3 # Example DB

# Configuration
SHARED_FOLDER = "../uploads/shared/"
PROCESSED_FOLDER = "./processed_lrs/"
SCRIPT_PATH = "./script.py"
DB_PATH = "../db/data.db"

def run_workflow():
    print("--- Starting 5-minute check ---")
    
    # Ensure processed folder exists
    if not os.path.exists(PROCESSED_FOLDER):
        os.makedirs(PROCESSED_FOLDER)

    for filename in os.listdir(SHARED_FOLDER):
        if filename.endswith((".xlsx", ".xls")):
            excel_path = os.path.join(SHARED_FOLDER, filename)
            lr_filename = filename.rsplit('.', 1)[0] + ".lr"
            lr_path = os.path.join(PROCESSED_FOLDER, lr_filename)

            # 1. SERVER RUNS SCRIPT
            # Passing file paths as arguments to script.py
            result = subprocess.run(["python", SCRIPT_PATH, excel_path, lr_path], 
                                     capture_output=True, text=True)
            
            if result.returncode == 0:
                # 2. SERVER DUMPS .LR TEXT TO DB
                dump_to_db(lr_path)
                # 3. Clean up (Optional: move/delete original excel so it's not processed again)
                # os.remove(excel_path) 
            else:
                print(f"Failed to process {filename}: {result.stderr}")

def dump_to_db(lr_file_path):
    with open(lr_file_path, 'r') as f:
        content = f.read()
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Assuming a table named 'logs' with a column 'raw_data'
    cursor.execute("INSERT INTO logs (raw_data) VALUES (?)", (content,))
    conn.commit()
    conn.close()
    print(f"Imported {os.path.basename(lr_file_path)} to Database.")

# MAIN LOOP (5 Minute Interval)
while True:
    run_workflow()
    print("Waiting 5 minutes...")
    time.sleep(300) # 300 seconds = 5 minutes