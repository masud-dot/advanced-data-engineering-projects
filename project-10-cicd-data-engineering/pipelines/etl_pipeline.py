from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {"transaction_id", "amount"}


def process_data(file_path="sample_data/sample_sales.csv"):
    """Process sales data and calculate tax and final transaction amount."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    df = pd.read_csv(path)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    if df["amount"].isna().any():
        raise ValueError("Input contains null amount values.")

    if (df["amount"] < 0).any():
        raise ValueError("Input contains negative amount values.")

    result = df.copy()
    result["tax_amount"] = result["amount"] * 0.18
    result["total_amount"] = result["amount"] + result["tax_amount"]

    return result


if __name__ == "__main__":
    result = process_data()
    print(result.to_string(index=False))
    print(f"\nProcessed rows: {len(result)}")
