import pandas as pd


def validate_processed_data(df: pd.DataFrame):
    """Validate the output of the ETL pipeline."""
    required_columns = {
        "transaction_id",
        "amount",
        "tax_amount",
        "total_amount",
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required output columns: {sorted(missing)}"
        )

    if df.empty:
        raise ValueError("Processed dataset is empty.")

    if df.isnull().any().any():
        raise ValueError("Processed dataset contains null values.")

    if (df["amount"] < 0).any():
        raise ValueError("Processed dataset contains negative amounts.")

    expected_total = df["amount"] + df["tax_amount"]

    if not expected_total.round(2).equals(
        df["total_amount"].round(2)
    ):
        raise ValueError("Total amount calculation failed.")

    if df["transaction_id"].duplicated().any():
        raise ValueError("Duplicate transaction IDs detected.")

    return True
