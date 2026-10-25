"""
load_hillstrom.py  -  Clean the real Hillstrom email dataset
============================================================

Download the CSV first (see README) and save it as:
    data/hillstrom_raw.csv

Run:  python src/load_hillstrom.py

What this script does:
  1. Reads the raw CSV and checks the expected columns exist
  2. Turns `segment` (which email they got) into treatment 0/1
  3. Turns text columns (zip_code, channel) into numbers (one-hot encoding)
  4. Drops `history_segment` (it just repeats `history`)
  5. Saves a clean file: data/hillstrom_clean.csv
"""

import sys
import pandas as pd

RAW_PATH = "data/hillstrom_raw.csv"
CLEAN_PATH = "data/hillstrom_clean.csv"

EXPECTED_COLUMNS = {
    "recency", "history_segment", "history", "mens", "womens",
    "zip_code", "newbie", "channel", "segment",
    "visit", "conversion", "spend",
}


def load_hillstrom(path=RAW_PATH):
    df = pd.read_csv(path)

    # Safety check: fail early with a clear message if the file looks different
    missing = EXPECTED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}. Found: {list(df.columns)}")

    # Treatment: 1 = got any email (Men's or Women's), 0 = got no email
    df["treatment"] = (~df["segment"].str.contains("No", case=False)).astype(int)

    # Rename outcome to match our synthetic data
    df = df.rename(columns={"conversion": "bought"})

    # Text columns -> numbers (one column per category, 0/1)
    df = pd.get_dummies(df, columns=["zip_code", "channel"], dtype=int)

    # Add an ID, drop redundant columns
    df.insert(0, "customer_id", range(1, len(df) + 1))
    df = df.drop(columns=["history_segment", "segment"])

    return df


if __name__ == "__main__":
    try:
        df = load_hillstrom()
    except FileNotFoundError:
        sys.exit(f"Could not find {RAW_PATH}. Download the dataset first.")

    df.to_csv(CLEAN_PATH, index=False)
    print(f"Saved {len(df)} rows -> {CLEAN_PATH}\n")
    print(df.head())
    print("\nTreatment split (0 = no email, 1 = email):")
    print(df["treatment"].value_counts())
    print("\nAverage outcomes by treatment:")
    print(df.groupby("treatment")[["visit", "bought", "spend"]].mean().round(4))
