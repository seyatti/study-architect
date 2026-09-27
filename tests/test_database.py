from database import (
    initialize_database,
    add_record,
    get_records,
    update_record,
    delete_record,
    save_setting,
    get_settings
)
import sqlite3

def test_initialize_database(tmp_path):
    db_path = tmp_path / "test.db"

    initialize_database(db_path)

    assert db_path.exists()

    connection = sqlite3.connect(db_path)

    result = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name='records'
        """
    ).fetchone()

    assert result == ("records",)

    connection.close()

def test_add_record(tmp_path):
    db_path = tmp_path / "test.db"

    initialize_database(db_path)

    date_value = "2026-09-27"
    subject = "Python"
    minutes = 90

    add_record(date_value, subject, minutes, db_path)

    connection = sqlite3.connect(db_path)

    result = connection.execute(
        """
        SELECT date, subject, minutes
        FROM records
        """
    ).fetchone()

    assert result == ("2026-09-27", "Python", 90)

    connection.close()

def test_get_recorads(tmp_path):
    db_path = tmp_path / "test.db"

    initialize_database(db_path)

    add_record(
        "2026-09-27",
        "Python",
        90,
        db_path
    )

    add_record(
        "2026-09-28",
        "英語",
        45,
        db_path
    )

    result = get_records(db_path)

    records = [
        {
            "id": 1,
            "date": "2026-09-27",
            "subject": "Python",
            "minutes": 90
        },
        {
            "id": 2,
            "date": "2026-09-28",
            "subject": "英語",
            "minutes": 45
        }
    ]

    assert records == result

def test_update_record(tmp_path):
    db_path = tmp_path / "test.db"

    initialize_database(db_path)

    add_record(
        "2026-09-27",
        "Python",
        90,
        db_path
    )

    update_record(
        1,
        "2026-09-28",
        "英語",
        120,
        db_path
    )

    result = get_records(db_path)

    records = [
        {
            "id": 1,
            "date": "2026-09-28",
            "subject": "英語",
            "minutes": 120
        }
    ]

    assert result == records

def test_delete_record(tmp_path):
    db_path = tmp_path / "test.db"

    initialize_database(db_path)

    add_record(
        "2026-09-27",
        "Python",
        90,
        db_path
    )

    add_record(
        "2026-09-28",
        "英語",
        45,
        db_path
    )

    delete_record(
        1,
        db_path
    )

    result = get_records(db_path)

    records = [
        {
            "id": 2,
            "date": "2026-09-28",
            "subject": "英語",
            "minutes": 45
        }
    ]

    assert result == records

def test_initialize_database_creates_settings_table(tmp_path):
    db_path = tmp_path / "test.db"

    initialize_database(db_path)

    assert db_path.exists()

    connection = sqlite3.connect(db_path)

    sql = """
    SELECT name
    FROM sqlite_master
    WHERE type="table" AND name="settings"
    """

    result = connection.execute(sql).fetchone()

    assert result == ("settings",)

def test_save_setting(tmp_path):
    db_path = tmp_path / "test.db"

    initialize_database(db_path)

    save_setting("time_step", 1, db_path)
    save_setting("time_step", 5, db_path)

    connection = sqlite3.connect(db_path)

    sql = """
    SELECT value
    FROM settings
    WHERE key = ?
    """

    result = connection.execute(
        sql,
        ("time_step",)
    ).fetchone()

    assert result == ("5",)

    connection.close()

def test_get_settings(tmp_path):
    db_path = tmp_path / "test.db"

    initialize_database(db_path)

    save_setting("time_step", 5, db_path)
    save_setting("time_input_unit", "hours", db_path)

    result = get_settings(db_path)

    settings = {
        "time_step": 5,
        "time_input_unit": "hours"
    }

    assert result == settings

def test_get_settings_returns_defaults(tmp_path):
    db_path = tmp_path / "test.db"

    initialize_database(db_path)

    result = get_settings(db_path)

    settings = {
        "time_step": 1,
        "time_input_unit": "minutes"
    }

    assert result == settings