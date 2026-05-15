USE BankAnalyticsDB;


CREATE TABLE Bank_Customers (
    Age                 INT,
    Job                 VARCHAR(50),
    Marital_Status      VARCHAR(20),
    Education           VARCHAR(20),
    default_status      VARCHAR(5),
    Balance             INT,
    Housing             VARCHAR(5),
    Loan                VARCHAR(5),
    Contact             VARCHAR(20),
    Day                 INT,
    Month               VARCHAR(10),
    Duration            INT,
    Campaign            INT,
    pdays               INT,
    previous            INT,
    poutcome            VARCHAR(20),
    y                   VARCHAR(5),
    Age_Group           VARCHAR(20),
    Balance_Segment     VARCHAR(20),
    Subscribed          INT,
    Has_Any_Loan        VARCHAR(5),
    Risk_Flag           VARCHAR(20),
    Month_Num           INT,
    Sub_Num             INT
);



-- Check row count
SELECT COUNT(*) AS Total_Rows 
FROM Bank_Customers;

-- Check sample data
SELECT TOP 5 * 
FROM Bank_Customers;

-- Check column data types
SELECT 
    COLUMN_NAME,
    DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Bank_Customers'
ORDER BY ORDINAL_POSITION;
