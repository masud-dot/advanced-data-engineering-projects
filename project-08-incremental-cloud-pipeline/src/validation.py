import pandas as pd


def validate_incremental_data(df: pd.DataFrame) -> None:
    """Validate incremental records before downstream loading."""
    required_columns = {
        "transaction_id",
        "customer_id",
        "amount",
        "updated_at",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    if df["transaction_id"].duplicated().any():
        raise ValueError("Duplicate transaction_id values detected.")

    if (df["amount"] < 0).any():
        raise ValueError("Negative transaction amounts detected.")

    if df["updated_at"].isna().any():
        raise ValueError("Null updated_at values detected.")
