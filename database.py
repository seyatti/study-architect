import sqlite3
from contextlib import closing

def initialize_database(db_path="data/study_architect.db"):

    with closing(sqlite3.connect(db_path)) as connection:
        with connection:

            records_sql = """
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                subject TEXT NOT NULL,
                minutes INTEGER NOT NULL
            )
            """

            settings_sql = """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL  
            )
            """

            goal_sql = """
            CREATE TABLE IF NOT EXISTS goal (
                id INTEGER PRIMARY KEY,
                target_minutes INTEGER NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL
            )
            """

            connection.execute(records_sql)
            connection.execute(settings_sql)
            connection.execute(goal_sql)

def add_record(date, subject, minutes, db_path="data/study_architect.db"):

    with closing(sqlite3.connect(db_path)) as connection:
        with connection:
            
            sql = """
            INSERT INTO records (date, subject, minutes)
            VALUES (?, ?, ?)    
            """

            connection.execute(
                sql,
                (date, subject, minutes)
            )

def get_records(db_path="data/study_architect.db"):

    with closing(sqlite3.connect(db_path)) as connection:

        sql = """
        SELECT id, date, subject, minutes
        FROM records
        ORDER BY id
        """

        rows = connection.execute(sql).fetchall()

    records = []

    for row in rows:
        record = {
            "id": row[0],
            "date": row[1],
            "subject": row[2],
            "minutes": row[3]
        }
        records.append(record)

    return records

def update_record(
        record_id,
        date,
        subject,
        minutes,
        db_path="data/study_architect.db",
):

    with closing(sqlite3.connect(db_path)) as connection:
        with connection:

            sql = """
            UPDATE records
            SET date = ?, subject = ?, minutes = ?
            WHERE id = ?
            """

            connection.execute(
                sql,
                (date, subject, minutes, record_id)
            )

def delete_record(
        record_id,
        db_path="data/study_architect.db"
):
    with closing(sqlite3.connect(db_path)) as connection:
        with connection: 

            sql = """
            DELETE FROM records
            WHERE id = ?
            """

            connection.execute(
                sql,
                (record_id,)
            )

def save_setting(
        key,
        value,
        db_path="data/study_architect.db"
):
    with closing(sqlite3.connect(db_path)) as connection:
        with connection:

            sql = """
            INSERT INTO settings (key, value)
            VALUES (?, ?)
            ON CONFLICT(key)
            DO UPDATE SET value = excluded.value
            """

            connection.execute(
                sql,
                (key, str(value))
            )

def get_settings(db_path="data/study_architect.db"):

    with closing(sqlite3.connect(db_path)) as connection:

        settings = {
            "time_step": 1,
            "time_input_unit": "minutes"
        }

        sql = """
        SELECT key, value
        FROM settings
        """

        rows = connection.execute(
            sql
        ).fetchall()

        for key, value in rows:
            if key == "time_step":
                settings[key] = int(value)
            else:
                settings[key] = value

    return settings

def save_goal(
        target_minutes,
        start_date,
        end_date,
        db_path="data/study_architect.db"
        ):

    with closing(sqlite3.connect(db_path)) as connection:
        with connection:

            sql = """
            INSERT INTO goal(
                id,
                target_minutes,
                start_date,
                end_date
            )
            VALUES (
                1,
                ?,
                ?,
                ?
            )
            ON CONFLICT(id) DO UPDATE SET
                target_minutes = excluded.target_minutes,
                start_date = excluded.start_date,
                end_date = excluded.end_date
            """

            connection.execute(
                sql,
                (
                    target_minutes,
                    start_date,
                    end_date
                )
            )

def get_goal(db_path="data/study_architect.db"):

    with closing(sqlite3.connect(db_path)) as connection:

        sql = """
        SELECT
            target_minutes,
            start_date,
            end_date
        FROM goal
        WHERE id = 1
        """

        cursor = connection.execute(sql)
        cursor_f = cursor.fetchone()
        if cursor_f is None:
            goal = None
        else:
            goal = {
                "target_minutes": cursor_f[0],
                "start_date": cursor_f[1],
                "end_date": cursor_f[2]
            }

    return goal