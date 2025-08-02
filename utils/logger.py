import os
import json

LOG_FILE = "logs/processed_files.json"

def load_processed_log():
    if not os.path.exists(LOG_FILE):
        return {}

    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # Log file exists but is corrupted or empty → reset
        return {}

def update_log(new_log):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "w") as f:
        json.dump(new_log, f, indent=4)
