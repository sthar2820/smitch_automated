import os
import hashlib

def get_file_metadata(path):
    stat = os.stat(path)
    return {
        "modified": stat.st_mtime,
        "size": stat.st_size,
    }

