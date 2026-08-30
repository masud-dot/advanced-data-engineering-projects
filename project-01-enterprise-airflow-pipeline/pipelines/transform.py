import pandas as pd


REQUIRED_COLUMNS = {
    "order_id",
    "customer_name",
    "product_name",
    "quantity",
    "price",
    "order_date",
    "region",
}


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    missing_columns = REQUIRED_COLUMNS.difference(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    result = df.drop_duplicates().copy()

    result["quantity"] = pd.to_numeric(
        result["quantity"], errors="raise"
    ).astype(int)

    result["price"] = pd.to_numeric(
        result["price"], errors="raise"
    )

    result["order_date"] = pd.to_datetime(
        result["order_date"], errors="raise"
    ).dt.date

    result["total_amount"] = (
        result["price"] * result["quantity"]
    )

    return result
