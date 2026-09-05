from pathlib import Path

import pandas as pd

from src.transformations import clean_sales_data
from src.validation import validate_sales_data


BASE_OUTPUT = Path("local_output")


def load_raw_data(
    source_path: str = "sample_data/raw_sales.csv",
) -> pd.DataFrame:
    """Load synthetic raw sales data."""
    return pd.read_csv(source_path)


def write_bronze(df: pd.DataFrame) -> Path:
    """Write the Bronze layer as Parquet."""
    path = BASE_OUTPUT / "bronze"
    path.mkdir(parents=True, exist_ok=True)

    output = path / "sales.parquet"
    df.to_parquet(output, index=False, engine="pyarrow")

    return output


def build_silver(df: pd.DataFrame) -> pd.DataFrame:
    """Transform raw records into the Silver layer."""
    return clean_sales_data(df)


def write_silver(df: pd.DataFrame) -> Path:
    """Write the cleaned Silver layer as Parquet."""
    path = BASE_OUTPUT / "silver"
    path.mkdir(parents=True, exist_ok=True)

    output = path / "sales.parquet"
    df.to_parquet(output, index=False, engine="pyarrow")

    return output


def build_gold(df: pd.DataFrame) -> pd.DataFrame:
    """Create business-level Gold sales metrics."""
    gold = (
        df.groupby("product_id", as_index=False)
        .agg(
            total_sales=("amount", "sum"),
            order_count=("transaction_id", "count"),
            avg_order_value=("amount", "mean"),
        )
        .sort_values("total_sales", ascending=False)
    )

    return gold


def write_gold(df: pd.DataFrame) -> Path:
    """Write the Gold analytical dataset."""
    path = BASE_OUTPUT / "gold"
    path.mkdir(parents=True, exist_ok=True)

    output = path / "gold_sales.parquet"
    df.to_parquet(output, index=False, engine="pyarrow")

    return output


def run_pipeline() -> None:
    """Execute the local Bronze → Silver → Gold pipeline."""
    raw = load_raw_data()

    bronze_path = write_bronze(raw)

    silver = build_silver(raw)
    validate_sales_data(silver)
    silver_path = write_silver(silver)

    gold = build_gold(silver)
    gold_path = write_gold(gold)

    print(f"Bronze rows: {len(raw)}")
    print(f"Silver rows: {len(silver)}")
    print(f"Gold rows: {len(gold)}")
    print(f"Bronze output: {bronze_path}")
    print(f"Silver output: {silver_path}")
    print(f"Gold output: {gold_path}")
    print("\nGold sales summary:")
    print(gold.to_string(index=False))
    print("\nLakehouse pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
