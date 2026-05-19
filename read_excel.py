import pandas as pd
import sys

file_path = r"c:\Users\controlss\Downloads\Livestream data 2026-04-21 - 2026-04-21 - Campaign 1862954693922098.xlsx"

try:
    df = pd.read_excel(file_path)
    print("Columns:")
    print(df.columns.tolist())
    print("\nFirst 5 rows:")
    print(df.head())
except Exception as e:
    print("Error reading excel:", e)
