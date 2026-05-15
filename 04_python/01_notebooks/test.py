import pandas as pd
import numpy as np
import os
import chardet

# Check raw file content
file_path = r'C:\Users\NEHA NAGAR\Desktop\bank-full.csv'

# Read first 5 lines as raw text
with open(file_path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        print(f"Line {i+1}: {line}")
        if i >= 4:
            break


with open(file_path, 'rb') as f:
    result = chardet.detect(f.read(10000))
    print(f"Encoding: {result['encoding']}")
    print(f"Confidence: {result['confidence']}")


# Try different encodings
for encoding in ['utf-8', 'latin1',
                 'iso-8859-1', 'cp1252']:
    try:
        df = pd.read_csv(
            file_path,
            encoding=encoding,
            sep=';'
        )
        print(f"✅ Works with encoding: {encoding}")
        print(f"   Rows: {len(df):,}")
        print(f"   Cols: {len(df.columns)}")
        break
    except Exception as e:
        print(f"❌ Failed with {encoding}: {e}")