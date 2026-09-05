from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path


@dataclass
class Alert:
    alert_id: str
    pipeline_name: str
    severity: str
    rule: str
    message: str
    created_at: str

    def to_dict(self) -> dict:
        return asdict(self)


def evaluate_metrics(
    pipeline_name: str,
    run_id: str,
    duration_seconds: float,
    error_count: int,
    output_rows: int,
    quality_score: float,
    thresholds: dict,
) -> list[Alert]:
    alerts = []

    def create_alert(severity: str, rule: str, message: str) -> None:
        alert_id = f"{run_id}-{rule}"
        alerts.append(
            Alert(
                alert_id=alert_id,
                pipeline_name=pipeline_name,
                severity=severity,
                rule=rule,
                message=message,
                created_at=datetime.now(timezone.utc).isoformat(),
            )
        )

    if duration_seconds > thresholds["max_duration_seconds"]:
        create_alert(
            "WARNING",
            "duration_threshold",
            (
                f"Duration {duration_seconds:.3f}s exceeds "
                f"{thresholds['max_duration_seconds']}s."
            ),
        )

    if error_count > thresholds["max_error_count"]:
        create_alert(
            "CRITICAL",
            "error_threshold",
            f"Error count {error_count} exceeds allowed maximum.",
        )

    if output_rows < thresholds["min_output_rows"]:
        create_alert(
            "CRITICAL",
            "volume_threshold",
            f"Output rows {output_rows} are below minimum.",
        )

    if quality_score < thresholds["min_quality_score"]:
        create_alert(
            "CRITICAL",
            "quality_threshold",
            (
                f"Quality score {quality_score:.2%} is below "
                f"minimum {thresholds['min_quality_score']:.2%}."
            ),
        )

    return alerts


def save_alerts(alerts: list[Alert], path: str) -> None:
    if not alerts:
        return

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    records = []

    if target.exists():
        try:
            records = json.loads(target.read_text(encoding="utf-8"))
            if not isinstance(records, list):
                records = []
        except (json.JSONDecodeError, OSError):
            records = []

    records.extend(alert.to_dict() for alert in alerts)

    target.write_text(
        json.dumps(records, indent=2),
        encoding="utf-8",
    )
