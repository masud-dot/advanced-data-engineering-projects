from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class HealthCheck:
    name: str
    status: str
    message: str

    @property
    def healthy(self) -> bool:
        return self.status == "HEALTHY"


def check_output_volume(
    output_rows: int,
    minimum_rows: int,
) -> HealthCheck:
    if output_rows >= minimum_rows:
        return HealthCheck(
            name="output_volume",
            status="HEALTHY",
            message=f"Output row count is {output_rows}.",
        )

    return HealthCheck(
        name="output_volume",
        status="UNHEALTHY",
        message=(
            f"Output row count {output_rows} is below "
            f"minimum {minimum_rows}."
        ),
    )


def check_error_rate(
    input_rows: int,
    error_count: int,
    maximum_rate: float,
) -> HealthCheck:
    if input_rows <= 0:
        return HealthCheck(
            name="error_rate",
            status="UNHEALTHY",
            message="No input rows were processed.",
        )

    error_rate = error_count / input_rows

    if error_rate <= maximum_rate:
        return HealthCheck(
            name="error_rate",
            status="HEALTHY",
            message=f"Error rate is {error_rate:.2%}.",
        )

    return HealthCheck(
        name="error_rate",
        status="UNHEALTHY",
        message=(
            f"Error rate {error_rate:.2%} exceeds "
            f"maximum {maximum_rate:.2%}."
        ),
    )


def check_duration(
    duration_seconds: float,
    maximum_seconds: float,
) -> HealthCheck:
    if duration_seconds <= maximum_seconds:
        return HealthCheck(
            name="duration",
            status="HEALTHY",
            message=f"Pipeline duration is {duration_seconds:.3f} seconds.",
        )

    return HealthCheck(
        name="duration",
        status="UNHEALTHY",
        message=(
            f"Pipeline duration {duration_seconds:.3f} seconds exceeds "
            f"maximum {maximum_seconds} seconds."
        ),
    )


def check_quality_score(
    quality_score: float,
    minimum_score: float,
) -> HealthCheck:
    if quality_score >= minimum_score:
        return HealthCheck(
            name="quality_score",
            status="HEALTHY",
            message=f"Quality score is {quality_score:.2%}.",
        )

    return HealthCheck(
        name="quality_score",
        status="UNHEALTHY",
        message=(
            f"Quality score {quality_score:.2%} is below "
            f"minimum {minimum_score:.2%}."
        ),
    )


def check_freshness(
    last_success: Optional[datetime],
    threshold_minutes: float,
) -> HealthCheck:
    if last_success is None:
        return HealthCheck(
            name="freshness",
            status="UNHEALTHY",
            message="No successful pipeline execution found.",
        )

    now = datetime.now(timezone.utc)

    if last_success.tzinfo is None:
        last_success = last_success.replace(tzinfo=timezone.utc)

    age_minutes = (now - last_success).total_seconds() / 60

    if age_minutes <= threshold_minutes:
        return HealthCheck(
            name="freshness",
            status="HEALTHY",
            message=f"Last successful run is {age_minutes:.1f} minutes old.",
        )

    return HealthCheck(
        name="freshness",
        status="UNHEALTHY",
        message=(
            f"Last successful run is {age_minutes:.1f} minutes old, "
            f"exceeding threshold {threshold_minutes} minutes."
        ),
    )
