import pandas as pd


REQUIRED_COLUMNS = {
    "transaction_id",
    "customer_id",
    "product_id",
    "amount",
    "event_time",
    "region",
}


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich raw lakehouse sales records."""
    if df.empty:
        return df.copy()

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    result = df.copy()

    result["amount"] = pd.to_numeric(
        result["amount"],
        errors="coerce",
    )

    result["event_time"] = pd.to_datetime(
        result["event_time"],
        errors="coerce",
    )

    result["region"] = result["region"].astype("string").str.strip()

    result = result.dropna(
        subset=[
            "transaction_id",
            "customer_id",
            "product_id",
            "amount",
            "event_time",
            "region",
        ]
    )

    result = result[result["amount"] > 0]

    result = result.drop_duplicates(
        subset=["transaction_id"],
        keep="last",
    )

    result["year"] = result["event_time"].dt.year
    result["month"] = result["event_time"].dt.month
    result["day"] = result["event_time"].dt.day

    return result
