
import pandas as pd

file_path = "01_Data/Raw/FMCG_2022_2024.csv"
df = pd.read_csv(file_path)

# 1. Records with negative quantities
negative_qty = df[
    (df["units_sold"] < 0) |
    (df["delivered_qty"] < 0)
]

print("\n=== NEGATIVE QUANTITIES ===")
print(negative_qty.to_string(index=False))

# 2. Records with negative stock
negative_stock = df[df["stock_available"] < 0]

print("\n=== NEGATIVE STOCK ===")
print(negative_stock.to_string(index=False))

# 3. Compare zero sales and stockout records
zero_sales = df["units_sold"] == 0
stockout = df["stock_available"] <= 0

print("\n=== ZERO SALES VS STOCKOUT ===")
print("Zero sales:", zero_sales.sum())
print("Stockout:", stockout.sum())
print("Both zero sales and stockout:", (zero_sales & stockout).sum())
print("Zero sales without stockout:", (zero_sales & ~stockout).sum())
print("Stockout without zero sales:", (stockout & ~zero_sales).sum())

# 4. Check whether product attributes are consistent
product_check = (
    df.groupby("sku")
    .agg(
        brand_count=("brand", "nunique"),
        category_count=("category", "nunique"),
        segment_count=("segment", "nunique")
    )
)

print("\n=== SKU ATTRIBUTE CONSISTENCY ===")
print(product_check[
    (product_check["brand_count"] > 1) |
    (product_check["category_count"] > 1) |
    (product_check["segment_count"] > 1)
])

# 5. Check pack type consistency per SKU
pack_check = (
    df.groupby("sku")
    .agg(
        pack_type_count=("pack_type", "nunique"),
        pack_types=("pack_type", lambda x: ", ".join(sorted(x.unique())))
    )
)

print("\n=== PACK TYPE CONSISTENCY ===")
print(pack_check[
    pack_check["pack_type_count"] > 1
])

print("\n=== PACK TYPE DISTRIBUTION ===")
print(df.groupby("pack_type")["sku"].nunique())
