import pandas as pd

from quality.completeness import validate_completeness


def test_completeness_passes_without_nulls():
    df = pd.DataFrame(
        {
            "customer_id": ["C001", "C002"],
            "amount": [100.0, 200.0],
        }
    )

    result = validate_completeness(
        df,
        ["customer_id", "amount"],
        minimum_score=0.95,
    )

    assert result.passed is True
    assert result.score == 1.0


def test_completeness_detects_nulls():
    df = pd.DataFrame(
        {
            "customer_id": ["C001", None],
            "amount": [100.0, 200.0],
        }
    )

    result = validate_completeness(
        df,
        ["customer_id", "amount"],
        minimum_score=0.95,
    )

    assert result.passed is False
    assert result.null_counts["customer_id"] == 1
