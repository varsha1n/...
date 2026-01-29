import pandas as pd
import sys
import os

def convert_excel_to_lr(input_path, output_path):
    try:
        # Read Excel (supports .xlsx and .xls)
        df = pd.read_excel(input_path)
        
        # Convert to Comma Separated Values and save as .lr
        # index=False prevents pandas from adding a row counter column
        df.to_csv(output_path, index=False)
        print(f"SUCCESS: Converted {os.path.basename(input_path)}")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Expecting arguments from server.py
    if len(sys.argv) > 2:
        convert_excel_to_lr(sys.argv[1], sys.argv[2])