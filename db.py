import sqlite3

DB_NAME = "database.db"
SCHEMA_FILE = "schema.sql"


def setup():
    connection = sqlite3.connect(DB_NAME)
    with open(SCHEMA_FILE) as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()


def get_db_connection():
    conn = sqlite3.connect(
        DB_NAME, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    conn.row_factory = sqlite3.Row
    return conn


def get_all_records():
    conn = get_db_connection()
    records = conn.execute("SELECT * FROM records").fetchall()
    conn.close()
    return records


if __name__ == "__main__":
    setup()
