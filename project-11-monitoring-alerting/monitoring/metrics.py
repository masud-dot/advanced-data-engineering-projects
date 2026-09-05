from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Optional


@dataclass
class PipelineMetrics:
    run_id: str
    pipeline_name: str
    status: str
    started_at: str
    ended_at: str
    duration_seconds: float
    input_rows: int
    output_rows: int
    error_count: int
    quality_score: float

    def to_dict(self) -> dict:
        return asdict(self)

    def save(self, path: str) -> None:
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

        records.append(self.to_dict())
        target.write_text(
            json.dumps(records, indent=2),
            encoding="utf-8",
        )


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def calculate_duration(started_at: datetime, ended_at: datetime) -> float:
    return round((ended_at - started_at).total_seconds(), 3)


def calculate_quality_score(
    input_rows: int,
    error_count: int,
) -> float:
    if input_rows <= 0:
        return 0.0

    score = 1 - (error_count / input_rows)
    return round(max(0.0, min(1.0, score)), 4)


def load_metrics(path: str) -> list[dict]:
    target = Path(path)

    if not target.exists():
        return []

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []
