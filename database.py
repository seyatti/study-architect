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