import pandas as pd
import pytest

from src.lakehouse_pipeline import build_gold
from src.transformations import clean_sales_data
from src.validation import validate_sales_data


def sample_dataframe():
    return pd.DataFrame(
        [
            {
                "transaction_id": 1,
                "customer_id": 101,
                "product_id": "P100",
                "amount": 100.00,
                "event_time": "2026-01-10 10:00:00",
                "region": "East",
            },
            {
                "transaction_id": 2,
                "customer_id": 102,
                "product_id": "P200",
                "amount": 200.00,
                "event_time": "2026-01-20 10:00:00",
                "region": "West",
            },
        ]
    )


def test_clean_sales_data():
    result = clean_sales_data(sample_dataframe())

    assert len(result) == 2
    assert "year" in result.columns
    assert "month" in result.columns
    assert "day" in result.columns


def test_validation_rejects_negative_amount():
    df = sample_dataframe()
    df.loc[0, "amount"] = -10

    with pytest.raises(ValueError):
        validate_sales_data(df)


def test_gold_aggregation():
    df = clean_sales_data(sample_dataframe())

    gold = build_gold(df)

    assert len(gold) == 2
    assert set(gold.columns) == {
        "product_id",
        "total_sales",
        "order_count",
        "avg_order_value",
    }
