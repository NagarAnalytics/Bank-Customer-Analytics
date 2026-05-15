# 01_eda.py
# Bank Customer Analytics — Exploratory Data Analysis
# ─────────────────────────────────────────────────────

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ── Setup ─────────────────────────────────────
BASE_PATH = r'C:\Users\Neha Nagar\Desktop\bank_analytics'
DATA_PATH = os.path.join(BASE_PATH, '01_data', 'cleaned')
CHARTS_DIR = os.path.join(BASE_PATH, '05_outputs', 'charts')
os.makedirs(CHARTS_DIR, exist_ok=True)

sns.set_theme(style='whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12

print("🔍 Starting Bank Customer EDA...")
print("=" * 50)

# ── Section 2: Load Data ───────────────────────
print("\n📦 Loading data...")

df = pd.read_csv(os.path.join(DATA_PATH, 'Bank_Customers.csv'))

print(f"  ✅ Rows:    {len(df):,}")
print(f"  ✅ Columns: {len(df.columns)}")
print(f"\n  Subscription Rate: "
      f"{df['Sub_Num'].mean()*100:.1f}%")
print(f"  Default Rate:      "
      f"{(df['default_status']=='Yes').mean()*100:.1f}%")
print(f"  Avg Balance:       "
      f"${df['Balance'].mean():,.2f}")

# ── Debug Default Column ───────────────────────
print("\n🔍 Checking default column...")

# Find the default column
default_cols = [c for c in df.columns
                if 'default' in c.lower()]
print(f"  Default columns found: {default_cols}")

# Check unique values
for col in default_cols:
    print(f"  {col} unique values: "
          f"{df[col].unique()}")


# ── Section 3: Charts ──────────────────────────
print("\n📊 Generating EDA charts...")

# ── Chart 1: Age Distribution ──────────────────
plt.figure(figsize=(12, 6))
sns.histplot(
    df['Age'],
    bins=30,
    color='#2196F3',
    edgecolor='white'
)
plt.axvline(
    df['Age'].mean(),
    color='red',
    linestyle='--',
    linewidth=2,
    label=f'Mean Age: {df["Age"].mean():.1f}'
)
plt.xlabel('Age')
plt.ylabel('Count')
plt.title(
    'Customer Age Distribution',
    fontsize=14, fontweight='bold'
)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(
    CHARTS_DIR, '01_age_distribution.png'),
    dpi=150)
plt.show()
print("  ✅ Chart 1 saved: age_distribution.png")

# ── Chart 2: Balance Distribution ─────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Full distribution
sns.histplot(
    df['Balance'],
    bins=50,
    color='#4CAF50',
    edgecolor='white',
    ax=axes[0]
)
axes[0].set_title(
    'Balance Distribution (Full)',
    fontsize=13, fontweight='bold'
)
axes[0].set_xlabel('Balance ($)')
axes[0].set_ylabel('Count')

# Zoomed in (remove extreme outliers)
df_filtered = df[
    (df['Balance'] > -2000) &
    (df['Balance'] < 20000)
]
sns.histplot(
    df_filtered['Balance'],
    bins=50,
    color='#4CAF50',
    edgecolor='white',
    ax=axes[1]
)
axes[1].set_title(
    'Balance Distribution (Zoomed)',
    fontsize=13, fontweight='bold'
)
axes[1].set_xlabel('Balance ($)')
axes[1].set_ylabel('Count')

plt.tight_layout()
plt.savefig(os.path.join(
    CHARTS_DIR, '02_balance_distribution.png'),
    dpi=150)
plt.show()
print("  ✅ Chart 2 saved: balance_distribution.png")

# ── Chart 3: Subscription Rate by Job ─────────
job_sub = df.groupby('Job_Title').agg(
    Total    = ('Sub_Num', 'count'),
    Subscribed = ('Sub_Num', 'sum')
).reset_index()
job_sub['Rate'] = (
    job_sub['Subscribed'] /
    job_sub['Total'] * 100
).round(2)
job_sub = job_sub.sort_values(
    'Rate', ascending=True)

