from monitoring.alerts import evaluate_metrics


THRESHOLDS = {
    "max_duration_seconds": 30,
    "max_error_count": 0,
    "min_output_rows": 1,
    "min_quality_score": 0.95,
}


def test_no_alerts_for_healthy_pipeline():
    alerts = evaluate_metrics(
        pipeline_name="sales_pipeline",
        run_id="run-001",
        duration_seconds=5,
        error_count=0,
        output_rows=100,
        quality_score=1.0,
        thresholds=THRESHOLDS,
    )

    assert alerts == []


def test_alert_for_slow_pipeline():
    alerts = evaluate_metrics(
        pipeline_name="sales_pipeline",
        run_id="run-002",
        duration_seconds=50,
        error_count=0,
        output_rows=100,
        quality_score=1.0,
        thresholds=THRESHOLDS,
    )

    assert len(alerts) == 1
    assert alerts[0].severity == "WARNING"
    assert alerts[0].rule == "duration_threshold"


def test_alerts_for_quality_and_errors():
    alerts = evaluate_metrics(
        pipeline_name="sales_pipeline",
        run_id="run-003",
        duration_seconds=5,
        error_count=5,
        output_rows=95,
        quality_score=0.90,
        thresholds=THRESHOLDS,
    )

    rules = {alert.rule for alert in alerts}

    assert "error_threshold" in rules
    assert "quality_threshold" in rules


def test_alert_for_zero_output():
    alerts = evaluate_metrics(
        pipeline_name="sales_pipeline",
        run_id="run-004",
        duration_seconds=5,
        error_count=0,
        output_rows=0,
        quality_score=1.0,
        thresholds=THRESHOLDS,
    )

    assert len(alerts) == 1
    assert alerts[0].severity == "CRITICAL"
    assert alerts[0].rule == "volume_threshold"
