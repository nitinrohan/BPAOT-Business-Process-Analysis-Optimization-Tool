import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

# 1. Load Data
conn = sqlite3.connect("data/bpaot.db")
df = pd.read_sql("SELECT * FROM requirements", conn)
conn.close()

# 2. Generate Word Frequency Chart
all_words = " ".join(df["requirement"].dropna()).lower().split()
freq = pd.Series(all_words).value_counts().head(10)

plt.figure(figsize=(8, 4))
freq.plot(kind='bar', color='skyblue')
plt.title("Top 10 Words in Requirements")
plt.tight_layout()
chart_path = "reports/word_freq_chart.png"
plt.savefig(chart_path)
plt.close()

# 3. Render HTML Template
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("report_template.html")
html_out = template.render(
    total=len(df),
    chart_path=chart_path,
    data=df.to_dict(orient="records")
)

# 4. Generate PDF Report
pdf_path = "reports/bpaot_report.pdf"
HTML(string=html_out, base_url=".").write_pdf(pdf_path)

print(f"✅ Report generated at: {pdf_path}")
