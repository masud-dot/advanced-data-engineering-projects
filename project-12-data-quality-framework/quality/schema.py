from dataclasses import dataclass
from typing import Dict, List

import pandas as pd


@dataclass
class SchemaResult:
    passed: bool
    message: str
    missing_columns: List[str]
    type_errors: Dict[str, str]


def validate_schema(
    df: pd.DataFrame,
    expected_columns: Dict[str, str],
) -> SchemaResult:
    missing = [
        column for column in expected_columns
        if column not in df.columns
    ]

    type_errors = {}

    for column, expected_type in expected_columns.items():
        if column not in df.columns:
            continue

        actual_type = str(df[column].dtype)

        if actual_type != expected_type:
            type_errors[column] = (
                f"expected {expected_type}, found {actual_type}"
            )

    passed = not missing and not type_errors

    if passed:
        message = "Schema validation passed."
    else:
        message = "Schema validation failed."

    return SchemaResult(
        passed=passed,
        message=message,
        missing_columns=missing,
        type_errors=type_errors,
    )
