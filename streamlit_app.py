import streamlit as st
import os
import zipfile
from io import BytesIO
from utils.logger import load_processed_log, update_log
from utils.file_utils import get_file_metadata
from utils.extractor import extract_smitch_data  # your custom extraction logic
from utils.saver import save_to_excel  # utility to save DataFrame to Excel

# --- UI Input ---
st.title("SMITCH Excel Extractor")
uploaded_folder = st.text_input("Enter path to centralized folder", value=r"C:\Users\sthar\Downloads\SMITCH_2025\SMITCH_2025")

extracted_folder = "extracted_outputs/"
os.makedirs(extracted_folder, exist_ok=True)

# --- Load JSON log for processed files ---
processed_log = load_processed_log()
new_log = processed_log.copy()

# --- Process Files ---
if uploaded_folder and os.path.isdir(uploaded_folder):
    with st.spinner("Extracting updated files..."):
        for root, _, files in os.walk(uploaded_folder):
            for file in files:
                if file.endswith((".xlsm", ".xlsx")) and not file.startswith("~$"):
                    full_path = os.path.join(root, file)
                    metadata = get_file_metadata(full_path)

                    if full_path not in processed_log or processed_log[full_path] != metadata:
                        st.write(f" Processing: {file}")
                        try:
                            extracted_df = extract_smitch_data(full_path)
                            out_path = os.path.join(extracted_folder, f"{os.path.splitext(file)[0]}_extracted.xlsx")
                            save_to_excel(extracted_df, out_path)
                            new_log[full_path] = metadata
                        except Exception as e:
                            st.error(f" Failed: {file} → {str(e)}")
        update_log(new_log)
        st.success(" Extraction complete.")
else:
    st.warning(" Please enter a valid folder path.")

# --- Download ZIP of all extracted files ---
if st.button("Download All Extracted Files"):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for fname in os.listdir(extracted_folder):
            fpath = os.path.join(extracted_folder, fname)
            zipf.write(fpath, arcname=fname)

    st.download_button(
        label=" Download ZIP",
        data=zip_buffer.getvalue(),
        file_name="SMITCH_Extracted.zip",
        mime="application/zip"
    )
