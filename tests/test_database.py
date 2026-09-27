from database import initialize_database
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