
from pathlib import Path
import duckdb

# Identify the project root independently of terminal location
BASE_DIR = Path(__file__).resolve().parent

# Create a local folder for the DuckDB database
db_dir = BASE_DIR / "01_Data" / "Processed"
db_dir.mkdir(parents=True, exist_ok=True)

db_path = db_dir / "fmcg.duckdb"
sql_path = BASE_DIR / "02_SQL" / "01_staging.sql"

# Execute SQL from the project root so relative CSV paths resolve
import os
os.chdir(BASE_DIR)

with duckdb.connect(str(db_path)) as con:
    sql = sql_path.read_text(encoding="utf-8")

    print(f"Executing SQL file: {sql_path}")
    print(f"SQL length: {len(sql)} characters")
    print(f"SQL preview: {sql[:200]}")

    con.execute(sql)
    
    dimensions_sql_path = BASE_DIR / "02_SQL" / "02_dimensions.sql"
    dimensions_sql = dimensions_sql_path.read_text(encoding="utf-8")
    con.execute(dimensions_sql)
    
    # Build FactSales after staging and dimensions
    fact_sql_path = BASE_DIR / "02_SQL" / "03_fact_sales.sql"
    fact_sql = fact_sql_path.read_text(encoding="utf-8")
    con.execute(fact_sql)

    print("\nFactSales created successfully.")

    
    dimension_validation = con.execute("""
        SELECT 'dim_product' AS table_name, COUNT(*) AS row_count
        FROM dim_product

        UNION ALL

        SELECT 'dim_channel', COUNT(*)
        FROM dim_channel

        UNION ALL

        SELECT 'dim_region', COUNT(*)
        FROM dim_region

        UNION ALL

        SELECT 'dim_pack_type', COUNT(*)
        FROM dim_pack_type

        UNION ALL

        SELECT 'dim_date', COUNT(*)
        FROM dim_date
    """).fetchdf()

    print("\n=== DIMENSION VALIDATION ===")
    print(dimension_validation.to_string(index=False))

        
    fact_validation = con.execute("""
        SELECT
            COUNT(*) AS total_fact_rows,
            COUNT(*) FILTER (
                WHERE date_key IS NULL
                OR product_key IS NULL
                OR channel_key IS NULL
                OR region_key IS NULL
                OR pack_type_key IS NULL
            ) AS unmatched_dimension_rows,
            SUM(units_sold) AS total_units_sold,
            SUM(estimated_sales_value) AS estimated_sales_value,
            COUNT(*) FILTER (
                WHERE is_negative_quantity_exception
            ) AS negative_quantity_exceptions
        FROM fact_sales
    """).fetchdf()

    print("\n=== FACT SALES VALIDATION ===")
    print(fact_validation.to_string(index=False))

    product_validation = con.execute("""
        SELECT
            COUNT(*) AS total_products,
            COUNT(DISTINCT sku) AS unique_skus,
            COUNT(DISTINCT product_key) AS unique_product_keys
        FROM dim_product
    """).fetchdf()

    print("\n=== PRODUCT DIMENSION VALIDATION ===")
    print(product_validation.to_string(index=False))
    

    tables = con.execute("SHOW TABLES").fetchall()
    print(f"Tables after execution: {tables}")

    result = con.execute("""
        SELECT
            COUNT(*) AS total_records,
            COUNT(DISTINCT sales_date) AS unique_dates,
            SUM(CAST(is_negative_quantity_exception AS INTEGER))
                AS negative_quantity_exceptions,
            SUM(CAST(is_potential_stockout AS INTEGER))
                AS potential_stockout_records
        FROM stg_sales
    """).fetchdf()

    print("\n=== STAGING VALIDATION ===")
    print(result.to_string(index=False))
    
    # Run automated SQL data quality tests
    validation_sql_path = BASE_DIR / "02_SQL" / "04_validation.sql"
    validation_sql = validation_sql_path.read_text(encoding="utf-8")

    validation_results = con.execute(validation_sql).fetchdf()

    print("\n=== AUTOMATED DATA QUALITY TESTS ===")
    print(validation_results.to_string(index=False))

    failed_tests = validation_results[
        validation_results["failed_records"] > 0
    ]

    if not failed_tests.empty:
        raise RuntimeError(
            "Data quality validation failed:\n"
            + failed_tests.to_string(index=False)
        )

    print("\nAll automated data quality tests passed.")

print("\nPipeline completed successfully.")
