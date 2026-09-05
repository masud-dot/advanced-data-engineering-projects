from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class CompletenessResult:
    passed: bool
    score: float
    message: str
    null_counts: dict


def validate_completeness(
    df: pd.DataFrame,
    required_columns: List[str],
    minimum_score: float = 0.95,
) -> CompletenessResult:
    if df.empty:
        return CompletenessResult(
            passed=False,
            score=0.0,
            message="Completeness validation failed: dataset is empty.",
            null_counts={},
        )

    null_counts = {
        column: int(df[column].isna().sum())
        for column in required_columns
        if column in df.columns
    }

    total_cells = len(df) * len(required_columns)
    missing_cells = sum(null_counts.values())

    score = (
        1.0 - (missing_cells / total_cells)
        if total_cells
        else 0.0
    )

    passed = score >= minimum_score

    return CompletenessResult(
        passed=passed,
        score=round(score, 4),
        message=(
            "Completeness validation passed."
            if passed
            else "Completeness validation failed."
        ),
        null_counts=null_counts,
    )
