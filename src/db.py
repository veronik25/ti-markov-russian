from pathlib import Path
import sqlite3

DB_PATH = Path("data") / "frequencies.sqlite3"

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True, parents=True)
    return sqlite3.connect(DB_PATH)

def init_schema():
    conn = get_connection()
    cur = conn.cursor()
    cur.executescript("""
    DROP TABLE IF EXISTS freq_overall;
    DROP TABLE IF EXISTS freq_conditional;

    CREATE TABLE freq_overall (
        symbol TEXT NOT NULL,
        count INTEGER NOT NULL,
        probability REAL NOT NULL,
        PRIMARY KEY (symbol)
    );

    CREATE TABLE freq_conditional (
        order_n INTEGER NOT NULL,
        context TEXT NOT NULL,
        symbol TEXT NOT NULL,
        count INTEGER NOT NULL,
        probability REAL NOT NULL,
        PRIMARY KEY (order_n, context, symbol)
    );
    """)
    conn.commit()
    conn.close()
