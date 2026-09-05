from pathlib import Path

import pandas as pd

from src.transformations import clean_incremental_data
from src.validation import validate_incremental_data


OUTPUT_PATH = Path("incremental_output.parquet")


def load_source_data(path: str) -> pd.DataFrame:
    """Load source transaction data from CSV."""
    return pd.read_csv(path)


def extract_incremental_data(
    df: pd.DataFrame,
    watermark: str,
) -> pd.DataFrame:
    """Return records newer than the supplied watermark."""
    result = df.copy()
    result["updated_at"] = pd.to_datetime(result["updated_at"])

    watermark_ts = pd.Timestamp(watermark)

    return result[
        result["updated_at"] > watermark_ts
    ].sort_values(
        ["updated_at", "transaction_id"]
    )


def run_local_pipeline(
    source_path: str = "sample_data/source_data.csv",
    watermark: str = "2026-01-15 00:00:00",
) -> pd.DataFrame:
    """Run the local incremental pipeline demonstration."""
    source = load_source_data(source_path)

    incremental = extract_incremental_data(
        source,
        watermark,
    )

    transformed = clean_incremental_data(incremental)

    validate_incremental_data(transformed)

    if not transformed.empty:
        transformed.to_parquet(
            OUTPUT_PATH,
            index=False,
            engine="pyarrow",
        )

    return transformed


if __name__ == "__main__":
    result = run_local_pipeline()

    print(f"Incremental rows processed: {len(result)}")

    if not result.empty:
        print(
            result[
                [
                    "transaction_id",
                    "customer_id",
                    "amount",
                    "updated_at",
                    "year",
                    "month",
                    "day",
                ]
            ].to_string(index=False)
        )

        print(f"\nOutput written to: {OUTPUT_PATH}")
    else:
        print("No new records found.")
