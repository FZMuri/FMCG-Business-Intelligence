
-- FMCG Commercial Intelligence Platform
-- Layer: Staging
-- Purpose: Standardise raw source fields and flag quality issues.

CREATE OR REPLACE TABLE stg_sales AS
SELECT
    TRY_CAST(date AS DATE) AS sales_date,
    TRIM(sku) AS sku,
    TRIM(brand) AS brand,
    TRIM(segment) AS segment,
    TRIM(category) AS category,
    TRIM(channel) AS channel,
    TRIM(region) AS region,
    TRIM(pack_type) AS pack_type,

    TRY_CAST(price_unit AS DECIMAL(12, 2)) AS unit_price,
    TRY_CAST(promotion_flag AS INTEGER) AS promotion_flag,
    TRY_CAST(delivery_days AS INTEGER) AS delivery_days,
    TRY_CAST(stock_available AS INTEGER) AS stock_available,
    TRY_CAST(delivered_qty AS INTEGER) AS delivered_qty,
    TRY_CAST(units_sold AS INTEGER) AS units_sold,

    CASE
        WHEN units_sold < 0
          OR delivered_qty < 0
          OR stock_available < 0
        THEN TRUE
        ELSE FALSE
    END AS is_negative_quantity_exception,

    CASE
        WHEN stock_available <= 0 THEN TRUE
        ELSE FALSE
    END AS is_potential_stockout

FROM read_csv_auto('01_Data/Raw/FMCG_2022_2024.csv');
