import sqlite3

# Connect to SQLite (creates file if not exists)
conn = sqlite3.connect("data/bpaot.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS requirements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    requirement TEXT NOT NULL,
    pain_point TEXT NOT NULL,
    proposed_solution TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("✅ Database initialized: data/bpaot.db")
