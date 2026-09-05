from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class BusinessRuleResult:
    passed: bool
    violation_count: int
    message: str
    violations: List[str]


def validate_business_rules(
    df: pd.DataFrame,
    amount_min: float = 0,
    allowed_statuses: List[str] | None = None,
) -> BusinessRuleResult:
    violations = []

    if "amount" in df.columns:
        invalid_amounts = df["amount"].isna() | (df["amount"] < amount_min)

        count = int(invalid_amounts.sum())

        if count:
            violations.append(
                f"{count} rows contain invalid amount values."
            )

    if "status" in df.columns and allowed_statuses:
        invalid_statuses = ~df["status"].isin(allowed_statuses)
        count = int(invalid_statuses.sum())

        if count:
            violations.append(
                f"{count} rows contain invalid status values."
            )

    violation_count = 0

    if "amount" in df.columns:
        violation_count += int(
            (df["amount"].isna() | (df["amount"] < amount_min)).sum()
        )

    if "status" in df.columns and allowed_statuses:
        violation_count += int(
            (~df["status"].isin(allowed_statuses)).sum()
        )

    passed = violation_count == 0

    return BusinessRuleResult(
        passed=passed,
        violation_count=violation_count,
        message=(
            "Business-rule validation passed."
            if passed
            else "Business-rule validation failed."
        ),
        violations=violations,
    )
