# 04_rfm_segmentation.py
# RFM Customer Segmentation Analysis
# ─────────────────────────────────────────────
#
# RFM = Recency + Frequency + Monetary
#
# We score each customer 1-5 on each dimension:
# 5 = Best, 1 = Worst
#
# Then combine scores to create segments like:
# Champions, Loyal, At Risk, Lost etc.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ── Setup ──────────────────────────────────────
BASE_PATH = (r'C:\Users\Neha Nagar\Desktop\bank_analytics')
DATA_PATH = os.path.join(
    BASE_PATH, '01_data', 'cleaned')
CHARTS_DIR = os.path.join(
    BASE_PATH, '05_outputs', 'charts')
os.makedirs(CHARTS_DIR, exist_ok=True)

sns.set_theme(style='whitegrid')

print("🎯 RFM Customer Segmentation Analysis")
print("=" * 50)
print("  R = Recency   (how recently contacted)")
print("  F = Frequency (how often contacted)")
print("  M = Monetary  (account balance)")
print("=" * 50)


# ── Section 2: Load Data ───────────────────────
print("\n📦 Step 1: Loading data...")

df = pd.read_csv(
    os.path.join(DATA_PATH,
                 'Bank_Customers.csv')
)

# Standardize text
text_cols = ['y', 'Job_Title', 'Marital_Status',
             'Education', 'poutcome']
for col in text_cols:
    if col in df.columns:
        df[col] = df[col].str.lower().str.strip()

df['Sub_Num'] = (df['y'] == 'yes').astype(int)

print(f" ✅ Loaded {len(df):,} customers")

# ── Section 3: Calculate RFM Values ───────────
print("\n📊 Step 2: Calculating RFM values...")

# ── RECENCY ────────────────────────────────────
# pdays = days since last contact
# -1 means never contacted before
# Lower pdays = more recent = BETTER
# We convert -1 to 999 (very old/never)

df['Recency'] = df['pdays'].apply(
    lambda x: 999 if x == -1 else x
)

print(f"  Recency:")
print(f"    Never contacted: "
      f"{(df['pdays']==-1).sum():,} customers")
print(f"    Avg days since contact: "
      f"{df[df['pdays']>0]['pdays'].mean():.0f} days")

# ── FREQUENCY ──────────────────────────────────
# Total contacts = campaign + previous
# Higher frequency = more engaged = BETTER

df['Frequency'] = df['Campaign'] + df['previous']

print(f"\n  Frequency:")
print(f"    Avg total contacts: "
      f"{df['Frequency'].mean():.1f}")
print(f"    Max contacts: "
      f"{df['Frequency'].max()}")

# ── MONETARY ───────────────────────────────────
# Balance = account balance
# Higher balance = more valuable = BETTER
# Handle negative balances

df['Monetary'] = df['Balance'].clip(lower=0)

print(f"\n  Monetary:")
print(f"    Avg balance: "
      f"${df['Monetary'].mean():,.2f}")
print(f"    Max balance: "
      f"${df['Monetary'].max():,.2f}")
print(f"    Zero/Negative: "
      f"{(df['Balance']<=0).sum():,} customers")


# ── Section 4: Score Customers 1-5 ────────────
print("\n📊 Step 3: Scoring customers 1-5...")
print("  (5 = Best, 1 = Worst)")

# We use QUINTILES to divide customers
# into 5 equal groups

# ── RECENCY SCORE ──────────────────────────────
# Lower recency = more recent = BETTER score
# So we REVERSE the scoring
# (lower days = higher score)
# NEW — handles NaN values safely
def safe_qcut(series, labels, reverse=False):
    """
    Safely cut a series into quintiles
    handling duplicates and NaN values
    """
    try:
        result = pd.qcut(
            series,
            q=5,
            labels=labels,
            duplicates='drop'
        )
    except Exception:
        result = pd.cut(
            series,
            bins=5,
            labels=labels,
            duplicates='drop'
        )
    # Fill any NaN with middle score (3)
    result = result.fillna(3)
    return result.astype(int)

# Recency Score (reversed — lower = better)
df['R_Score'] = safe_qcut(
    df['Recency'],
    labels=[5, 4, 3, 2, 1],
    reverse=True
)

# Frequency Score
df['F_Score'] = safe_qcut(
    df['Frequency'].rank(method='first'),
    labels=[1, 2, 3, 4, 5]
)

# Monetary Score
df['M_Score'] = safe_qcut(
    df['Monetary'].rank(method='first'),
    labels=[1, 2, 3, 4, 5]
)

print(f"  ✅ R Score range: "
      f"{df['R_Score'].min()} - "
      f"{df['R_Score'].max()}")
print(f"  ✅ F Score range: "
      f"{df['F_Score'].min()} - "
      f"{df['F_Score'].max()}")
print(f"  ✅ M Score range: "
      f"{df['M_Score'].min()} - "
      f"{df['M_Score'].max()}")

# ── COMBINED RFM SCORE ─────────────────────────
# Concatenate R+F+M scores into one string
# e.g. R=5, F=4, M=3 → '543'
df['RFM_Score'] = (
    df['R_Score'].astype(str) +
    df['F_Score'].astype(str) +
    df['M_Score'].astype(str)
)

