import pandas as pd

def save_to_excel(data, path):
    # Convert list of dictionaries to DataFrame if necessary
    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = data
    
    df.to_excel(path, index=False)
