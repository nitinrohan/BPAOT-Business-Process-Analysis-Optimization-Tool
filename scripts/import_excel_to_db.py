import pandas as pd
import sqlite3
import os

EXCEL_FILE = "data/requirements.xlsx"
DB_FILE = "data/bpaot.db"

def import_excel_to_db():
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ Excel file not found at {EXCEL_FILE}")
        return

    if not os.path.exists(DB_FILE):
        print(f"❌ Database file not found at {DB_FILE}")
        return

    # Load Excel
    df = pd.read_excel(EXCEL_FILE)

    # Clean up column names to match DB schema
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Connect to DB and insert
    conn = sqlite3.connect(DB_FILE)
    df.to_sql("requirements", conn, if_exists="append", index=False)
    conn.close()

    print(f"✅ Imported {len(df)} rows from Excel to the database.")

if __name__ == "__main__":
    import_excel_to_db()
