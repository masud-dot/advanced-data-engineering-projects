from dataclasses import dataclass

import pandas as pd


@dataclass
class ReferentialIntegrityResult:
    passed: bool
    invalid_count: int
    message: str


def validate_referential_integrity(
    df: pd.DataFrame,
    source_column: str,
    reference_df: pd.DataFrame,
    reference_column: str,
) -> ReferentialIntegrityResult:
    if source_column not in df.columns:
        return ReferentialIntegrityResult(
            passed=False,
            invalid_count=0,
            message=(
                "Referential integrity validation failed: "
                f"missing source column {source_column}."
            ),
        )

    if reference_column not in reference_df.columns:
        return ReferentialIntegrityResult(
            passed=False,
            invalid_count=0,
            message=(
                "Referential integrity validation failed: "
                f"missing reference column {reference_column}."
            ),
        )

    valid_values = set(reference_df[reference_column].dropna())

    invalid_count = int(
        (~df[source_column].isin(valid_values)).sum()
    )

    passed = invalid_count == 0

    return ReferentialIntegrityResult(
        passed=passed,
        invalid_count=invalid_count,
        message=(
            "Referential integrity validation passed."
            if passed
            else (
                "Referential integrity validation failed: "
                f"{invalid_count} invalid references detected."
            )
        ),
    )
