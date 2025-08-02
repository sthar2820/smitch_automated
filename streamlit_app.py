import streamlit as st
import os
import zipfile
from io import BytesIO
from utils.logger import load_processed_log, update_log
from utils.file_utils import get_file_metadata
from utils.extractor import extract_smitch_data_from_path
from utils.saver import save_to_excel

st.title("SMITCH Automated Extractor")

# Step 1: Folder Input
uploaded_folder = st.text_input("Enter path to centralized folder", value=r"C:\Users\sthar\Downloads\SMITCH_2025")
extracted_folder = "extracted_outputs"
os.makedirs(extracted_folder, exist_ok=True)

# Step 2: Load JSON log
processed_log = load_processed_log()
new_log = processed_log.copy()

# Step 3: Trigger Extraction
if st.button("Extract Data"):
    with st.spinner("Scanning and extracting files..."):
        count = 0
        for root, _, files in os.walk(uploaded_folder):
            for file in files:
                if file.endswith(".xlsm") or file.endswith(".xlsx"):
                    full_path = os.path.join(root, file)
                    metadata = get_file_metadata(full_path)

                    if full_path not in processed_log or processed_log[full_path] != metadata:
                        try:
                            st.write(f"Processing: `{os.path.relpath(full_path, uploaded_folder)}`")
                            extracted_data = extract_smitch_data_from_path(full_path)
                            if extracted_data:
                                # Construct clean file name using subfolder + file
                                relative_path = os.path.relpath(full_path, uploaded_folder)
                                safe_name = relative_path.replace("\\", "_").replace("/", "_").replace(" ", "_")
                                output_filename = os.path.splitext(safe_name)[0] + "_extracted.xlsx"
                                output_path = os.path.join(extracted_folder, output_filename)

                                save_to_excel(extracted_data, output_path)
                                new_log[full_path] = metadata
                                count += 1
                            else:
                                st.warning(f"No data extracted from: {file}")
                        except Exception as e:
                            st.error(f"Failed: {file} → {str(e)}")
        update_log(new_log)
        st.success(f"✅ Extraction complete. {count} new/updated file(s) processed.")

# Step 4: Download Button
if st.button("Download All Extracted Files"):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for fname in os.listdir(extracted_folder):
            fpath = os.path.join(extracted_folder, fname)
            zipf.write(fpath, arcname=fname)

    st.download_button(
        label="⬇️ Download ZIP",
        data=zip_buffer.getvalue(),
        file_name="SMITCH_Extracted.zip",
        mime="application/zip"
    )
