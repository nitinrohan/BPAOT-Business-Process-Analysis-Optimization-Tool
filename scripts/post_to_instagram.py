import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from instagrapi import Client

# Load Instagram credentials
load_dotenv()
username = os.getenv("IG_USERNAME")
password = os.getenv("IG_PASSWORD")

# Connect to the database
conn = sqlite3.connect("data/bpaot.db")
df = pd.read_sql("SELECT * FROM requirements", conn)
conn.close()

# Process top keywords from 'requirement' column
keywords = " ".join(df["requirement"].dropna().str.lower().tolist()).split()
top_words = pd.Series(keywords).value_counts().head(3).index.tolist()
top_keywords = ", ".join(top_words)

# Dynamic caption using top keywords
caption = f"📊 BPAOT Weekly Insight\nTop trending keywords: {top_keywords}\n#automation #BPAOT #data"

# Path to chart image
image_path = "reports/word_freq_chart.png"

# Instagram upload
try:
    cl = Client()
    cl.login(username, password)
    cl.photo_upload(path=image_path, caption=caption)
    print("✅ Instagram post published!")
except Exception as e:
    print(f"❌ Failed to post to Instagram: {e}")
