import sqlite3

connection = sqlite3.connect("cases.db")
connection.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        error TEXT NOT NULL
    )
""")
print("cases 表已就绪")
connection.close()