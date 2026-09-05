import pandas as pd

from quality.schema import validate_schema


def test_schema_passes_for_valid_dataframe():
    df = pd.DataFrame(
        {
            "transaction_id": [1],
            "customer_id": ["C001"],
            "product_id": ["P100"],
            "transaction_date": ["2026-09-04"],
            "amount": [100.0],
            "status": ["COMPLETED"],
        }
    )

    expected = {
        "transaction_id": "int64",
        "customer_id": "object",
        "product_id": "object",
        "transaction_date": "object",
        "amount": "float64",
        "status": "object",
    }

    result = validate_schema(df, expected)

    assert result.passed is True
    assert result.missing_columns == []
    assert result.type_errors == {}


def test_schema_detects_missing_column():
    df = pd.DataFrame(
        {
            "transaction_id": [1],
            "customer_id": ["C001"],
        }
    )

    expected = {
        "transaction_id": "int64",
        "customer_id": "object",
        "amount": "float64",
    }

    result = validate_schema(df, expected)

    assert result.passed is False
    assert "amount" in result.missing_columns
