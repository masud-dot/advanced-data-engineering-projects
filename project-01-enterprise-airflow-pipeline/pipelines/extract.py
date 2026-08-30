from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "order_id",
    "customer_name",
    "product_name",
    "quantity",
    "price",
    "order_date",
    "region",
]


def extract_data(file_path: str) -> pd.DataFrame:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    df = pd.read_csv(path)

    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return df
