import json

def load_records(file_path="data/records.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        return []  

def load_settings(file_path="data/settings.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        return {
            "time_step": 1,
            "time_input_unit": "minutes"
        }

def save_records(records, file_path="data/records.json"):
    with open(file_path, "w", encoding="utf-8") as f:
       json.dump(
           records,
           f,
           ensure_ascii=False,
           indent=2
       )

def save_settings(settings, file_path="data/settings.json"):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(
            settings,
            f,
            ensure_ascii=False,
            indent=2
        )