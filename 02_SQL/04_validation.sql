
-- FMCG Commercial Intelligence Platform
-- Automated data quality validation
-- Each test returns a count of failing records.
-- Expected result: 0 for every test.

SELECT
    'fact_row_count_mismatch' AS test_name,
    ABS(
        (SELECT COUNT(*) FROM fact_sales) -
        (SELECT COUNT(*) FROM stg_sales)
    ) AS failed_records

UNION ALL

SELECT
    'unmatched_foreign_keys',
    COUNT(*)
    FROM fact_sales
    WHERE date_key IS NULL
       OR product_key IS NULL
       OR channel_key IS NULL
       OR region_key IS NULL
       OR pack_type_key IS NULL

UNION ALL

SELECT
    'duplicate_fact_grain',
    COUNT(*)
    FROM (
        SELECT
            date_key,
            product_key,
            channel_key,
            region_key,
            pack_type_key
        FROM fact_sales
        GROUP BY ALL
        HAVING COUNT(*) > 1
    )

UNION ALL

SELECT
    'duplicate_product_keys',
    COUNT(*)
    FROM (
        SELECT product_key
        FROM dim_product
        GROUP BY product_key
        HAVING COUNT(*) > 1
    )

UNION ALL

SELECT
    'duplicate_product_skus',
    COUNT(*)
    FROM (
        SELECT sku
        FROM dim_product
        GROUP BY sku
        HAVING COUNT(*) > 1
    )

UNION ALL

SELECT
    'null_sales_dates',
    COUNT(*)
    FROM stg_sales
    WHERE sales_date IS NULL

UNION ALL

SELECT
    'null_product_skus',
    COUNT(*)
    FROM stg_sales
    WHERE sku IS NULL OR sku = '';
