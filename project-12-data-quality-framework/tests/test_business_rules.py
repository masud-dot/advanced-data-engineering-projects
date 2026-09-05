import pandas as pd

from quality.business_rules import validate_business_rules


def test_business_rules_pass_for_valid_data():
    df = pd.DataFrame(
        {
            "amount": [100.0, 200.0],
            "status": ["COMPLETED", "REFUNDED"],
        }
    )

    result = validate_business_rules(
        df,
        amount_min=0,
        allowed_statuses=[
            "COMPLETED",
            "CANCELLED",
            "REFUNDED",
        ],
    )

    assert result.passed is True
    assert result.violation_count == 0


def test_business_rules_detect_invalid_values():
    df = pd.DataFrame(
        {
            "amount": [-100.0],
            "status": ["INVALID"],
        }
    )

    result = validate_business_rules(
        df,
        amount_min=0,
        allowed_statuses=[
            "COMPLETED",
            "CANCELLED",
            "REFUNDED",
        ],
    )

    assert result.passed is False
    assert result.violation_count == 2
