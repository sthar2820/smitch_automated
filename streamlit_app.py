import streamlit as st
import os
import zipfile
import pandas as pd
from io import BytesIO

from utils.logger import load_processed_log, update_log
from utils.file_utils import get_file_metadata
from utils.extractor import extract_smitch_data_from_path
from utils.saver import save_to_excel

# Input centralized folder path
uploaded_folder = st.text_input("Enter path to centralized folder", value=r"C:\Users\sthar\Downloads\SMITCH_2025\SMITCH_2025")
extracted_folder = "extracted_outputs/"
os.makedirs(extracted_folder, exist_ok=True)

processed_log = load_processed_log()
new_log = processed_log.copy()

with st.spinner("Scanning folder and extracting updated files..."):
    for root, _, files in os.walk(uploaded_folder):
        for file in files:
            if file.endswith(".xlsm") or file.endswith(".xlsx"):
                full_path = os.path.join(root, file)
                metadata = get_file_metadata(full_path)

                if full_path not in processed_log or processed_log[full_path] != metadata:
                    st.write(f"Processing: {file}")
                    try:
                        extracted = extract_smitch_data_from_path(full_path)
                        if extracted:
                            df = pd.DataFrame(extracted)
                            output_name = os.path.splitext(file)[0] + "_extracted.xlsx"
                            save_to_excel(df, os.path.join(extracted_folder, output_name))
                            new_log[full_path] = metadata
                        else:
                            st.warning(f"No data extracted from {file}")
                    except Exception as e:
                        st.error(f"Failed to process {file}: {e}")

update_log(new_log)

# Allow user to download all extracted files as ZIP
if st.button("Download All Extracted Files"):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for fname in os.listdir(extracted_folder):
            fpath = os.path.join(extracted_folder, fname)
            zipf.write(fpath, arcname=fname)

    st.download_button(
        label="Download ZIP",
        data=zip_buffer.getvalue(),
        file_name="SMITCH_Extracted.zip",
        mime="application/zip"
    )
