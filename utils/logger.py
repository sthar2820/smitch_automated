import os
import json

LOG_PATH = "logs/processed_files.json"
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def load_processed_log():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            return json.load(f)
    return {}

def update_log(log_data):
    with open(LOG_PATH, "w") as f:
        json.dump(log_data, f, indent=4)
