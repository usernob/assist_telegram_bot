import sqlite3

def make_table():
    connection = sqlite3.connect('main.db')
    connection.executescript('CREATE TABLE IF NOT EXISTS links (id INTEGER PRIMARY KEY AUTOINCREMENT,original_url TEXT NOT NULL, mime_type TEXT NOT NULL)')
    
    connection.commit()
    connection.close()

def get_db_connection():
    conn = sqlite3.connect('main.db')
    conn.row_factory = sqlite3.Row
    return conn

make_table()