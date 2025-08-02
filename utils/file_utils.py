import os

def get_file_metadata(path):
    try:
        return os.path.getmtime(path)
    except:
        return None
