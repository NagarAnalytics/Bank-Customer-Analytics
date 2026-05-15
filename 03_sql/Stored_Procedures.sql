-- ── STORED PROCEDURE 1: Customer Filter by Risk ────────
CREATE PROCEDURE sp_GetCustomersByRisk
    @RiskLevel      VARCHAR(20),
    @MinBalance     INT = 0,
    @TopN           INT = 100
AS
BEGIN
    SELECT TOP (@TopN)
        Age,
        Job,
        Marital_Status,
        Education,
        Balance,
        Risk_Flag,
        Age_Group,
        Balance_Segment,
        Sub_Num,
        default_status
    FROM Bank_Customers
    WHERE Risk_Flag = @RiskLevel AND Balance >= @MinBalance
    ORDER BY Balance DESC;
END;

-- Test Stored Procedure 1
-- Get top 10 High Risk customers with balance > 1000
EXEC sp_GetCustomersByRisk
    @RiskLevel  = 'High Risk',
    @MinBalance = 1000,
    @TopN       = 10;

-- Get top 20 Low Risk customers with balance > 5000
EXEC sp_GetCustomersByRisk
    @RiskLevel  = 'Low Risk',
    @MinBalance = 5000,
    @TopN       = 20;



-- ── STORED PROCEDURE 2: Segment Analysis ──────
CREATE PROCEDURE sp_SegmentAnalysis
    @SegmentType    VARCHAR(20),
    @SegmentValue   VARCHAR(50)
AS
BEGIN
    IF @SegmentType = 'job'
    BEGIN
        SELECT
            Age_Group,
            COUNT(*)                        AS Customers,
            CAST(AVG(balance)
                AS DECIMAL(10,2))           AS Avg_Balance,
            SUM(Sub_Num)                    AS Subscribed,
            CAST(SUM(Sub_Num) * 100.0 /
                COUNT(*) AS DECIMAL(5,2))   AS Sub_Rate
        FROM Bank_Customers
        WHERE job = @SegmentValue
        GROUP BY Age_Group
        ORDER BY Sub_Rate DESC;
    END

    IF @SegmentType = 'education'
    BEGIN
        SELECT
            job,
            COUNT(*)                        AS Customers,
            CAST(AVG(balance)
                AS DECIMAL(10,2))           AS Avg_Balance,
            SUM(Sub_Num)                    AS Subscribed,
            CAST(SUM(Sub_Num) * 100.0 /
                COUNT(*) AS DECIMAL(5,2))   AS Sub_Rate
        FROM Bank_Customers
        WHERE education = @SegmentValue
        GROUP BY job
        ORDER BY Sub_Rate DESC;
    END

    IF @SegmentType = 'age_group'
    BEGIN
        SELECT
            job,
            education,
            COUNT(*)                        AS Customers,
            CAST(AVG(balance)
                AS DECIMAL(10,2))           AS Avg_Balance,
            SUM(Sub_Num)                    AS Subscribed,
            CAST(SUM(Sub_Num) * 100.0 /
                COUNT(*) AS DECIMAL(5,2))   AS Sub_Rate
        FROM Bank_Customers
        WHERE Age_Group = @SegmentValue
        GROUP BY job, education
        ORDER BY Sub_Rate DESC;
    END
END;

-- Test Stored Procedure 2
-- Analyze management job segment
EXEC sp_SegmentAnalysis
    @SegmentType  = 'job',
    @SegmentValue = 'management';

-- Analyze tertiary education segment
EXEC sp_SegmentAnalysis
    @SegmentType  = 'education',
    @SegmentValue = 'tertiary';

-- Analyze 25-34 age group
EXEC sp_SegmentAnalysis
    @SegmentType  = 'age_group',
    @SegmentValue = '25-34';