import streamlit as st
import os
from utils.logger import load_processed_log, update_log
from utils.file_utils import get_file_metadata
from utils.extractor import extract_smitch_data_from_path  # <- make sure this returns a list of dicts
from utils.saver import save_to_excel
import zipfile
from io import BytesIO

st.title("SMITCH Extractor App")

uploaded_folder = st.text_input("Enter path to centralized folder", value=r"C:\Users\sthar\Downloads\SMITCH_2025\SMITCH_2025")
extracted_folder = "extracted_outputs"
os.makedirs(extracted_folder, exist_ok=True)

# Load previous log
processed_log = load_processed_log()
new_log = processed_log.copy()

if st.button("Extract Data"):
    with st.spinner("Extracting files..."):
        count = 0
        for root, _, files in os.walk(uploaded_folder):
            for file in files:
                if file.endswith(".xlsm") or file.endswith(".xlsx"):
                    full_path = os.path.join(root, file)
                    metadata = get_file_metadata(full_path)

                    if full_path not in processed_log or processed_log[full_path] != metadata:
                        st.write(f"Processing: {file}")
                        try:
                            extracted_data = extract_smitch_data_from_path(full_path)
                            if extracted_data:
                                output_filename = os.path.splitext(file)[0] + "_extracted.xlsx"
                                output_path = os.path.join(extracted_folder, output_filename)
                                save_to_excel(extracted_data, output_path)
                                new_log[full_path] = metadata
                                count += 1
                            else:
                                st.warning(f"No data extracted from {file}")
                        except Exception as e:
                            st.error(f"Failed: {file} → {str(e)}")
        st.success(f"Extraction complete. {count} files extracted.")
        update_log(new_log)

# Download extracted files
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
