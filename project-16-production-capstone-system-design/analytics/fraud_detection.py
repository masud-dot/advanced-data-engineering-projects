import pandas as pd


class FraudDetector:
    """
    Deterministic rule-based fraud simulation.

    This demonstrates how production fraud screening can be represented
    locally without claiming to implement a real fraud model.
    """

    def detect(self, transactions: pd.DataFrame) -> pd.DataFrame:
        df = transactions.copy()

        df["fraud_flag"] = (
            (df["amount"] > 2000)
            | (
                df["merchant_category"].eq("Travel")
                & (df["amount"] > 1800)
            )
        )

        df["fraud_reason"] = "NONE"
        df.loc[df["amount"] > 2000, "fraud_reason"] = "HIGH_VALUE"
        df.loc[
            df["merchant_category"].eq("Travel")
            & (df["amount"] > 1800),
            "fraud_reason",
        ] = "HIGH_VALUE_TRAVEL"

        return df
