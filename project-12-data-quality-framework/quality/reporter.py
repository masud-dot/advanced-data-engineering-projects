import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict


def build_quality_report(
    dataset_name: str,
    row_count: int,
    checks: Dict[str, Any],
    quality_score: float,
    passed: bool,
) -> Dict[str, Any]:
    return {
        "dataset": dataset_name,
        "row_count": row_count,
        "quality_score": quality_score,
        "status": "PASS" if passed else "FAIL",
        "checks": checks,
    }


def save_quality_report(
    report: Dict[str, Any],
    output_file: str = "local_output/quality_report.json",
) -> None:
    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    def serialize(value):
        if hasattr(value, "__dataclass_fields__"):
            return asdict(value)
        raise TypeError(
            f"Object of type {type(value).__name__} is not JSON serializable"
        )

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=2,
            default=serialize,
        )
