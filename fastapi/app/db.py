import sqlite3
from contextlib import contextmanager
from .config import DB_PATH

@contextmanager
def get_connection():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"SQLite database not found: {DB_PATH}")
    conn=sqlite3.connect(str(DB_PATH))
    conn.row_factory=sqlite3.Row
    try: yield conn
    finally: conn.close()

def fetch_all(sql,params=()):
    with get_connection() as c: return [dict(r) for r in c.execute(sql,params).fetchall()]
def fetch_one(sql,params=()):
    with get_connection() as c:
        r=c.execute(sql,params).fetchone()
        return dict(r) if r else None
