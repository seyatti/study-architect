import pytest
from storage import save_records, load_records, save_settings, load_settings

def test_save_and_load_records(tmp_path):
    records = [
        {
            "date": "2026-09-20",
            "subject": "Python",
            "minutes": 90
        },
        {
            "date": "2026-09-21",
            "subject": "英語",
            "minutes": 45
        }
    ]

    save_records(records, file_path = tmp_path / "records.json")

    result = load_records(file_path = tmp_path / "records.json")

    assert result == records

def test_save_and_load_records_empty(tmp_path):

    result = load_records(file_path = tmp_path / "not_found.json")

    assert result == []

def test_save_and_load_settings(tmp_path):
    settings = {
        "time_step": 15,
        "time_input_unit": "hours"
    }

    save_settings(settings, tmp_path / "settings.json")

    result = load_settings(tmp_path / "settings.json")

    assert result == settings

def test_save_and_load_settings_empty(tmp_path):

    result = load_settings(tmp_path / "not_found.json")

    assert result == {
        "time_step": 1,
        "time_input_unit": "minutes"
    }