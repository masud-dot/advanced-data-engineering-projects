import pandas as pd


def validate_sales_data(df: pd.DataFrame) -> None:
    """Validate cleaned Silver-layer sales data."""
    required_columns = {
        "transaction_id",
        "customer_id",
        "product_id",
        "amount",
        "event_time",
        "region",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    if df["transaction_id"].duplicated().any():
        raise ValueError("Duplicate transaction_id values detected.")

    if df["amount"].isna().any():
        raise ValueError("Null amount values detected.")

    if (df["amount"] <= 0).any():
        raise ValueError("Non-positive sales amounts detected.")

    if df["event_time"].isna().any():
        raise ValueError("Null event_time values detected.")

    if df["customer_id"].isna().any():
        raise ValueError("Null customer_id values detected.")

    if df["product_id"].isna().any():
        raise ValueError("Null product_id values detected.")
