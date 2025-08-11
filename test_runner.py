import os
import sys
import re

# Add root to path for module discovery
sys.path.append(os.path.dirname(__file__))

from config import Config
from utils.logger import load_processed_log, update_log
from utils.file_utils import get_file_metadata
from utils.extractor import extract_smitch_data_from_path
from utils.saver import save_to_excel

# Use configuration paths instead of hardcoded ones
centralized_folder = Config.WATCH_PATH
extracted_folder = Config.OUTPUT_PATH
os.makedirs(extracted_folder, exist_ok=True)

print(f"Processing files from: {centralized_folder}")
print(f"Saving extracted data to: {extracted_folder}")

# Load previous log
processed_log = load_processed_log()
new_log = processed_log.copy()

# Process files
extracted_count = 0
for root, _, files in os.walk(centralized_folder):
    for file in files:
        if file.endswith(".xlsm") or file.endswith(".xlsx"):
            full_path = os.path.join(root, file)
            metadata = get_file_metadata(full_path)

            if full_path not in processed_log or processed_log[full_path] != metadata:
                print(f"Processing: {file}")
                try:
                    extracted_data = extract_smitch_data_from_path(full_path)
                    if extracted_data:
                        # Include subfolder name in output file name to avoid collisions
                        subfolder = os.path.relpath(root, centralized_folder).replace("\\", "_").replace("/", "_")
                        output_filename = f"{subfolder}_{os.path.splitext(file)[0]}_extracted.xlsx"
                        output_path = os.path.join(extracted_folder, output_filename)
                        save_to_excel(extracted_data, output_path)
                        new_log[full_path] = metadata
                        extracted_count += 1
                    else:
                        print(f"[!] No data extracted from: {file}")
                except Exception as e:
                    print(f"[X] Failed: {file} -> {str(e)}")

# Update log
update_log(new_log)
print(f"\nExtraction complete. {extracted_count} file(s) processed and saved in '{extracted_folder}'.")
