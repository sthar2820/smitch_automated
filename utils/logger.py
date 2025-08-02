import os
import json

LOG_PATH = os.path.join("logs", "processed_files.json")

def load_processed_log():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            return json.load(f)
    return {}

def update_log(log_dict):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_PATH, "w") as f:
        json.dump(log_dict, f, indent=2)
