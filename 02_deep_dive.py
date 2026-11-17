
import pandas as pd
from pathlib import Path

folder = Path("01_Data/Raw")

# Load primary dataset
df = pd.read_csv(folder / "FMCG_2022_2024.csv")

# Convert date to proper datetime
df["date"] = pd.to_datetime(df["date"])

print("\n========== 1. DATE COVERAGE ==========")
print("Start date:", df["date"].min())
print("End date:", df["date"].max())
print("Unique dates:", df["date"].nunique())

print("\n========== 2. BUSINESS DIMENSIONS ==========")

dimensions = [
    "sku", "brand", "segment",
    "category", "channel", "region", "pack_type"
]

for col in dimensions:
    print(f"{col}: {df[col].nunique()} unique values")
    print(df[col].value_counts().to_string())
    print("-" * 40)

print("\n========== 3. NUMERIC PROFILING ==========")

numeric_cols = [
    "price_unit", "delivery_days",
    "stock_available", "delivered_qty", "units_sold"
]

print(df[numeric_cols].describe().round(2))

print("\n========== 4. BUSINESS METRICS ==========")

df["estimated_revenue"] = (
    df["price_unit"] * df["units_sold"]
)

print("Total units sold:", df["units_sold"].sum())
print("Estimated revenue:", round(
    df["estimated_revenue"].sum(), 2
))

print("Zero-sales records:",
      (df["units_sold"] == 0).sum())

print("Promotion records:",
      (df["promotion_flag"] == 1).sum())

print("Stockout records:",
      (df["stock_available"] == 0).sum())

print("\n========== 5. DATA GRAIN ==========")

candidate_key = [
    "date", "sku", "channel", "region", "pack_type"
]

print("Duplicate candidate keys:",
      df.duplicated(subset=candidate_key).sum())

print("\n========== 6. BUSINESS RULE CHECKS ==========")

print("Sales exceeding delivered quantity:",
      (df["units_sold"] > df["delivered_qty"]).sum())

print("Negative quantities:",
      ((df["units_sold"] < 0) |
       (df["delivered_qty"] < 0)).sum())

print("Negative prices:",
      (df["price_unit"] < 0).sum())

print("\n========== 7. REVENUE BY CHANNEL ==========")

print(
    df.groupby("channel")["estimated_revenue"]
    .sum()
    .sort_values(ascending=False)
    .round(2)
)

print("\n========== 8. REVENUE BY CATEGORY ==========")

print(
    df.groupby("category")["estimated_revenue"]
    .sum()
    .sort_values(ascending=False)
    .round(2)
)

print("\n========== PROFILING COMPLETED ==========")
