import os
import sqlite3

# Ensure the data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Using context manager for database connection
def get_upcoming_collections(limit=10):
    with sqlite3.connect('data/collections.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM collections WHERE date > CURRENT_DATE ORDER BY date ASC LIMIT ?", (limit,))
        return cursor.fetchall()