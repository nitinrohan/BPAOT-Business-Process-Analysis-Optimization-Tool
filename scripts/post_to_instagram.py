import os
from instagrapi import Client
from dotenv import load_dotenv

# Load IG credentials
load_dotenv()
username = os.getenv("IG_USERNAME")
password = os.getenv("IG_PASSWORD")

# Image to post
image_path = "reports/word_freq_chart.png"
caption = "📊 Weekly BPAOT Insight\nTop 10 keywords from submitted requirements.\n#BPAOT #DataAnalysis #Automation"

# Login and post
try:
    cl = Client()
    cl.login(username, password)

    cl.photo_upload(
        path=image_path,
        caption=caption
    )
    print("✅ Instagram post published!")
except Exception as e:
    print(f"❌ Failed to post to Instagram: {e}")
