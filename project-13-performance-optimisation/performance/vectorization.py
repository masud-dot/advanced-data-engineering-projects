import pandas as pd


def apply_vectorized_discount(
    df: pd.DataFrame,
    amount_column: str = "amount",
    discount_column: str = "discount_rate",
) -> pd.DataFrame:
    result = df.copy()

    result["discounted_amount"] = (
        result[amount_column]
        * (1 - result[discount_column])
    )

    return result


def classify_amount_vectorized(
    df: pd.DataFrame,
    amount_column: str = "amount",
) -> pd.DataFrame:
    result = df.copy()

    result["amount_category"] = pd.cut(
        result[amount_column],
        bins=[-float("inf"), 500, 1000, float("inf")],
        labels=["LOW", "MEDIUM", "HIGH"],
    )

    return result
