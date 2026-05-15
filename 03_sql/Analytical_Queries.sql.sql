USE BankAnalyticsDB;

-- ── QUERY 1: Overall Subscription Rate ─────────

SELECT 
	COUNT(*) AS 'Total Customer', 
	SUM(Sub_Num) AS 'Total Subscribed',
	CAST(SUM(Sub_Num) * 100.0 / COUNT(*) AS Decimal(5,2)) AS 'Subscription Rate'
FROM Bank_Customers


-- ── QUERY 2: Subscription Rate by Job ─────────

SELECT 
	Job,
	COUNT(*) AS 'Total Customer',
	SUM(Sub_Num) as 'Subscribed',
	CAST(SUM(Sub_Num) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS 'Subscription Rate'
FROM Bank_Customers
GROUP BY Job
ORDER BY 'Subscription Rate' DESC



-- ── QUERY 3: Default Rate by Job ──────────────

SELECT 
	Job,
	COUNT(*) as 'Total Customer',
	SUM(CASE WHEN default_status = 'Yes' Then 1 ELSE 0 END) AS Defaulted,
	CAST(SUM(CASE WHEN default_status = 'Yes' Then 1 ELSE 0 END) * 100.0 / COUNT(*) AS Decimal(5,2)) AS 'Default Rate'
FROM Bank_Customers
GROUP BY Job
ORDER BY 'Default Rate' DESC


-- ── QUERY 4: Balance by Education ─────────────

SELECT 
	Education,
	COUNT(*) AS 'Total Customer',
	CAST(AVG(Balance) AS Decimal(10,2)) AS 'Average Balance',
	MAX(Balance) AS 'Max Balance',
	MIN(Balance) AS 'Min Balance',
	SUM(Sub_Num) AS 'Subscribed',
	CAST(SUM(Sub_Num) * 100.0 / COUNT(*) AS Decimal(5,2)) AS 'Subscription Rate'
FROM Bank_Customers
GROUP BY Education
ORDER BY 'Average Balance' DESC



-- ── QUERY 5: Risk Distribution ────────────────

SELECT 
	Risk_Flag,
	COUNT(*) AS Customer_Count,
	CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS DECIMAL(5,2)) AS Percentage,
	SUM(Sub_Num) AS Subscribed,
	CAST(AVG(Balance) AS Decimal(10,2)) AS Avg_Balance,
	CAST(SUM(Sub_Num) * 100.0 / COUNT(*) AS Decimal(5,2)) AS 'Subscription Rate'
FROM Bank_Customers
GROUP BY Risk_Flag
ORDER BY Customer_Count DESC;


-- ── QUERY 6: Monthly Campaign Performance ─────

SELECT
    month,
    Month_Num,
    COUNT(*)                                AS Total_Contacts,
    SUM(Sub_Num)                            AS Subscribed,
    CAST(SUM(Sub_Num) * 100.0 /
        COUNT(*) AS DECIMAL(5,2))           AS Subscription_Rate,
    CAST(AVG(duration) AS DECIMAL(10,2))    AS Avg_Call_Duration
FROM Bank_Customers
GROUP BY month, Month_Num
ORDER BY Month_Num;



-- ── QUERY 7: Age Group Analysis ───────────────

SELECT
    Age_Group,
    COUNT(*)                                AS Total_Customers,
    CAST(AVG(balance) AS DECIMAL(10,2))     AS Avg_Balance,
    SUM(Sub_Num)                            AS Subscribed,
    CAST(SUM(Sub_Num) * 100.0 /
        COUNT(*) AS DECIMAL(5,2))           AS Subscription_Rate,
    SUM(CASE WHEN default_status = 'yes'
        THEN 1 ELSE 0 END)                  AS Defaulted
FROM Bank_Customers
GROUP BY Age_Group
ORDER BY Subscription_Rate DESC;


-- ── QUERY 8: Balance Segment Analysis ─────────

SELECT
    Balance_Segment,
    COUNT(*)                                AS Customer_Count,
    CAST(AVG(balance) AS DECIMAL(10,2))     AS Avg_Balance,
    SUM(Sub_Num)                            AS Subscribed,
    CAST(SUM(Sub_Num) * 100.0 /
        COUNT(*) AS DECIMAL(5,2))           AS Subscription_Rate,
    SUM(CASE WHEN default_status = 'yes'
        THEN 1 ELSE 0 END)                  AS Defaulted
FROM Bank_Customers
GROUP BY Balance_Segment
ORDER BY Avg_Balance DESC;

