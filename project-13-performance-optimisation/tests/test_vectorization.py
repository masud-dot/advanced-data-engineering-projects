import pandas as pd

from performance.vectorization import (
    apply_vectorized_discount,
    classify_amount_vectorized,
)


def test_vectorized_discount():
    df = pd.DataFrame(
        {
            "amount": [100.0, 200.0],
            "discount_rate": [0.10, 0.20],
        }
    )

    result = apply_vectorized_discount(df)

    assert result["discounted_amount"].tolist() == [
        90.0,
        160.0,
    ]


def test_vectorized_classification():
    df = pd.DataFrame(
        {
            "amount": [100.0, 750.0, 1500.0],
        }
    )

    result = classify_amount_vectorized(df)

    assert result["amount_category"].astype(str).tolist() == [
        "LOW",
        "MEDIUM",
        "HIGH",
    ]
