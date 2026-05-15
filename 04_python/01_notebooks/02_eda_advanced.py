# 02_eda_advanced.py
# Bank Customer Analytics — Advanced EDA
# ─────────────────────────────────────────────

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import squarify
import os

# ── Setup ─────────────────────────────────────
BASE_PATH = r'C:\Users\NEHA NAGAR\Desktop\bank_analytics'
DATA_PATH = os.path.join(BASE_PATH, '01_data', 'cleaned')
CHARTS_DIR = os.path.join(BASE_PATH, '05_outputs', 'charts')
os.makedirs(CHARTS_DIR, exist_ok=True)

sns.set_theme(style='whitegrid')
print("📊 Starting Advanced EDA...")
print("=" * 50)

# ── Load and Prepare Data ──────────────────────
df = pd.read_csv(
    os.path.join(DATA_PATH, 'Bank_Customers.csv'))

# Standardize columns
# NEW — comprehensive standardization
print("\n🔧 Standardizing columns...")

# Check actual column names
print(f"  Columns: {list(df.columns)}")

# Standardize ALL text columns to lowercase
text_cols = [
    'y', 'Job_Title', 'Marital_Status', 'Education',
    'Housing', 'Loan', 'Contact',
    'Month', 'poutcome'
]
for col in text_cols:
    if col in df.columns:
        df[col] = df[col].str.lower().str.strip()

# Handle default column name
if 'default' in df.columns:
    df['default_status'] = (
        df['default'].str.lower().str.strip()
    )
elif 'default_status' in df.columns:
    df['default_status'] = (
        df['default_status'].str.lower().str.strip()
    )

# Recreate Sub_Num
df['Sub_Num'] = (df['y'] == 'yes').astype(int)

# Verify everything
print(f"  y unique values:       {df['y'].unique()}")
print(f"  Sub_Num unique:        {df['Sub_Num'].unique()}")
print(f"  Subscription Rate:     "
      f"{df['Sub_Num'].mean()*100:.1f}%")
print(f"  Education unique:      "
      f"{df['Education'].unique()}")
print(f"  poutcome unique:       "
      f"{df['poutcome'].unique()}")
print(f"  default_status unique: "
      f"{df['default_status'].unique()}")

df['Age_Group'] = pd.cut(
    df['Age'],
    bins=[0, 25, 35, 45, 55, 65, 100],
    labels=[
        'Under 25', '25-34', '35-44',
        '45-54',    '55-64', '65+'
    ]
)

month_map = {
    'January':1,   'February':2,  'March':3,
    'April':4,     'May':5,       'June':6,
    'July':7,      'August':8,    'September':9,
    'October':10,  'November':11, 'December':12
}
df['Month_Num'] = df['Month'].map(month_map)

df['Call_Duration_Group'] = pd.cut(df['Duration'], bins=[0, 60, 180, 300, 600, float('inf')], labels=['Under 1 min', '1-3 mins',
                                                                                                      '3-5 mins',    '5-10 mins',
                                                                                                      'Over 10 mins'])
print(f"  ✅ Loaded {len(df):,} rows")
print(f"  ✅ All columns prepared")

# ── CRITICAL DEBUG ─────────────────────────────
print("\n🔍 Critical Debug Check:")
print(f"  Sub_Num sum:    {df['Sub_Num'].sum()}")
print(f"  Sub_Num mean:   {df['Sub_Num'].mean():.4f}")
print(f"  y value counts: {df['y'].value_counts().to_dict()}")
print(f"  Sample y values:{df['y'].head(10).tolist()}")
print(f"  Sub_Num sample: {df['Sub_Num'].head(10).tolist()}")

# Test groupby manually
test = df.groupby('Education').agg(
    Total      = ('Sub_Num', 'count'),
    Subscribed = ('Sub_Num', 'sum')
).reset_index()
test['Rate'] = test['Subscribed'] / test['Total'] * 100
print(f"\n  Education test:")
print(test[['Education','Total',
            'Subscribed','Rate']].to_string())


# ── Chart 9: Education vs Balance vs Sub ───────
print("\n📊 Generating advanced charts...")

edu_analysis = df.groupby('Education').agg(
    Total       = ('Sub_Num', 'count'),
    Subscribed  = ('Sub_Num', 'sum'),
    Avg_Balance = ('Balance', 'mean')).reset_index()

edu_analysis['Sub_Rate'] = (edu_analysis['Subscribed'] /edu_analysis['Total'] * 100).round(2)

# NEW — use actual values from data
edu_order = sorted( df['Education'].unique().tolist() )
print(f"  Education values: {edu_order}")

edu_analysis['Education'] = pd.Categorical(
    edu_analysis['Education'],
    categories=edu_order,
    ordered=True
)
edu_analysis = edu_analysis.sort_values('Education')

fig, ax1 = plt.subplots(figsize=(12, 6))

x = np.arange(len(edu_analysis))
width = 0.35

