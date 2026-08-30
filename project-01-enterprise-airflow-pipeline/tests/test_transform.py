import pandas as pd
import pytest

from pipelines.transform import transform_data


COLUMNS = [
    "order_id",
    "customer_name",
    "product_name",
    "quantity",
    "price",
    "order_date",
    "region",
]


def test_transform_removes_duplicates_and_calculates_total():
    df = pd.DataFrame(
        [
            ["1001", "Alice", "Laptop", 1, 75000, "2026-01-05", "East"],
            ["1001", "Alice", "Laptop", 1, 75000, "2026-01-05", "East"],
        ],
        columns=COLUMNS,
    )

    result = transform_data(df)

    assert len(result) == 1
    assert result.loc[0, "total_amount"] == 75000


def test_transform_rejects_missing_columns():
    df = pd.DataFrame({"order_id": ["1001"]})

    with pytest.raises(ValueError):
        transform_data(df)


def test_transform_calculates_multiple_units():
    df = pd.DataFrame(
        [
            ["1002", "Bob", "Keyboard", 2, 2000, "2026-01-05", "West"],
        ],
        columns=COLUMNS,
    )

    result = transform_data(df)

    assert result.loc[0, "total_amount"] == 4000
    assert result.loc[0, "quantity"] == 2
