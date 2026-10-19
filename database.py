import sqlite3
from datetime import datetime
DB_NAME = "detection.db" 
def connect():
    return sqlite3.connect(DB_NAME)
def init_db():
    conn = connect()
    conn.execute("""CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file TEXT,
        risk_score INTEGER,
        status TEXT,
        time TEXT)""")
    conn.commit()
    conn.close()
def log_event(file, risk_score, status):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    conn.execute("INSERT INTO events (file, risk_score, status, time) VALUES (?, ?, ?, ?)",
                 (file, risk_score, status, now))
    conn.commit()
    conn.close()
def get_recent_events(limit=50):
    conn = connect()
    rows = conn.execute("SELECT file, risk_score, status, time FROM events "
                        "ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return rows
def clear_events():
    conn = connect()
    conn.execute("DELETE FROM events")
    conn.commit()
    conn.close()
init_db()
 
