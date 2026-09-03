import argparse
import os
from datetime import date
from pathlib import Path

import boto3
import pandas as pd


DEFAULT_BUCKET = "enterprise-data-lake"
DEFAULT_INPUT = "datasets/sales_data.csv"
DEFAULT_OUTPUT_DIR = "output"


def load_source_data(input_path: str) -> pd.DataFrame:
    """Load sales data from a local CSV file."""
    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    df = pd.read_csv(path)

    required_columns = {
        "order_id",
        "customer_name",
        "product_name",
        "quantity",
        "price",
        "order_date",
        "region",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean sales data and calculate total order amount."""
    cleaned = df.copy()

    cleaned = cleaned.drop_duplicates()
    cleaned = cleaned.dropna(
        subset=[
            "order_id",
            "quantity",
            "price",
            "order_date",
            "region",
        ]
    )

    cleaned["quantity"] = pd.to_numeric(
        cleaned["quantity"], errors="coerce"
    )
    cleaned["price"] = pd.to_numeric(
        cleaned["price"], errors="coerce"
    )

    cleaned["order_date"] = pd.to_datetime(
        cleaned["order_date"], errors="coerce"
    )

    cleaned = cleaned.dropna(
        subset=["quantity", "price", "order_date"]
    )

    cleaned = cleaned[
        (cleaned["quantity"] > 0) &
        (cleaned["price"] >= 0)
    ]

    cleaned["total_amount"] = (
        cleaned["quantity"] * cleaned["price"]
    )

    return cleaned


def create_regional_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create the Gold-layer regional sales summary."""
    summary = (
        df.groupby("region", as_index=False)["total_amount"]
        .sum()
        .rename(columns={"total_amount": "total_sales"})
    )

    return summary.sort_values("region").reset_index(drop=True)


def write_local_outputs(
    cleaned_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    output_dir: str,
) -> dict:
    """Write Silver and Gold datasets locally as Parquet."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    silver_path = output_path / "processed_sales.parquet"
    gold_path = output_path / "regional_sales_summary.parquet"

    cleaned_df.to_parquet(silver_path, index=False)
    summary_df.to_parquet(gold_path, index=False)

    return {
        "silver": silver_path,
        "gold": gold_path,
    }


def upload_to_s3(
    bucket: str,
    input_path: str,
    cleaned_path: Path,
    summary_path: Path,
) -> None:
    """Upload Bronze, Silver, and Gold datasets to Amazon S3."""
    s3 = boto3.client("s3")

    today = date.today()

    bronze_key = (
        f"bronze/sales/"
        f"year={today.year}/"
        f"month={today.month:02d}/"
        f"day={today.day:02d}/"
        f"sales_data.csv"
    )

    silver_key = "silver/cleaned_sales/processed_sales.parquet"
    gold_key = "gold/analytics/regional_sales_summary.parquet"

    s3.upload_file(input_path, bucket, bronze_key)
    s3.upload_file(str(cleaned_path), bucket, silver_key)
    s3.upload_file(str(summary_path), bucket, gold_key)

    print(f"Uploaded Bronze: s3://{bucket}/{bronze_key}")
    print(f"Uploaded Silver: s3://{bucket}/{silver_key}")
    print(f"Uploaded Gold:   s3://{bucket}/{gold_key}")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="AWS S3 Bronze-Silver-Gold data lake pipeline"
    )

    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT,
        help="Path to source CSV file",
    )

    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help="Local directory for generated Parquet files",
    )

    parser.add_argument(
        "--bucket",
        default=os.getenv("S3_BUCKET", DEFAULT_BUCKET),
        help="S3 bucket name",
    )

    parser.add_argument(
        "--upload",
        action="store_true",
        help="Upload Bronze, Silver, and Gold datasets to S3",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    print("Starting AWS S3 Data Lake Pipeline...")
    print(f"Input: {args.input}")

    # Bronze source
    df = load_source_data(args.input)
    print(f"Bronze records loaded: {len(df)}")

    # Silver transformation
    cleaned_df = transform_data(df)
    print(f"Silver records after cleaning: {len(cleaned_df)}")

    # Gold aggregation
    summary_df = create_regional_summary(cleaned_df)

    # Local outputs
    outputs = write_local_outputs(
        cleaned_df,
        summary_df,
        args.output_dir,
    )

    print(f"Silver output: {outputs['silver']}")
    print(f"Gold output:   {outputs['gold']}")

    print("\nRegional Sales Summary:")
    print(summary_df.to_string(index=False))

    # Optional AWS upload
    if args.upload:
        upload_to_s3(
            args.bucket,
            args.input,
            outputs["silver"],
            outputs["gold"],
        )
    else:
        print(
            "\nS3 upload skipped. "
            "Use --upload when AWS credentials and S3 access are configured."
        )

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