# Overall score (average)
df['RFM_Total'] = (
    df['R_Score'] +
    df['F_Score'] +
    df['M_Score']
) / 3

print(f"  ✅ R Score range: "
      f"{df['R_Score'].min()} - "
      f"{df['R_Score'].max()}")
print(f"  ✅ F Score range: "
      f"{df['F_Score'].min()} - "
      f"{df['F_Score'].max()}")
print(f"  ✅ M Score range: "
      f"{df['M_Score'].min()} - "
      f"{df['M_Score'].max()}")
print(f"  ✅ RFM Total range: "
      f"{df['RFM_Total'].min():.1f} - "
      f"{df['RFM_Total'].max():.1f}")

# ── Section 5: Create Segments ─────────────────
print("\n📊 Step 4: Creating customer segments...")

def assign_segment(row):
    r = row['R_Score']
    f = row['F_Score']
    m = row['M_Score']
    total = row['RFM_Total']

    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'
    elif r >= 3 and f >= 3 and m >= 4:
        return 'Loyal Customers'
    elif r >= 4 and f <= 2:
        return 'Recent Customers'
    elif r >= 3 and f >= 3 and m >= 3:
        return 'Potential Loyalists'
    elif r >= 4 and f >= 3 and m >= 3:
        return 'Promising'
    elif r >= 3 and f <= 2 and m >= 3:
        return 'Need Attention'
    elif r <= 2 and f >= 3 and m >= 3:
        return 'At Risk'
    elif r <= 2 and f >= 4 and m >= 4:
        return 'Cannot Lose Them'
    elif r <= 2 and f <= 2 and m >= 3:
        return 'Hibernating'
    else:
        return 'Lost'

df['Segment'] = df.apply(
    assign_segment, axis=1)

# Segment summary
segment_summary = df.groupby('Segment').agg(
    Customer_Count  = ('Sub_Num', 'count'),
    Avg_Balance     = ('Balance', 'mean'),
    Avg_RFM         = ('RFM_Total', 'mean'),
    Subscribed      = ('Sub_Num', 'sum'),
    Avg_R           = ('R_Score', 'mean'),
    Avg_F           = ('F_Score', 'mean'),
    Avg_M           = ('M_Score', 'mean')
).reset_index()

segment_summary['Sub_Rate'] = (
    segment_summary['Subscribed'] /
    segment_summary['Customer_Count'] * 100
).round(2)

segment_summary['Avg_Balance'] = \
    segment_summary['Avg_Balance'].round(2)
segment_summary['Avg_RFM'] = \
    segment_summary['Avg_RFM'].round(2)

segment_summary = segment_summary.sort_values(
    'Avg_RFM', ascending=False)

print(f"\n  Customer Segments:")
print(f"  {'Segment':<22} {'Count':>7} "
      f"{'Avg Balance':>12} "
      f"{'Sub Rate':>10}")
print(f"  {'-'*55}")

for _, row in segment_summary.iterrows():
    print(f"  {row['Segment']:<22} "
          f"{row['Customer_Count']:>7,} "
          f"${row['Avg_Balance']:>11,.2f} "
          f"{row['Sub_Rate']:>9.1f}%")



# ── Section 6: Charts ──────────────────────────
print("\n📊 Generating RFM charts...")

# ── Chart 16: Segment Distribution ────────────
colors_seg = {
    'Champions':         '#4CAF50',
    'Loyal Customers':   '#2196F3',
    'Potential Loyalists':'#03A9F4',
    'Promising':         '#00BCD4',
    'Recent Customers':  '#8BC34A',
    'Need Attention':    '#FF9800',
    'At Risk':           '#FF5722',
    'Cannot Lose Them':  '#F44336',
    'Hibernating':       '#9E9E9E',
    'Lost':              '#607D8B'
}

seg_counts = segment_summary.set_index('Segment')['Customer_Count']

plt.figure(figsize=(12, 7))
bars = plt.barh(
    seg_counts.index,
    seg_counts.values,
    color=[colors_seg.get(s, '#9E9E9E')
           for s in seg_counts.index]
)
plt.xlabel('Number of Customers')
plt.title(
    'Customer Distribution by RFM Segment',
    fontsize=14, fontweight='bold'
)
for bar, val in zip(bars, seg_counts.values):
    pct = val/len(df)*100
    plt.text(
        bar.get_width() + 50,
        bar.get_y() + bar.get_height()/2,
        f'{val:,} ({pct:.1f}%)',
        va='center', fontsize=10
    )
plt.tight_layout()
plt.savefig(os.path.join(
    CHARTS_DIR,
    '16_rfm_segments.png'),
    dpi=150)
plt.show()
print("  ✅ Chart 16 saved: rfm_segments.png")

# ── Chart 17: Subscription Rate by Segment ────
seg_sub = segment_summary.sort_values(
    'Sub_Rate', ascending=True)

