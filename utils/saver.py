import os
import pandas as pd

def save_to_excel(df, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_excel(output_path, index=False)

