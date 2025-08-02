import pandas as pd

def save_to_excel(df, out_path):
    df.to_excel(out_path, index=False)