plt.figure(figsize=(12, 7))
bars = plt.barh(
    job_sub['Job_Title'],
    job_sub['Rate'],
    color=sns.color_palette(
        'Blues_d', len(job_sub))
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
    'Subscription Rate by Job Type',
    fontsize=14, fontweight='bold'
)
plt.legend()
for bar, val in zip(
        bars, job_sub['Rate']):
    plt.text(
        bar.get_width() + 0.2,
        bar.get_y() + bar.get_height()/2,
        f'{val:.1f}%',
        va='center', fontsize=10
    )
plt.tight_layout()
plt.savefig(os.path.join(
    CHARTS_DIR, '03_subscription_by_job.png'),
    dpi=150)
plt.show()
print("  ✅ Chart 3 saved: subscription_by_job.png")

# ── Chart 4: Balance by Subscription ──────────
plt.figure(figsize=(12, 6))
sns.boxplot(
    data=df,
    x='y',
    y='Balance',
    palette={
        'Yes': '#4CAF50',
        'No':  '#F44336'
    }
)
plt.ylim(-2000, 20000)
plt.xlabel('Subscribed to Term Deposit')
plt.ylabel('Account Balance ($)')
plt.title(
    'Balance Distribution by Subscription Status',
    fontsize=14, fontweight='bold'
)
plt.xticks([0, 1], ['No', 'Yes'])
plt.tight_layout()
plt.savefig(os.path.join(
    CHARTS_DIR, '04_balance_by_subscription.png'),
    dpi=150)
plt.show()
print("  ✅ Chart 4 saved: "
      "balance_by_subscription.png")

# ── Chart 5: Correlation Heatmap ───────────────
plt.figure(figsize=(12, 8))
numeric_cols = [
    'Age', 'Balance', 'Duration',
    'Campaign', 'previous', 'Sub_Num'
]
corr_matrix = df[numeric_cols].corr().round(2)
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt='.2f',
    cmap='RdYlGn',
    linewidths=0.5,
    square=True,
    cbar_kws={'label': 'Correlation'}
)
plt.title(
    'Correlation Heatmap — Numeric Features',
    fontsize=14, fontweight='bold'
)
plt.tight_layout()
plt.savefig(os.path.join(
    CHARTS_DIR, '05_correlation_heatmap.png'),
    dpi=150)
plt.show()
print("  ✅ Chart 5 saved: correlation_heatmap.png")

# ── Chart 6: Subscription by Age Group ────────
age_sub = df.groupby(
    'Age_Group',
    observed=True
).agg(
    Total      = ('Sub_Num', 'count'),
    Subscribed = ('Sub_Num', 'sum')
).reset_index()
age_sub['Rate'] = (
    age_sub['Subscribed'] /
    age_sub['Total'] * 100
).round(2)

fig, ax1 = plt.subplots(figsize=(12, 6))
bars = ax1.bar(
    age_sub['Age_Group'],
    age_sub['Total'],
    color='#2196F3',
    alpha=0.7,
    label='Total Customers'
)
ax1.set_xlabel('Age Group')
ax1.set_ylabel(
    'Total Customers', color='#2196F3')
ax1.tick_params(
    axis='y', labelcolor='#2196F3')

ax2 = ax1.twinx()
ax2.plot(
    age_sub['Age_Group'],
    age_sub['Rate'],
    color='#FF9800',
    marker='o',
    linewidth=2,
    markersize=8,
    label='Subscription Rate'
)
ax2.set_ylabel(
    'Subscription Rate (%)',
    color='#FF9800')
ax2.tick_params(
    axis='y', labelcolor='#FF9800')

plt.title(
    'Customer Count and Subscription Rate '
    'by Age Group',
    fontsize=14, fontweight='bold'
)
fig.legend(loc='upper right',
           bbox_to_anchor=(0.9, 0.9))
