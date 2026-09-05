from dataclasses import dataclass
from datetime import datetime, timezone

import pandas as pd


@dataclass
class FreshnessResult:
    passed: bool
    age_days: float
    message: str


def validate_freshness(
    df: pd.DataFrame,
    timestamp_column: str,
    max_age_days: int,
) -> FreshnessResult:
    if timestamp_column not in df.columns or df.empty:
        return FreshnessResult(
            passed=False,
            age_days=float("inf"),
            message="Freshness validation failed: timestamp data unavailable.",
        )

    timestamps = pd.to_datetime(
        df[timestamp_column],
        errors="coerce",
        utc=True,
    ).dropna()

    if timestamps.empty:
        return FreshnessResult(
            passed=False,
            age_days=float("inf"),
            message="Freshness validation failed: no valid timestamps.",
        )

    latest_timestamp = timestamps.max()
    now = pd.Timestamp(datetime.now(timezone.utc))

    age_days = max(
        0.0,
        (now - latest_timestamp).total_seconds() / 86400,
    )

    passed = age_days <= max_age_days

    return FreshnessResult(
        passed=passed,
        age_days=round(age_days, 4),
        message=(
            "Freshness validation passed."
            if passed
            else "Freshness validation failed."
        ),
    )
