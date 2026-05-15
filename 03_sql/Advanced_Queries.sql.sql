USE BankAnalyticsDB

-- ── ADVANCED QUERY 1: Customer Value Ranking ──
-- Uses CTE + Window Functions (RANK, NTILE)


USE BankAnalyticsDB;

-- ── ADVANCED QUERY 1: Customer Value Ranking ──
-- Uses CTE + Window Functions (RANK, NTILE)
WITH CustomerScores AS (
    SELECT
        age,
        job,
        education,
        balance,
        Sub_Num,
        Risk_Flag,
        -- Score each customer 1-100
        CAST(
            -- Balance score (40%)
            (CAST(balance AS FLOAT) /
            MAX(balance) OVER() * 40) +
            -- Subscription score (40%)
            (Sub_Num * 40) +
            -- Risk score (20%)
            (CASE Risk_Flag
                WHEN 'Low Risk'    THEN 20
                WHEN 'Medium Risk' THEN 10
                ELSE 0
            END)
        AS DECIMAL(5,2))            AS Customer_Score
    FROM Bank_Customers
    WHERE balance >= 0
)
SELECT
    age,
    job,
    education,
    balance,
    Risk_Flag,
    Customer_Score,
    RANK() OVER (
        ORDER BY Customer_Score DESC
    )                               AS Overall_Rank,
    NTILE(4) OVER (
        ORDER BY Customer_Score DESC
    )                               AS Customer_Tier,
    CASE NTILE(4) OVER (
        ORDER BY Customer_Score DESC)
        WHEN 1 THEN 'Platinum'
        WHEN 2 THEN 'Gold'
        WHEN 3 THEN 'Silver'
        ELSE       'Bronze'
    END                             AS Tier_Label
FROM CustomerScores
ORDER BY Customer_Score DESC;

-- ── ADVANCED QUERY 2: Campaign Effectiveness ──
-- Uses CTE + LAG + Running Total
WITH MonthlyStats AS (
    SELECT
        Month_Num,
        month,
        COUNT(*)                    AS Total_Contacts,
        SUM(Sub_Num)                AS Subscribed,
        CAST(SUM(Sub_Num) * 100.0 /
            COUNT(*) AS DECIMAL(5,2)) AS Sub_Rate,
        CAST(AVG(duration) AS
            DECIMAL(10,2))          AS Avg_Duration
    FROM Bank_Customers
    GROUP BY Month_Num, month
)
SELECT
    Month_Num,
    month,
    Total_Contacts,
    Subscribed,
    Sub_Rate,
    Avg_Duration,
    -- Previous month subscription rate
    LAG(Sub_Rate) OVER (
        ORDER BY Month_Num
    )                               AS Prev_Month_Rate,
    -- Month over Month change
    CAST(Sub_Rate - LAG(Sub_Rate)
        OVER (ORDER BY Month_Num)
        AS DECIMAL(5,2))            AS MoM_Change,
    -- Running total of subscribers
    SUM(Subscribed) OVER (
        ORDER BY Month_Num
        ROWS BETWEEN UNBOUNDED
        PRECEDING AND CURRENT ROW
    )                               AS Running_Total_Subscribed,
    -- Running subscription rate
    CAST(SUM(Subscribed) OVER (
        ORDER BY Month_Num
        ROWS BETWEEN UNBOUNDED
        PRECEDING AND CURRENT ROW) * 100.0 /
        SUM(Total_Contacts) OVER (
        ORDER BY Month_Num
        ROWS BETWEEN UNBOUNDED
        PRECEDING AND CURRENT ROW)
        AS DECIMAL(5,2))            AS Running_Sub_Rate
FROM MonthlyStats
ORDER BY Month_Num;

-- ── ADVANCED QUERY 3: Customer Segmentation ───
-- Uses Multiple CTEs + PERCENT_RANK
WITH BalancePercentile AS (
    SELECT
        age,
        job,
        marital,
        education,
        balance,
        Sub_Num,
        Risk_Flag,
        Age_Group,
        Balance_Segment,
        Has_Any_Loan,
        -- Balance percentile rank
        CAST(PERCENT_RANK() OVER (
            ORDER BY balance
        ) * 100 AS DECIMAL(5,2))    AS Balance_Percentile
    FROM Bank_Customers
),
CustomerSegments AS (
    SELECT
        *,
        CASE
            WHEN Balance_Percentile >= 75
                AND Sub_Num = 1
                AND Risk_Flag = 'Low Risk'
            THEN 'Premium Loyal'
            WHEN Balance_Percentile >= 75
                AND Sub_Num = 0
            THEN 'High Value Prospect'
            WHEN Balance_Percentile >= 50
                AND Sub_Num = 1
            THEN 'Mid Value Loyal'
            WHEN Balance_Percentile >= 50
                AND Sub_Num = 0
            THEN 'Mid Value Prospect'
            WHEN Balance_Percentile >= 25
            THEN 'Growing Customer'
            ELSE 'Entry Level'
        END                         AS Customer_Segment
    FROM BalancePercentile
)
SELECT
    Customer_Segment,
    COUNT(*)                        AS Customer_Count,
    CAST(COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER()
        AS DECIMAL(5,2))            AS Pct_Of_Total,
    CAST(AVG(balance)
        AS DECIMAL(10,2))           AS Avg_Balance,
    SUM(Sub_Num)                    AS Subscribed,
    CAST(SUM(Sub_Num) * 100.0 /
        COUNT(*) AS DECIMAL(5,2))   AS Sub_Rate,
    SUM(CASE WHEN Risk_Flag =
        'High Risk' THEN 1 ELSE 0
        END)                        AS High_Risk_Count
FROM CustomerSegments
GROUP BY Customer_Segment
ORDER BY Avg_Balance DESC;