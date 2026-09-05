import pandas as pd


class SimulatedSparkProcessor:
    """
    Local simulation of Spark Structured Streaming.

    The implementation uses Pandas deliberately. It represents the
    processing contract without claiming to execute Spark locally.
    """

    REQUIRED_COLUMNS = {
        "transaction_id",
        "customer_id",
        "transaction_timestamp",
        "merchant_category",
        "amount",
        "currency",
        "status",
    }

    def transform(self, transactions: pd.DataFrame) -> pd.DataFrame:
        missing = self.REQUIRED_COLUMNS - set(transactions.columns)

        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        df = transactions.copy()

        df["transaction_timestamp"] = pd.to_datetime(
            df["transaction_timestamp"], errors="coerce"
        )
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

        df = df.dropna(
            subset=[
                "transaction_id",
                "customer_id",
                "transaction_timestamp",
                "amount",
            ]
        )

        df = df[df["amount"] >= 0]
        df = df[df["status"] == "COMPLETED"]
        df = df.drop_duplicates(subset=["transaction_id"])

        return df.reset_index(drop=True)
