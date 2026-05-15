USE BankAnalyticsDB;

-- ── VIEW 1: Customer Summary ───────────────────
CREATE VIEW vw_Customer_Summary AS

SELECT
    Job,
    Marital_Status,
    Education,
    Age_Group,
    Balance_Segment,
    Risk_Flag,
    COUNT(*) AS Total_Customers,
    CAST(AVG(balance) AS DECIMAL(10,2)) AS Avg_Balance,
    SUM(Sub_Num) AS Total_Subscribed,
    CAST(SUM(Sub_Num) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS Subscription_Rate,
    SUM(CASE WHEN default_status = 'yes' THEN 1 ELSE 0 END) AS Total_Defaulted,
    CAST(SUM(CASE WHEN default_status = 'yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS Default_Rate

FROM Bank_Customers
GROUP BY
    Job,
    Marital_Status,
    Education,
    Age_Group,
    Balance_Segment,
    Risk_Flag;

-- Test View 1
SELECT TOP 10 * FROM vw_Customer_Summary
ORDER BY Subscription_Rate DESC;


-- ── VIEW 2: Campaign Performance ──────────────
CREATE VIEW vw_Campaign_Performance AS

SELECT
    Month,
    Month_Num,
    Contact,
    COUNT(*) AS Total_Contacts,
    SUM(Sub_Num) AS Total_Subscribed,
    CAST(SUM(Sub_Num) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS Subscription_Rate,
    CAST(AVG(duration) AS DECIMAL(10,2)) AS Avg_Call_Duration,
    CAST(AVG(campaign) AS DECIMAL(10,2)) AS Avg_Contacts_Per_Customer,
    SUM(CASE WHEN poutcome = 'success' THEN 1 ELSE 0 END) AS Previous_Success,
    CAST(AVG(balance) AS DECIMAL(10,2)) AS Avg_Customer_Balance

FROM Bank_Customers
GROUP BY
    Month,
    Month_Num,
    contact;

-- Test View 2
SELECT * FROM vw_Campaign_Performance
ORDER BY Month_Num;