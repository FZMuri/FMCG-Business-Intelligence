
import pandas as pd
from pathlib import Path

# Location of the raw dataset
DATA_FOLDER = Path("01_Data/Raw")

files = list(DATA_FOLDER.glob("*"))

for file in files:

    if file.suffix.lower() not in [".csv", ".parquet"]:
        continue

    print("\n" + "=" * 70)
    print(f"FILE: {file.name}")
    print("=" * 70)

    try:
        if file.suffix.lower() == ".csv":
            df = pd.read_csv(file)
        else:
            df = pd.read_parquet(file)

        print(f"\nRows: {df.shape[0]:,}")
        print(f"Columns: {df.shape[1]}")

        print("\nCOLUMN NAMES AND DATA TYPES:")
        print(df.dtypes)

        print("\nFIRST 5 RECORDS:")
        print(df.head().to_string())

        print("\nMISSING VALUES:")
        print(df.isnull().sum())

        print("\nDUPLICATE ROWS:")
        print(df.duplicated().sum())

        print("\nMEMORY USAGE:")
        print(f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    except Exception as e:
        print(f"ERROR: {e}")
        