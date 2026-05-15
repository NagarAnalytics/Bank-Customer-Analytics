# 03_churn_prediction.py
# Bank Customer Churn Prediction
# Using Random Forest Classifier
# ─────────────────────────────────────────────

# What this script does:
# 1. Loads 45,211 customer records
# 2. Teaches a model to predict subscription
# 3. Tests how accurate the model is
# 4. Shows which factors matter most
# 5. Exports predictions for Power BI

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# These are the ML tools — like a calculator
# but for pattern finding
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
from sklearn.preprocessing import LabelEncoder

# ── Setup ──────────────────────────────────────
BASE_PATH = r'C:\Users\NEHA NAGAR\Desktop\bank_analytics'
DATA_PATH = os.path.join(
    BASE_PATH, '01_data', 'cleaned')
CHARTS_DIR = os.path.join(
    BASE_PATH, '05_outputs', 'charts')
os.makedirs(CHARTS_DIR, exist_ok=True)

sns.set_theme(style='whitegrid')

print("🤖 Bank Customer Subscription Predictor")
print("=" * 50)
print("  Using: Random Forest Classifier")
print("  Goal:  Predict who will subscribe")
print("=" * 50)


# ── Section 2: Load and Prepare Data ──────────
# Think of this as gathering all the information
# about each customer before making a prediction

print("\n📦 Step 1: Loading customer data...")

df = pd.read_csv(
    os.path.join(DATA_PATH,
                 'Bank_Customers.csv')
)

# Standardize text columns to lowercase
text_cols = [
    'y', 'Job_Title', 'Marital_Status', 'Education',
    'Housing', 'Loan', 'Contact',
    'Month', 'poutcome' ]

for col in text_cols:
    if col in df.columns:
        df[col] = df[col].str.lower().str.strip()

# Handle default column
if 'default' in df.columns:
    df['default_status'] = (
        df['default'].str.lower().str.strip()
    )
elif 'default_status' in df.columns:
    df['default_status'] = (
        df['default_status'].str.lower().str.strip()
    )

print(f"  ✅ Loaded {len(df):,} customers")

# ── Section 3: Select Features ─────────────────
# Features = the columns we use to make predictions
# Think of these as clues that help predict
# whether a customer will subscribe

print("\n📋 Step 2: Selecting prediction features...")

# These are our INPUT columns (the clues)
# We chose these because they describe
# the customer and the campaign
feature_cols = [
    'Age',             # How old is the customer?
    'Balance',         # How much money do they have?
    'Duration',        # How long was the call?
    'Campaign',        # How many times contacted?
    'previous',        # Previous campaign contacts?
    'Job_Title',       # What do they do for work?
    'Marital_Status',  # Are they married?
    'Education',       # What is their education?
    'default_status',  # Do they have default?
    'Housing',         # Do they have housing loan?
    'Loan',            # Do they have personal loan?
    'Contact',         # How were they contacted?
    'Month',           # Which month?
    'poutcome'         # Previous campaign result?
]

# This is our OUTPUT column (what we predict)
target_col = 'y'  # yes = subscribed, no = didn't

print(f"  ✅ Input features:  {len(feature_cols)}")
print(f"  ✅ Target variable: {target_col}")
print(f"\n  Features used:")
for i, col in enumerate(feature_cols, 1):
    print(f"    {i:2}. {col}")

# ── Section 4: Convert Text to Numbers ─────────
# ML models only understand numbers not text
# So we convert 'yes'/'no' to 1/0
# and 'management'/'student' to 0/1/2/3...

print("\n🔄 Step 3: Converting text to numbers...")
print("  (ML models only understand numbers)")

# Copy only the columns we need
df_ml = df[feature_cols + [target_col]].copy()

# LabelEncoder converts text to numbers
# Example: 'blue-collar'=0, 'management'=1,
#          'student'=2, 'technician'=3...
le = LabelEncoder()

# Columns that need converting
text_features = [
    'Job_Title', 'Marital_Status', 'Education',
    'default_status', 'Housing', 'Loan',
    'Contact', 'Month', 'poutcome'
]

# Store encoding mappings for later reference
encoding_map = {}

for col in text_features:
    df_ml[col] = le.fit_transform(
        df_ml[col].astype(str)
    )
    encoding_map[col] = dict(
        zip(le.classes_,
            le.transform(le.classes_))
    )
    print(f"  ✅ {col:<20} "
          f"→ {len(encoding_map[col])} categories")

# Convert target: yes=1, no=0
df_ml[target_col] = (
    df_ml[target_col] == 'yes').astype(int)

print(f"\n  ✅ All conversions complete!")
print(f"  Subscribers (1): "
      f"{df_ml[target_col].sum():,}")
print(f"  Non-subscribers (0): "
      f"{(df_ml[target_col]==0).sum():,}")


# ── Section 5: Split Data ──────────────────────
# We split data into two groups:
# - Training set: model LEARNS from this (80%)
# - Testing set:  we CHECK accuracy on this (20%)
#
# Why not train on everything?
# If you study the exact exam questions
# you'll ace the test but learn nothing!
# Same principle here.

