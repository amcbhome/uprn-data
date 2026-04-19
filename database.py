import sqlite3

DB_PATH = "data.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS collections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uprn TEXT,
        date TEXT,
        type TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_collections(uprn, events):
    conn = get_connection()
    cursor = conn.cursor()

    for event in events:
        cursor.execute("""
        INSERT INTO collections (uprn, date, type)
        VALUES (?, ?, ?)
        """, (uprn, event["date"], event["type"]))

    conn.commit()
    conn.close()


def get_upcoming_collections(uprn, limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"""
    SELECT date, type
    FROM collections
    WHERE uprn = ?
      AND date(date) >= date('now')
    ORDER BY date ASC
    LIMIT {int(limit)}
    """

    cursor.execute(query, (uprn,))
    rows = cursor.fetchall()
    conn.close()

    return rows
