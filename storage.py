import json

def load_records():
    try:
        with open("data/records.json", "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        return []  

def load_settings():
    try:
        with open("data/settings.json", "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        return {
            "time_step": 1,
            "time_input_unit": "minutes"
        }

def save_records(records):
    with open("data/records.json", "w", encoding="utf-8") as f:
       json.dump(
           records,
           f,
           ensure_ascii=False,
           indent=2
       )

def save_settings(settings):
    with open("data/settings.json", "w", encoding="utf-8") as f:
        json.dump(
            settings,
            f,
            ensure_ascii=False,
            indent=2
        )