print("\n✂️  Step 4: Splitting data 80/20...")

# X = all input features (the clues)
X = df_ml[feature_cols]

# y = what we want to predict
y = df_ml[target_col]

# Split into training and testing
# random_state=42 means results are
# reproducible — same split every time
X_train, X_test, y_train, y_test = \
    train_test_split(
        X, y,
        test_size=0.2,      # 20% for testing
        random_state=42,    # reproducible
        stratify=y          # keep same ratio
    )                       # of yes/no in both

print(f"  ✅ Training set: {len(X_train):,} "
      f"customers (80%)")
print(f"  ✅ Testing set:  {len(X_test):,} "
      f"customers (20%)")
print(f"\n  Training subscribers: "
      f"{y_train.sum():,} "
      f"({y_train.mean()*100:.1f}%)")
print(f"  Testing subscribers:  "
      f"{y_test.sum():,} "
      f"({y_test.mean()*100:.1f}%)")

# ── Section 6: Train the Model ─────────────────
# This is where the magic happens!
# The model looks at 36,168 customers
# and learns patterns that predict subscription
#
# n_estimators=100 means 100 decision trees
# max_depth=10 means each tree can be
# 10 levels deep
# class_weight='balanced' handles the fact
# that only 11.7% subscribed
# (imbalanced dataset)

print("\n🤖 Step 5: Training Random Forest...")
print("  Building 100 decision trees...")
print("  This may take 30-60 seconds...")

model = RandomForestClassifier(
    n_estimators=100,       # 100 trees
    max_depth=10,           # tree depth
    random_state=42,        # reproducible
    class_weight='balanced',# handle imbalance
    n_jobs=-1               # use all CPU cores
)

# This one line trains the entire model!
# It's looking at all 36,168 customers
# and learning patterns
model.fit(X_train, y_train)

print(f"  ✅ Model trained successfully!")
print(f"  Trees built: "
      f"{model.n_estimators}")
print(f"  Features used: "
      f"{model.n_features_in_}")

# ── Section 7: Make Predictions ───────────────
# Now we test the model on the 9,043
# customers it has NEVER seen before

print("\n🔮 Step 6: Making predictions...")
print("  Testing on 9,043 unseen customers...")

# Predict yes/no for each test customer
y_pred = model.predict(X_test)

# Predict PROBABILITY of subscribing
# This gives a score 0-100% for each customer
y_prob = model.predict_proba(X_test)[:, 1]

print(f"  ✅ Predictions complete!")
print(f"  Predicted subscribers: "
      f"{y_pred.sum():,}")
print(f"  Actual subscribers:    "
      f"{y_test.sum():,}")


# ── Section 8: Evaluate Accuracy ──────────────
# Now we check how well the model performed
# Think of this as marking the exam paper

print("\n📊 Step 7: Evaluating model accuracy...")

# Overall accuracy — what % did it get right?
accuracy = accuracy_score(y_test, y_pred)
print(f"\n  🎯 Overall Accuracy: "
      f"{accuracy*100:.1f}%")

# Detailed report showing:
# Precision = of all predicted yes, how many
#             were actually yes?
# Recall    = of all actual yes, how many
#             did we correctly predict?
# F1-Score  = balance between precision/recall
print(f"\n  📋 Detailed Report:")
print(classification_report(
    y_test, y_pred,
    target_names=[
        'Not Subscribed',
        'Subscribed'
    ]
))

# ── Section 9: Confusion Matrix ────────────────
# Shows exactly what the model got right/wrong
#
#                 Predicted No  Predicted Yes
# Actual No    [True Negative   False Positive]
# Actual Yes   [False Negative  True Positive ]

print("\n📊 Step 8: Confusion Matrix...")

cm = confusion_matrix(y_test, y_pred)

tn = cm[0][0]  # Correctly said No
fp = cm[0][1]  # Wrongly said Yes
fn = cm[1][0]  # Wrongly said No
tp = cm[1][1]  # Correctly said Yes

print(f"\n  True Negatives  (correctly said No):  "
      f"{tn:,}")
print(f"  False Positives (wrongly said Yes):    "
      f"{fp:,}")
print(f"  False Negatives (wrongly said No):     "
      f"{fn:,}")
print(f"  True Positives  (correctly said Yes):  "
      f"{tp:,}")

print(f"\n  💡 Business Meaning:")
print(f"  • {tp:,} subscribers correctly identified"
      f" → campaign them!")
print(f"  • {fp:,} non-subscribers wrongly flagged"
      f" → wasted calls")
print(f"  • {fn:,} subscribers missed"
      f" → lost opportunity")

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=[
        'Not Subscribed',
        'Subscribed'
    ],
    yticklabels=[
        'Not Subscribed',
        'Subscribed'
    ]
)
plt.title(
    'Confusion Matrix — Subscription Prediction',
    fontsize=14, fontweight='bold'
)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.tight_layout()
plt.savefig(os.path.join(
    CHARTS_DIR,
    '13_confusion_matrix.png'),
    dpi=150)
plt.show()
print("\n  ✅ Chart 13 saved: confusion_matrix.png")

