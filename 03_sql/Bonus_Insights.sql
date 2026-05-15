-- ── BONUS: Top Insights Queries ────────────────

-- Insight 1: Best customer profile for subscription
SELECT TOP 1
    Job,
    Education,
    Age_Group,
    Balance_Segment,
    COUNT(*) AS Customers,
    CAST(SUM(Sub_Num) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS Sub_Rate
FROM Bank_Customers
GROUP BY
    job,
    education,
    Age_Group,
    Balance_Segment
HAVING COUNT(*) > 50
ORDER BY Sub_Rate DESC;


-- Insight 2: Worst customer profile for subscription
SELECT TOP 1
    Job,
    Education,
    Age_Group,
    Balance_Segment,
    COUNT(*) AS Customers,
    CAST(SUM(Sub_Num) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS Sub_Rate
FROM Bank_Customers
GROUP BY
    Job,
    Education,
    Age_Group,
    Balance_Segment
HAVING COUNT(*) > 50
ORDER BY Sub_Rate ASC;


-- Insight 3: Impact of previous campaign success
SELECT
    poutcome AS Previous_Outcome,
    COUNT(*) AS Customers,
    CAST(SUM(Sub_Num) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS Sub_Rate,
    CAST(AVG(balance) AS DECIMAL(10,2)) AS Avg_Balance

FROM Bank_Customers
GROUP BY poutcome
ORDER BY Sub_Rate DESC;


-- Insight 4: Call duration impact on subscription
SELECT
    CASE
        WHEN duration < 60   THEN 'Under 1 min'
        WHEN duration < 180  THEN '1-3 mins'
        WHEN duration < 300  THEN '3-5 mins'
        WHEN duration < 600  THEN '5-10 mins'
        ELSE                      'Over 10 mins'
    END  AS Call_Duration,
    COUNT(*) AS Customers,
    SUM(Sub_Num) AS Subscribed,
    CAST(SUM(Sub_Num) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS Sub_Rate

FROM Bank_Customers
GROUP BY
    CASE
        WHEN duration < 60   THEN 'Under 1 min'
        WHEN duration < 180  THEN '1-3 mins'
        WHEN duration < 300  THEN '3-5 mins'
        WHEN duration < 600  THEN '5-10 mins'
        ELSE                      'Over 10 mins'
    END
ORDER BY Sub_Rate DESC;