plt.figure(figsize=(12, 7))
bars = plt.barh(
    seg_sub['Segment'],
    seg_sub['Sub_Rate'],
    color=[colors_seg.get(s, '#9E9E9E')
           for s in seg_sub['Segment']]
)
plt.axvline(
    x=df['Sub_Num'].mean()*100,
    color='red',
    linestyle='--',
    linewidth=2,
    label=f'Overall Rate: '
          f'{df["Sub_Num"].mean()*100:.1f}%'
)
plt.xlabel('Subscription Rate (%)')
plt.title(
    'Subscription Rate by Customer Segment',
    fontsize=14, fontweight='bold'
)
plt.legend()
for bar, val in zip(
    bars, seg_sub['Sub_Rate']
):
    plt.text(
        bar.get_width() + 0.3,
        bar.get_y() + bar.get_height()/2,
        f'{val:.1f}%',
        va='center', fontsize=10
    )
plt.tight_layout()
plt.savefig(os.path.join(
    CHARTS_DIR,
    '17_segment_subscription.png'),
    dpi=150)
plt.show()
print("  ✅ Chart 17 saved: "
      "segment_subscription.png")

# ── Chart 18: RFM Heatmap ─────────────────────
rfm_pivot = df.pivot_table(
    values='Sub_Num',
    index='R_Score',
    columns='M_Score',
    aggfunc='mean'
) * 100

plt.figure(figsize=(10, 8))
sns.heatmap(
    rfm_pivot,
    annot=True,
    fmt='.1f',
    cmap='RdYlGn',
    linewidths=0.5,
    cbar_kws={
        'label': 'Subscription Rate (%)'
    }
)
plt.title(
    'Subscription Rate Heatmap\n'
    'Recency Score vs Monetary Score',
    fontsize=14, fontweight='bold'
)
plt.xlabel('Monetary Score (Balance)')
plt.ylabel('Recency Score (Recent Contact)')
plt.tight_layout()
plt.savefig(os.path.join(
    CHARTS_DIR,
    '18_rfm_heatmap.png'),
    dpi=150)
plt.show()
print("  ✅ Chart 18 saved: rfm_heatmap.png")

# ── Chart 19: Avg Balance by Segment ──────────
seg_bal = segment_summary.sort_values(
    'Avg_Balance', ascending=True)

plt.figure(figsize=(12, 7))
bars = plt.barh(
    seg_bal['Segment'],
    seg_bal['Avg_Balance'],
    color=[colors_seg.get(s, '#9E9E9E')
           for s in seg_bal['Segment']]
)
plt.xlabel('Average Balance ($)')
plt.title(
    'Average Account Balance by Segment',
    fontsize=14, fontweight='bold'
)
for bar, val in zip(
    bars, seg_bal['Avg_Balance']
):
    plt.text(
        bar.get_width() + 10,
        bar.get_y() + bar.get_height()/2,
        f'${val:,.0f}',
        va='center', fontsize=10
    )
plt.tight_layout()
plt.savefig(os.path.join(
    CHARTS_DIR,
    '19_segment_balance.png'),
    dpi=150)
plt.show()
print("  ✅ Chart 19 saved: segment_balance.png")

# ── Section 7: Export Results ──────────────────
print("\n💾 Step 5: Exporting results...")

# Export full RFM data
rfm_export = df[[
    'Age', 'Job_Title', 'Marital_Status',
    'Education', 'Balance',
    'Recency', 'Frequency', 'Monetary',
    'R_Score', 'F_Score', 'M_Score',
    'RFM_Score', 'RFM_Total',
    'Segment', 'Sub_Num', 'y'
]].copy()

rfm_export.to_csv(
    os.path.join(
        BASE_PATH,
        '05_outputs',
        'rfm_segments.csv'
    ),
    index=False
)
print("  ✅ Exported: rfm_segments.csv")

# Export segment summary
segment_summary.to_csv(
    os.path.join(
        BASE_PATH,
        '05_outputs',
        'rfm_summary.csv'
    ),
    index=False
)
print("  ✅ Exported: rfm_summary.csv")

# ── Summary ────────────────────────────────────
print("\n" + "=" * 50)
print("✅ RFM Segmentation Complete!")
print(f"\n  👥 Customer Segments Found: "
      f"{df['Segment'].nunique()}")
print(f"\n  🏆 Top Segments by Sub Rate:")

top_segs = segment_summary.nlargest(
    3, 'Sub_Rate')
for _, row in top_segs.iterrows():
    print(f"  • {row['Segment']:<22} "
          f"{row['Sub_Rate']:.1f}% "
          f"subscription rate")

print(f"\n  💰 Highest Value Segment:")
rich_seg = segment_summary.nlargest(
    1, 'Avg_Balance').iloc[0]
print(f"  • {rich_seg['Segment']}: "
      f"${rich_seg['Avg_Balance']:,.2f} "
      f"avg balance")

print(f"\n  📁 Files saved:")
print(f"  • charts/16_rfm_segments.png")
print(f"  • charts/17_segment_subscription.png")
print(f"  • charts/18_rfm_heatmap.png")
print(f"  • charts/19_segment_balance.png")
print(f"  • outputs/rfm_segments.csv")
print(f"  • outputs/rfm_summary.csv")
print("=" * 50)