# ── Section 10: Feature Importance ────────────
# Which columns mattered most for prediction?
# This is the most business-valuable insight!

print("\n📊 Step 9: Feature Importance Analysis...")
print("  (Which factors predict subscription?)")

importance_df = pd.DataFrame({
    'Feature':   feature_cols,
    'Importance': model.feature_importances_
}).sort_values(
    'Importance',
    ascending=False
)

print(f"\n  Top 10 Most Important Features:")
print(f"  {'Feature':<20} {'Importance':>10} "
      f"{'Bar'}")
print(f"  {'-'*50}")

for _, row in importance_df.head(10).iterrows():
    bar = '█' * int(
        row['Importance'] * 200)
    print(f"  {row['Feature']:<20} "
          f"{row['Importance']:>10.4f} "
          f"{bar}")

# Plot feature importance
plt.figure(figsize=(12, 7))
colors = [
    '#2196F3' if i < 3
    else '#64B5F6' if i < 6
    else '#BBDEFB'
    for i in range(len(importance_df))
]
bars = plt.barh(
    importance_df['Feature'][::-1],
    importance_df['Importance'][::-1],
    color=colors[::-1]
)
plt.xlabel('Importance Score')
plt.title(
    'Feature Importance — '
    'What Predicts Subscription?',
    fontsize=14, fontweight='bold'
)
for bar, val in zip(
    bars,
    importance_df['Importance'][::-1]
):
    plt.text(
        bar.get_width() + 0.001,
        bar.get_y() + bar.get_height()/2,
        f'{val:.4f}',
        va='center', fontsize=9
    )
plt.tight_layout()
plt.savefig(os.path.join(
    CHARTS_DIR,
    '14_feature_importance.png'),
    dpi=150)
plt.show()
print("  ✅ Chart 14 saved: feature_importance.png")

# ── Section 11: Export Predictions ────────────
# Export predictions for Power BI dashboard

print("\n💾 Step 10: Exporting predictions...")

# Add predictions to test set
results_df = X_test.copy()
results_df['Actual_Subscribed']    = \
    y_test.values
results_df['Predicted_Subscribed'] = y_pred
results_df['Subscription_Probability'] = \
    (y_prob * 100).round(2)

# Add risk category based on probability
results_df['Risk_Category'] = pd.cut(
    results_df['Subscription_Probability'],
    bins=[0, 25, 50, 75, 100],
    labels=[
        'Low Probability',
        'Medium Probability',
        'High Probability',
        'Very High Probability'
    ]
)

# Export to CSV
results_df.to_csv(
    os.path.join(
        BASE_PATH,
        '05_outputs',
        'churn_predictions.csv'
    ),
    index=False
)
print("  ✅ Exported: churn_predictions.csv")

# ── Summary ────────────────────────────────────
print("\n" + "=" * 50)
print("✅ Churn Prediction Complete!")
print(f"\n  🎯 Model Performance:")
print(f"  Overall Accuracy:    "
      f"{accuracy*100:.1f}%")
print(f"  Subscribers Found:   {tp:,}")
print(f"  Subscribers Missed:  {fn:,}")
print(f"\n  🔑 Top 3 Predictors:")
for i, row in importance_df.head(3).iterrows():
    print(f"  {importance_df.index.get_loc(i)+1}. "
          f"{row['Feature']:<20} "
          f"{row['Importance']:.4f}")
print(f"\n  📁 Files saved:")
print(f"  • charts/13_confusion_matrix.png")
print(f"  • charts/14_feature_importance.png")
print(f"  • outputs/churn_predictions.csv")
print("=" * 50)


# ── BONUS: ROC Curve ───────────────────────────
from sklearn.metrics import roc_curve, auc

print("\n📊 Bonus: ROC Curve...")

# Calculate ROC curve points
fpr, tpr, thresholds = roc_curve(
    y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(10, 7))
plt.plot(
    fpr, tpr,
    color='#2196F3',
    linewidth=2,
    label=f'ROC Curve '
          f'(AUC = {roc_auc:.3f})'
)
plt.plot(
    [0, 1], [0, 1],
    color='grey',
    linestyle='--',
    linewidth=1,
    label='Random Classifier (AUC = 0.5)'
)
plt.fill_between(
    fpr, tpr,
    alpha=0.1,
    color='#2196F3'
)
plt.xlabel(
    'False Positive Rate\n'
    '(Non-subscribers wrongly flagged)',
    fontsize=11
)
plt.ylabel(
    'True Positive Rate\n'
    '(Subscribers correctly found)',
    fontsize=11
)
plt.title(
    f'ROC Curve — Subscription Prediction\n'
    f'AUC Score: {roc_auc:.3f} '
    f'(Higher is Better, Max = 1.0)',
    fontsize=14, fontweight='bold'
)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(
    CHARTS_DIR,
    '15_roc_curve.png'),
    dpi=150)
plt.show()
print(f"  ✅ Chart 15 saved: roc_curve.png")
print(f"  AUC Score: {roc_auc:.3f}")
print(f"  (0.5 = random, 1.0 = perfect)")