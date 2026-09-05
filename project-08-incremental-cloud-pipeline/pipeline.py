import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:admin@localhost:5432/data_engineering",
)

PIPELINE_NAME = "incremental_cloud_pipeline"
OUTPUT_PATH = Path("incremental_output.parquet")


def get_engine():
    return create_engine(DATABASE_URL)


def get_watermark(engine):
    query = text("""
        SELECT last_watermark
        FROM pipeline_metadata
        WHERE pipeline_name = :pipeline_name
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"pipeline_name": PIPELINE_NAME}).scalar()

    if result is None:
        raise RuntimeError(
            f"No watermark found for pipeline '{PIPELINE_NAME}'."
        )

    return result


def extract_incremental_data(engine, watermark):
    query = text("""
        SELECT
            transaction_id,
            customer_id,
            amount,
            created_at,
            updated_at
        FROM customer_transactions
        WHERE updated_at > :watermark
        ORDER BY updated_at, transaction_id
    """)

    return pd.read_sql(
        query,
        engine,
        params={"watermark": watermark},
    )


def transform_data(df):
    if df.empty:
        return df

    result = df.copy()

    result["updated_at"] = pd.to_datetime(result["updated_at"])
    result["created_at"] = pd.to_datetime(result["created_at"])

    result = result.drop_duplicates(
        subset=["transaction_id"],
        keep="last",
    )

    result["year"] = result["updated_at"].dt.year
    result["month"] = result["updated_at"].dt.month
    result["day"] = result["updated_at"].dt.day

    return result


def write_output(df):
    if df.empty:
        return

    df.to_parquet(
        OUTPUT_PATH,
        index=False,
        engine="pyarrow",
    )


def get_max_watermark(df):
    if df.empty:
        return None

    return df["updated_at"].max()


def update_watermark(engine, new_watermark):
    if new_watermark is None:
        return

    query = text("""
        UPDATE pipeline_metadata
        SET last_watermark = :new_watermark
        WHERE pipeline_name = :pipeline_name
    """)

    with engine.begin() as conn:
        conn.execute(
            query,
            {
                "new_watermark": new_watermark,
                "pipeline_name": PIPELINE_NAME,
            },
        )


def run_pipeline():
    engine = get_engine()

    watermark = get_watermark(engine)
    print(f"Current watermark: {watermark}")

    extracted = extract_incremental_data(engine, watermark)
    print(f"Extracted rows: {len(extracted)}")

    transformed = transform_data(extracted)
    print(f"Transformed rows: {len(transformed)}")

    if transformed.empty:
        print("No new records found. Watermark unchanged.")
        return

    new_watermark = get_max_watermark(transformed)

    write_output(transformed)

    # Advance the watermark only after the downstream output succeeds.
    update_watermark(engine, new_watermark)

    print(f"Output written to: {OUTPUT_PATH}")
    print(f"New watermark: {new_watermark}")
    print("Incremental pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
