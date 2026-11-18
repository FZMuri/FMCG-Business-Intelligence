
-- FMCG Commercial Intelligence Platform
-- Dimensional layer: Product dimension

CREATE OR REPLACE TABLE dim_product AS
SELECT
    ROW_NUMBER() OVER (ORDER BY sku) AS product_key,
    sku,
    brand,
    segment,
    category
FROM (
    SELECT DISTINCT
        sku,
        brand,
        segment,
        category
    FROM stg_sales
) AS products;


-- Sales channel dimension
CREATE OR REPLACE TABLE dim_channel AS
SELECT
    ROW_NUMBER() OVER (ORDER BY channel) AS channel_key,
    channel
FROM (
    SELECT DISTINCT channel
    FROM stg_sales
) AS channels;


-- Region dimension
CREATE OR REPLACE TABLE dim_region AS
SELECT
    ROW_NUMBER() OVER (ORDER BY region) AS region_key,
    region
FROM (
    SELECT DISTINCT region
    FROM stg_sales
) AS regions;


-- Packaging dimension
CREATE OR REPLACE TABLE dim_pack_type AS
SELECT
    ROW_NUMBER() OVER (ORDER BY pack_type) AS pack_type_key,
    pack_type
FROM (
    SELECT DISTINCT pack_type
    FROM stg_sales
) AS pack_types;


-- Calendar dimension
CREATE OR REPLACE TABLE dim_date AS
SELECT
    CAST(STRFTIME(calendar_date, '%Y%m%d') AS INTEGER) AS date_key,
    calendar_date AS sales_date,
    YEAR(calendar_date) AS year,
    QUARTER(calendar_date) AS quarter,
    MONTH(calendar_date) AS month_number,
    MONTHNAME(calendar_date) AS month_name,
    WEEK(calendar_date) AS week_number,
    DAY(calendar_date) AS day_of_month,
    DAYOFWEEK(calendar_date) AS day_of_week_number
FROM generate_series(
    DATE '2022-01-01',
    DATE '2024-12-31',
    INTERVAL 1 DAY
) AS calendar(calendar_date)
