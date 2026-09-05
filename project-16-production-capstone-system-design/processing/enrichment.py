import pandas as pd


class TransactionEnricher:
    """Join transaction events with customer master data."""

    def enrich(
        self,
        transactions: pd.DataFrame,
        customers: pd.DataFrame,
    ) -> pd.DataFrame:
        df = transactions.merge(
            customers,
            on="customer_id",
            how="left",
            validate="many_to_one",
        )

        df["customer_name"] = df["customer_name"].fillna("UNKNOWN")
        df["country"] = df["country"].fillna("UNKNOWN")
        df["customer_segment"] = df["customer_segment"].fillna("UNKNOWN")

        return df
