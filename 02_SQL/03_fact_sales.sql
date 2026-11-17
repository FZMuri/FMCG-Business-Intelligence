
-- FMCG Commercial Intelligence Platform
-- Fact table: one row per date, SKU, channel, region, pack type

CREATE OR REPLACE TABLE fact_sales AS
SELECT
    d.date_key,
    p.product_key,
    c.channel_key,
    r.region_key,
    pk.pack_type_key,

    s.units_sold,
    s.unit_price,

    -- Estimated sales value, not confirmed net revenue
    CAST(
        s.units_sold * s.unit_price
        AS DECIMAL(18, 2)
    ) AS estimated_sales_value,

    s.delivered_qty,
    s.stock_available,
    s.delivery_days,
    s.promotion_flag,
    s.is_negative_quantity_exception,
    s.is_potential_stockout

FROM stg_sales AS s

LEFT JOIN dim_date AS d
    ON s.sales_date = d.sales_date

LEFT JOIN dim_product AS p
    ON s.sku = p.sku

LEFT JOIN dim_channel AS c
    ON s.channel = c.channel

LEFT JOIN dim_region AS r
    ON s.region = r.region

LEFT JOIN dim_pack_type AS pk
    ON s.pack_type = pk.pack_type;
