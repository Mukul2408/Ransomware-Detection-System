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
def get_dates():
    conn = connect()
    rows = conn.execute("SELECT DISTINCT substr(time, 1, 10) FROM events ORDER BY time DESC").fetchall()
    conn.close()
    return [r[0] for r in rows if r[0]]
def get_events_by_date(date_str):
    conn = connect()
    rows = conn.execute("SELECT file, risk_score, status, time FROM events WHERE time LIKE ? ORDER BY id DESC", (f"{date_str}%",),).fetchall()
    conn.close()
    return rows
def clear_events():
    conn = connect()
    conn.execute("DELETE FROM events")
    conn.commit()
    conn.close()
init_db()
 
