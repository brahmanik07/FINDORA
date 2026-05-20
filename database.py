import sqlite3

conn = sqlite3.connect("database.db")

conn.execute('''
CREATE TABLE users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
phone TEXT,
email TEXT,
password TEXT
)
''')

conn.execute('''
CREATE TABLE items (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
description TEXT,
type TEXT
)
''')

conn.commit()
conn.close()