from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class DuplicateResult:
    passed: bool
    duplicate_count: int
    message: str


def validate_duplicates(
    df: pd.DataFrame,
    key_columns: List[str],
) -> DuplicateResult:
    missing_columns = [
        column for column in key_columns
        if column not in df.columns
    ]

    if missing_columns:
        return DuplicateResult(
            passed=False,
            duplicate_count=0,
            message=(
                "Duplicate validation failed: "
                f"missing key columns {missing_columns}."
            ),
        )

    duplicate_count = int(
        df.duplicated(subset=key_columns, keep=False).sum()
    )

    passed = duplicate_count == 0

    return DuplicateResult(
        passed=passed,
        duplicate_count=duplicate_count,
        message=(
            "Duplicate validation passed."
            if passed
            else (
                "Duplicate validation failed: "
                f"{duplicate_count} duplicate rows detected."
            )
        ),
    )
