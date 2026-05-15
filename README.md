# 🏦 Bank Customer Analytics & Risk Intelligence

![Python](https://img.shields.io/badge/Python-3.10-blue)
![SQL](https://img.shields.io/badge/SQL-Server-red)
![PowerBI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow)
![ML](https://img.shields.io/badge/ML-Random%20Forest-green)

## 📊 Project Overview
An end-to-end banking analytics project analyzing 
45,211 customers to predict term deposit 
subscription, identify customer segments, and 
assess credit risk.

## 🛠️ Tools Used
| Tool | Purpose |
|------|---------|
| Excel / Power Query | Data cleaning & scenario analysis |
| SQL Server (SSMS) | Database design & analytical queries |
| Python 3.10 | EDA, ML prediction, RFM segmentation |
| Power BI | 5-page interactive dashboard |

## 📁 Dataset
- **Source:** UCI Machine Learning Repository
- **Dataset:** Bank Marketing Dataset
- **Size:** 45,211 customer records
- **Features:** 17 columns

## 🔑 Key Findings

### Subscription Analysis
- Overall subscription rate: **11.7%**
- Students have the highest rate: **28.7%**
- March is the best month: **52.0%**
- Calls over 10 mins convert at: **48.4%**

### ML Model Performance
- Algorithm: **Random Forest Classifier**
- Accuracy: **84.3%**
- AUC Score: **0.916** (Excellent)
- Top predictor: **Call Duration (50.4%)**

### RFM Segmentation
- Champions (3.4%): **31.6%** subscription rate
- Average balance: **$3,366**
- Lost customers (40%): Only **$3** avg balance
- Biggest opportunity: **Need Attention** segment

### Risk Analysis
- Default rate: **1.8%** (815 customers)
- High Risk customers: all have a negative balance
- Previous campaign success: **64.7%** conversion

## 📊 Dashboard Pages
1. **Executive Summary** — KPIs, job analysis, risk
2. **Customer Segmentation** — RFM segments
3. **Churn & Risk Analysis** — ML predictions
4. **Campaign Performance** — Monthly trends
5. **ML Predictions** — Feature importance

## 💡 Business Recommendations
1. **Focus on March** — 52% subscription rate
2. **Train agents** — longer calls = more subscriptions
3. **Re-target previous successes** — 64.7% rate
4. **Champion retention** — highest value segment
5. **Re-engage Need Attention** — high balance, low engagement

## 🚀 How to Run

### Prerequisites
```bash
pip install -r requirements.txt
```

### Steps
1. Clone the repository
2. Download the UCI Bank Marketing dataset
3. Run Power Query cleaning in Excel
4. Import data to SQL Server
5. Run Python scripts in order (01-04)
6. Open Power BI dashboard

### Python Scripts Order
```bash
python 01_eda.py
python 02_eda_advanced.py
python 03_churn_prediction.py
python 04_rfm_segmentation.py
```

## 📸 Dashboard Screenshots

### Executive Summary
![Page 1](05_outputs/charts/dashboard_p1.png)

### Customer Segmentation
![Page 2](05_outputs/charts/dashboard_p2.png)

### Churn & Risk Analysis
![Page 3](05_outputs/charts/dashboard_p3.png)

### Campaign Performance
![Page 4](05_outputs/charts/dashboard_p4.png)

### ML Predictions
![Page 5](05_outputs/charts/dashboard_p5.png)