plt.tight_layout()
plt.savefig(os.path.join(
    CHARTS_DIR, '06_subscription_by_age.png'),
    dpi=150)
plt.show()
print("  ✅ Chart 6 saved: subscription_by_age.png")

# ── Chart 7: Monthly Subscription Trend ───────
monthly = df.groupby(
    ['Month_Num', 'Month']
).agg(
    Total      = ('Sub_Num', 'count'),
    Subscribed = ('Sub_Num', 'sum')
).reset_index()
monthly['Rate'] = (
    monthly['Subscribed'] /
    monthly['Total'] * 100
).round(2)
monthly = monthly.sort_values('Month_Num')

fig, ax1 = plt.subplots(figsize=(14, 6))
ax1.bar(
    monthly['Month'],
    monthly['Total'],
    color='#2196F3',
    alpha=0.7,
    label='Total Contacts'
)
ax1.set_xlabel('Month')
ax1.set_ylabel(
    'Total Contacts', color='#2196F3')

ax2 = ax1.twinx()
ax2.plot(
    monthly['Month'],
    monthly['Rate'],
    color='#FF9800',
    marker='o',
    linewidth=2,
    markersize=8,
    label='Subscription Rate %'
)
ax2.set_ylabel(
    'Subscription Rate (%)',
    color='#FF9800')

plt.title(
    'Monthly Campaign Performance',
    fontsize=14, fontweight='bold'
)
fig.legend(loc='upper right',
           bbox_to_anchor=(0.9, 0.9))
plt.tight_layout()
plt.savefig(os.path.join(
    CHARTS_DIR, '07_monthly_performance.png'),
    dpi=150)
plt.show()
print("  ✅ Chart 7 saved: monthly_performance.png")

# ── Chart 8: Risk Distribution ─────────────────
risk_dist = df['Risk_Flag'].value_counts()

colors_risk = {
    'High Risk':   '#F44336',
    'Medium Risk': '#FF9800',
    'Low Risk':    '#4CAF50'
}

plt.figure(figsize=(10, 6))
bars = plt.bar(
    risk_dist.index,
    risk_dist.values,
    color=[colors_risk.get(r, '#9E9E9E')
           for r in risk_dist.index]
)
plt.xlabel('Risk Level')
plt.ylabel('Number of Customers')
plt.title(
    'Customer Risk Distribution',
    fontsize=14, fontweight='bold'
)
for bar, val in zip(bars, risk_dist.values):
    pct = val/len(df)*100
    plt.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + 100,
        f'{val:,}\n({pct:.1f}%)',
        ha='center', fontsize=11
    )
plt.tight_layout()
plt.savefig(os.path.join(
    CHARTS_DIR, '08_risk_distribution.png'),
    dpi=150)
plt.show()
print("  ✅ Chart 8 saved: risk_distribution.png")

# ── Summary ────────────────────────────────────
print("\n" + "=" * 50)
print("✅ EDA Complete!")
print(f"\n  📊 8 charts saved to:")
print(f"  {CHARTS_DIR}")
print(f"\n  🔑 Key Findings:")
print(f"  • Subscription Rate: "
      f"{df['Sub_Num'].mean()*100:.1f}%")
print(f"  • Default Rate:      "
      f"{(df['default_status']=='Yes').mean()*100:.1f}%")
print(f"  • Avg Balance:       "
      f"${df['Balance'].mean():,.2f}")
print(f"  • Top Job (Sub Rate):"
      f" {job_sub.iloc[-1]['Job_Title']} "
      f"({job_sub.iloc[-1]['Rate']:.1f}%)")
print(f"  • Best Month:        "
      f"{monthly.loc[monthly['Rate'].idxmax(), 'Month']}"
      f" ({monthly['Rate'].max():.1f}%)")
print(f"  • High Risk Customers:"
      f" {(df['Risk_Flag']=='High Risk').sum():,}")
print("=" * 50)