import json
import os

LOG_PATH = "logs/processed_files.json"

def load_processed_log():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            return json.load(f)
    return {}

def update_log(new_log):
    with open(LOG_PATH, "w") as f:
        json.dump(new_log, f, indent=4)

