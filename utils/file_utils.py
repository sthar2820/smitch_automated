import os
import hashlib

def get_file_metadata(file_path):
    """
    Return a hash of the file content + last modified time.
    """
    try:
        stat = os.stat(file_path)
        with open(file_path, "rb") as f:
            content = f.read()
        file_hash = hashlib.md5(content).hexdigest()
        return f"{stat.st_mtime}-{file_hash}"
    except Exception:
        return None
