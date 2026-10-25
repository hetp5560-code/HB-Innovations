import sqlite3

DATABASE = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE, timeout=30)
    conn.row_factory = sqlite3.Row
    return conn