bars1 = ax1.bar(
    x - width/2,
    edu_analysis['Avg_Balance'],
    width,
    color='#2196F3',
    alpha=0.8,
    label='Avg Balance ($)'
)
ax1.set_xlabel('Education Level')
ax1.set_ylabel(
    'Average Balance ($)',
    color='#2196F3'
)
ax1.tick_params(
    axis='y', labelcolor='#2196F3')
ax1.set_xticks(x)
ax1.set_xticklabels(
    edu_analysis['Education'])

ax2 = ax1.twinx()
bars2 = ax2.bar(
    x + width/2,
    edu_analysis['Sub_Rate'],
    width,
    color='#FF9800',
    alpha=0.8,
    label='Subscription Rate (%)'
)
ax2.set_ylabel(
    'Subscription Rate (%)',
    color='#FF9800'
)
ax2.tick_params(
    axis='y', labelcolor='#FF9800')

# Add value labels
for bar in bars1:
    ax1.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + 20,
        f'${bar.get_height():,.0f}',
        ha='center', fontsize=9,
        color='#2196F3'
    )
for bar in bars2:
    ax2.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + 0.2,
        f'{bar.get_height():.1f}%',
        ha='center', fontsize=9,
        color='#FF9800'
    )

plt.title(
    'Education Level vs Balance '
    'and Subscription Rate',
    fontsize=14, fontweight='bold'
)
fig.legend(
    loc='upper left',
    bbox_to_anchor=(0.1, 0.9)
)
plt.tight_layout()
plt.savefig(os.path.join(
    CHARTS_DIR,
    '09_education_analysis.png'),
    dpi=150)
plt.show()
print("  ✅ Chart 9 saved: "
      "education_analysis.png")

# ── Chart 10: Call Duration Impact ─────────────
duration_analysis = df.groupby('Call_Duration_Group',
    observed=True
).agg(
    Total      = ('Sub_Num', 'count'),
    Subscribed = ('Sub_Num', 'sum')
).reset_index()

duration_analysis['Sub_Rate'] = (
    duration_analysis['Subscribed'] /
    duration_analysis['Total'] * 100
).round(2)

colors_duration = [
    '#F44336', '#FF9800',
    '#FFC107', '#4CAF50', '#2196F3'
]

fig, axes = plt.subplots(
    1, 2, figsize=(14, 6))

# Bar chart
axes[0].bar(
    duration_analysis[
        'Call_Duration_Group'],
    duration_analysis['Sub_Rate'],
    color=colors_duration
)
axes[0].set_xlabel('Call Duration')
axes[0].set_ylabel(
    'Subscription Rate (%)')
axes[0].set_title(
    'Subscription Rate by Call Duration',
    fontsize=13, fontweight='bold'
)
axes[0].tick_params(
    axis='x', rotation=30)

for i, (bar, val) in enumerate(zip(
    axes[0].patches,
    duration_analysis['Sub_Rate']
)):
    axes[0].text(
        bar.get_x() +
        bar.get_width()/2,
        bar.get_height() + 0.3,
        f'{val:.1f}%',
        ha='center', fontsize=10,
        fontweight='bold'
    )

# Volume chart
axes[1].bar(
    duration_analysis[
        'Call_Duration_Group'],
    duration_analysis['Total'],
    color=colors_duration,
    alpha=0.7
)
axes[1].set_xlabel('Call Duration')
axes[1].set_ylabel(
    'Number of Calls')
axes[1].set_title(
    'Call Volume by Duration',
    fontsize=13, fontweight='bold'
)
axes[1].tick_params(
    axis='x', rotation=30)

for bar, val in zip(
    axes[1].patches,
    duration_analysis['Total']
):
    axes[1].text(
        bar.get_x() +
        bar.get_width()/2,
        bar.get_height() + 50,
        f'{val:,}',
        ha='center', fontsize=9
    )

plt.suptitle(
    'Impact of Call Duration on '
    'Subscription Rate',
    fontsize=14, fontweight='bold'
)
plt.tight_layout()
plt.savefig(os.path.join(
    CHARTS_DIR,
    '10_call_duration_impact.png'),
    dpi=150)
plt.show()
print("  ✅ Chart 10 saved: "
      "call_duration_impact.png")


# ── Chart 11: Previous Campaign Outcome ────────
poutcome_analysis = df.groupby('poutcome'
).agg(
    Total      = ('Sub_Num', 'count'),
    Subscribed = ('Sub_Num', 'sum'),
    Avg_Balance= ('Balance', 'mean')
).reset_index()

poutcome_analysis['Sub_Rate'] = (
    poutcome_analysis['Subscribed'] /
    poutcome_analysis['Total'] * 100
).round(2)

poutcome_analysis = \
    poutcome_analysis.sort_values(
    'Sub_Rate', ascending=False)

colors_outcome = {
    'Success': '#4CAF50',
    'Other':   '#FF9800',
    'Failure': '#F44336',
    'Unknown': '#9E9E9E'
}

fig, axes = plt.subplots(
    1, 2, figsize=(14, 6))

