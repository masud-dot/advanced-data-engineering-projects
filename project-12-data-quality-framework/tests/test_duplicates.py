import pandas as pd

from quality.duplicates import validate_duplicates


def test_duplicates_pass_for_unique_keys():
    df = pd.DataFrame(
        {
            "transaction_id": [1, 2, 3],
            "amount": [100.0, 200.0, 300.0],
        }
    )

    result = validate_duplicates(
        df,
        ["transaction_id"],
    )

    assert result.passed is True
    assert result.duplicate_count == 0


def test_duplicates_detect_duplicate_keys():
    df = pd.DataFrame(
        {
            "transaction_id": [1, 2, 2],
            "amount": [100.0, 200.0, 300.0],
        }
    )

    result = validate_duplicates(
        df,
        ["transaction_id"],
    )

    assert result.passed is False
    assert result.duplicate_count == 2
