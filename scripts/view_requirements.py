import pandas as pd
import os

def view_excel(path="data/requirements.xlsx"):
    if os.path.exists(path):
        df = pd.read_excel(path)
        print("\n📄 Current Requirements:\n")
        print(df)
    else:
        print(f"\n❌ No file found at {path}")

if __name__ == "__main__":
    view_excel()