# Subscription rate
bars = axes[0].bar(
    poutcome_analysis['poutcome'],
    poutcome_analysis['Sub_Rate'],
    color=[
        colors_outcome.get(p, '#9E9E9E')
        for p in
        poutcome_analysis['poutcome']
    ]
)
axes[0].set_xlabel(
    'Previous Campaign Outcome')
axes[0].set_ylabel(
    'Subscription Rate (%)')
axes[0].set_title(
    'Subscription Rate by Previous Outcome',
    fontsize=13, fontweight='bold'
)
for bar, val in zip(
    bars,
    poutcome_analysis['Sub_Rate']
):
    axes[0].text(
        bar.get_x() +
        bar.get_width()/2,
        bar.get_height() + 0.5,
        f'{val:.1f}%',
        ha='center',
        fontweight='bold',
        fontsize=11
    )

# Customer count
axes[1].bar(
    poutcome_analysis['poutcome'],
    poutcome_analysis['Total'],
    color=[
        colors_outcome.get(p, '#9E9E9E')
        for p in
        poutcome_analysis['poutcome']
    ],
    alpha=0.7
)
axes[1].set_xlabel(
    'Previous Campaign Outcome')
axes[1].set_ylabel('Customer Count')
axes[1].set_title(
    'Customer Count by Previous Outcome',
    fontsize=13, fontweight='bold'
)
for bar, val in zip(
    axes[1].patches,
    poutcome_analysis['Total']
):
    axes[1].text(
        bar.get_x() +
        bar.get_width()/2,
        bar.get_height() + 100,
        f'{val:,}',
        ha='center', fontsize=10
    )

plt.suptitle(
    'Impact of Previous Campaign Outcome',
    fontsize=14, fontweight='bold'
)
plt.tight_layout()
plt.savefig(os.path.join(
    CHARTS_DIR,
    '11_previous_outcome.png'),
    dpi=150)
plt.show()
print("  ✅ Chart 11 saved: "
      "previous_outcome.png")



# ── Chart 12: Customer Segment Treemap ─────────
segment_data = df.groupby(
    'Job_Title'
).agg(
    Total      = ('Sub_Num', 'count'),
    Subscribed = ('Sub_Num', 'sum'),
    Avg_Balance= ('Balance', 'mean')
).reset_index()

segment_data['Sub_Rate'] = (
    segment_data['Subscribed'] /
    segment_data['Total'] * 100
).round(1)

segment_data = segment_data.sort_values(
    'Total', ascending=False)

# Create labels
labels = [
    f"{row['Job_Title'].title()}\n"
    f"{row['Total']:,} customers\n"
    f"Sub: {row['Sub_Rate']}%"
    for _, row in segment_data.iterrows()
]

# Color by subscription rate
colors = [
    '#4CAF50' if r >= 20
    else '#FF9800' if r >= 11.7
    else '#F44336'
    for r in segment_data['Sub_Rate']
]

plt.figure(figsize=(14, 8))
squarify.plot(
    sizes=segment_data['Total'],
    label=labels,
    color=colors,
    alpha=0.8,
    text_kwargs={
        'fontsize': 9,
        'fontweight': 'bold',
        'color': 'white'
    }
)
plt.axis('off')
plt.title(
    'Customer Segments by Job Type\n'
    '(Green=High Sub Rate, '
    'Orange=Average, Red=Below Average)',
    fontsize=14, fontweight='bold'
)
plt.tight_layout()
plt.savefig(os.path.join(
    CHARTS_DIR,
    '12_customer_segments_treemap.png'),
    dpi=150)
plt.show()
print("  ✅ Chart 12 saved: "
      "customer_segments_treemap.png")

# ── Summary ────────────────────────────────────
print("\n" + "=" * 50)
print("✅ Advanced EDA Complete!")
print(f"\n  📊 Key Advanced Findings:")
print(f"  • Best Education (Sub Rate): "
      f"{edu_analysis.loc[edu_analysis['Sub_Rate'].idxmax(), 'Education']}"
      f" ({edu_analysis['Sub_Rate'].max():.1f}%)")
print(f"  • Best Call Duration: "
      f"{duration_analysis.loc[duration_analysis['Sub_Rate'].idxmax(), 'Call_Duration_Group']}"
      f" ({duration_analysis['Sub_Rate'].max():.1f}%)")
# NEW — handle any case
success_mask = poutcome_analysis[
    'poutcome'].str.lower() == 'Success'
if success_mask.any():
    # Fix poutcome summary print
    success_rate = poutcome_analysis.loc[
        poutcome_analysis['poutcome'] == 'Success','Sub_Rate'].values

    if len(success_rate) > 0:
        print(f"  • Previous Success Impact: "
              f"{success_rate[0]:.1f}% vs "
              f"overall "
              f"{df['Sub_Num'].mean() * 100:.1f}%")
else:
    print(f"  • Previous Success: "
          f"No 'success' category found")
    print(f"  • poutcome values: "
          f"{poutcome_analysis['poutcome'].tolist()}")
print(f"\n  4 charts saved to:")
print(f"  {CHARTS_DIR}")
print("=" * 50)

