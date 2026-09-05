import pandas as pd


def clean_incremental_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich incremental transaction records."""
    if df.empty:
        return df.copy()

    result = df.copy()

    result["amount"] = pd.to_numeric(result["amount"], errors="coerce")
    result["created_at"] = pd.to_datetime(result["created_at"], errors="coerce")
    result["updated_at"] = pd.to_datetime(result["updated_at"], errors="coerce")

    result = result.dropna(
        subset=["transaction_id", "customer_id", "amount", "updated_at"]
    )

    result = result.drop_duplicates(
        subset=["transaction_id"],
        keep="last",
    )

    result["year"] = result["updated_at"].dt.year
    result["month"] = result["updated_at"].dt.month
    result["day"] = result["updated_at"].dt.day

    return result
