# exploration.py
# Day 2 — Understanding the Bank Marketing Dataset
# ─────────────────────────────────────────────────

import pandas as pd
import numpy as np
import os

import pandas as pd
import numpy as np
import os

print("📊 Loading Bank Marketing Dataset...")
print("=" * 50)

file_path = r'C:\Users\NEHA NAGAR\Desktop\bank-full.csv'

df = pd.read_csv(
    file_path,
    sep=',',
    encoding='utf-8-sig'
)

print(f"  ✅ Rows:    {len(df):,}")
print(f"  ✅ Columns: {len(df.columns)}")
print(f"\nColumns:")
for col in df.columns:
    print(f"  {col}")

print(f"  ✅ Rows:    {len(df):,}")
print(f"  ✅ Columns: {len(df.columns)}")

# ── Basic Info ─────────────────────────────────
print("\n📋 Column Information:")
print("-" * 50)
for col in df.columns:
    dtype    = df[col].dtype
    nulls    = df[col].isnull().sum()
    unique   = df[col].nunique()
    print(f"  {col:<15} | {str(dtype):<10} | "
          f"Nulls: {nulls:<5} | "
          f"Unique: {unique}")

# ── Target Variable Analysis ───────────────────
print("\n🎯 Target Variable (y) — Term Deposit:")
print("-" * 50)
target = df['y'].value_counts()
target_pct = df['y'].value_counts(normalize=True)*100
for val in target.index:
    print(f"  {val:<5} → {target[val]:>6,} customers "
          f"({target_pct[val]:.1f}%)")

# ── Numeric Columns Summary ────────────────────
print("\n📊 Numeric Columns Summary:")
print("-" * 50)
print(df.describe().round(2).to_string())

# ── Categorical Columns Summary ────────────────
print("\n📊 Categorical Columns:")
print("-" * 50)
cat_cols = df.select_dtypes(
    include='object').columns

for col in cat_cols:
    print(f"\n  {col.upper()}:")
    vals = df[col].value_counts()
    for v, c in vals.items():
        pct = c/len(df)*100
        print(f"    {str(v):<20} "
              f"{c:>6,} ({pct:.1f}%)")

# ── Key Business Metrics ───────────────────────
print("\n💰 Key Business Metrics:")
print("-" * 50)
print(f"  Avg Customer Balance: "
      f"${df['balance'].mean():,.2f}")
print(f"  Median Balance:       "
      f"${df['balance'].median():,.2f}")
print(f"  Customers in Default: "
      f"{(df['default']=='yes').sum():,} "
      f"({(df['default']=='yes').mean()*100:.1f}%)")
print(f"  Has Housing Loan:     "
      f"{(df['housing']=='yes').sum():,} "
      f"({(df['housing']=='yes').mean()*100:.1f}%)")
print(f"  Has Personal Loan:    "
      f"{(df['loan']=='yes').sum():,} "
      f"({(df['loan']=='yes').mean()*100:.1f}%)")
print(f"  Subscribed (y=yes):   "
      f"{(df['y']=='yes').sum():,} "
      f"({(df['y']=='yes').mean()*100:.1f}%)")

# ── Age Analysis ───────────────────────────────
print("\n👥 Age Distribution:")
print("-" * 50)
age_bins = [0,25,35,45,55,65,100]
age_labels = [
    'Under 25','25-34',
    '35-44','45-54',
    '55-64','65+'
]
df['Age_Group'] = pd.cut(
    df['age'],
    bins=age_bins,
    labels=age_labels
)
age_dist = df['Age_Group'].value_counts().sort_index()
for grp, cnt in age_dist.items():
    pct = cnt/len(df)*100
    print(f"  {grp:<12} "
          f"{cnt:>6,} ({pct:.1f}%)")

# ── Subscription Rate by Job ───────────────────
print("\n💼 Subscription Rate by Job:")
print("-" * 50)
job_sub = df.groupby('job')['y'].apply(
    lambda x: (x=='yes').mean()*100
).sort_values(ascending=False)

for job, rate in job_sub.items():
    print(f"  {job:<20} {rate:.1f}%")

# ── Balance by Education ───────────────────────
print("\n🎓 Average Balance by Education:")
print("-" * 50)
edu_bal = df.groupby('education')[
    'balance'].mean().sort_values(
    ascending=False)

for edu, bal in edu_bal.items():
    print(f"  {edu:<15} ${bal:,.2f}")

# ── Save Cleaned Preview ───────────────────────
print("\n💾 Saving data preview...")
# NEW — Save to Desktop
df.head(100).to_csv(
    r'C:\Users\NEHA NAGAR\Desktop\bank_preview.csv',
    index=False
)
print("  ✅ Preview saved: bank_preview.csv")

print("\n" + "=" * 50)
print("✅ Day 2 Exploration Complete!")
print(f"\n  Key Findings:")
print(f"  • Total Customers:    {len(df):,}")
print(f"  • Subscription Rate:  "
      f"{(df['y']=='yes').mean()*100:.1f}%")
print(f"  • Default Rate:       "
      f"{(df['default']=='yes').mean()*100:.1f}%")
print(f"  • Avg Balance:        "
      f"${df['balance'].mean():,.2f}")
print("=" * 50)