from datetime import datetime, timezone

from monitoring.metrics import (
    PipelineMetrics,
    calculate_duration,
    calculate_quality_score,
)


def test_calculate_duration():
    start = datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    end = datetime(2026, 1, 1, 10, 0, 5, tzinfo=timezone.utc)

    assert calculate_duration(start, end) == 5.0


def test_quality_score():
    assert calculate_quality_score(100, 0) == 1.0
    assert calculate_quality_score(100, 10) == 0.9
    assert calculate_quality_score(0, 0) == 0.0


def test_metrics_to_dict():
    metrics = PipelineMetrics(
        run_id="run-001",
        pipeline_name="sales_pipeline",
        status="SUCCESS",
        started_at="2026-01-01T10:00:00+00:00",
        ended_at="2026-01-01T10:00:05+00:00",
        duration_seconds=5.0,
        input_rows=100,
        output_rows=100,
        error_count=0,
        quality_score=1.0,
    )

    data = metrics.to_dict()

    assert data["run_id"] == "run-001"
    assert data["status"] == "SUCCESS"
    assert data["quality_score"] == 1.0
