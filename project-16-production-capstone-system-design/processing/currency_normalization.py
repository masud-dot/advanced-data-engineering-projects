import pandas as pd


class CurrencyNormalizer:
    """
    Normalize synthetic transaction amounts to USD.

    These rates are illustrative only and are intentionally fixed so the
    project remains deterministic and runnable without external services.
    Production systems should source FX rates from an approved provider.
    """

    DEFAULT_USD_RATES = {
        "USD": 1.00,
        "GBP": 1.25,
        "CAD": 0.74,
        "EUR": 1.08,
    }

    def __init__(self, usd_rates: dict[str, float] | None = None):
        self.usd_rates = usd_rates or self.DEFAULT_USD_RATES.copy()

    def normalize(self, transactions: pd.DataFrame) -> pd.DataFrame:
        df = transactions.copy()

        df["usd_rate"] = df["currency"].map(self.usd_rates)

        if df["usd_rate"].isna().any():
            currencies = sorted(
                df.loc[df["usd_rate"].isna(), "currency"].unique()
            )
            raise ValueError(
                f"Missing USD conversion rates for currencies: {currencies}"
            )

        df["amount_usd"] = (df["amount"] * df["usd_rate"]).round(2)

        return df
