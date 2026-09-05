import pandas as pd
import pytest

from src.incremental_pipeline import extract_incremental_data
from src.transformations import clean_incremental_data
from src.validation import validate_incremental_data


def sample_dataframe():
    return pd.DataFrame(
        [
            {
                "transaction_id": 1,
                "customer_id": 101,
                "amount": 100.00,
                "created_at": "2026-01-10 10:00:00",
                "updated_at": "2026-01-10 10:00:00",
            },
            {
                "transaction_id": 2,
                "customer_id": 102,
                "amount": 200.00,
                "created_at": "2026-01-20 10:00:00",
                "updated_at": "2026-01-20 10:00:00",
            },
        ]
    )


def test_incremental_filter():
    df = sample_dataframe()

    result = extract_incremental_data(
        df,
        "2026-01-15 00:00:00",
    )

    assert len(result) == 1
    assert result.iloc[0]["transaction_id"] == 2


def test_transformation():
    df = sample_dataframe()

    result = clean_incremental_data(df)

    assert "year" in result.columns
    assert "month" in result.columns
    assert "day" in result.columns
    assert len(result) == 2


def test_validation_rejects_negative_amount():
    df = sample_dataframe()
    df.loc[0, "amount"] = -10

    cleaned = clean_incremental_data(df)

    with pytest.raises(ValueError):
        validate_incremental_data(cleaned)
