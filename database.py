import sqlite3

def initialize_database(db_path="data/study_architect.db"):
    connection = sqlite3.connect(db_path)

    sql = """
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        subject TEXT NOT NULL,
        minutes INTEGER NOT NULL
    )
    """

    connection.execute(sql)

    connection.commit()
    connection.close()

def add_record(date, subject, minutes, db_path="data/study_architect.db"):
    connection = sqlite3.connect(db_path)

    sql = """
    INSERT INTO records (date, subject, minutes)
    VALUES (?, ?, ?)    
    """

    connection.execute(
        sql,
        (date, subject, minutes)
    )

    connection.commit()
    connection.close()

def get_records(db_path="data/study_architect.db"):
    connection = sqlite3.connect(db_path)

    sql = """
    SELECT id, date, subject, minutes
    FROM records
    ORDER BY id
    """

    rows = connection.execute(sql).fetchall()

    connection.close()

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
    connection = sqlite3.connect(db_path)

    sql = """
    UPDATE records
    SET date = ?, subject = ?, minutes = ?
    WHERE id = ?
    """

    connection.execute(
        sql,
        (date, subject, minutes, record_id)
    )

    connection.commit()
    connection.close()

def delete_record(
        record_id,
        db_path="data/study_architect.db"
):
    connection = sqlite3.connect(db_path)

    sql = """
    DELETE FROM records
    WHERE id = ?
    """

    connection.execute(
        sql,
        (record_id,)
    )

    connection.commit()
    connection.close()