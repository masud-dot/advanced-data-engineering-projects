from pathlib import Path

from pipelines.monitored_pipeline import run_pipeline


def test_pipeline_execution(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    Path("configs").mkdir()
    Path("sample_data").mkdir()

    Path("configs/monitoring.yaml").write_text(
        """
pipeline:
  name: test_sales_pipeline
  freshness_threshold_minutes: 60
  max_error_rate: 0.10
  min_output_rows: 1

alerts:
  enabled: true
  severity_levels:
    - INFO
    - WARNING
    - CRITICAL

thresholds:
  max_error_rate: 0.10
  max_duration_seconds: 30
  max_error_count: 0
  min_quality_score: 0.95
  min_output_rows: 1

logging:
  level: INFO
  log_file: local_output/pipeline.log

storage:
  metrics_file: local_output/metrics.json
  alerts_file: local_output/alerts.json
""",
        encoding="utf-8",
    )

    Path("sample_data/sales_data.csv").write_text(
        """transaction_id,customer_id,product_id,region,amount,status
1001,C001,P100,East,100.00,COMPLETED
1002,C002,P200,West,200.00,COMPLETED
1003,C003,P300,North,300.00,COMPLETED
""",
        encoding="utf-8",
    )

    result = run_pipeline()

    assert result["metrics"].status == "SUCCESS"
    assert result["metrics"].input_rows == 3
    assert result["metrics"].output_rows == 3
    assert result["metrics"].error_count == 0
    assert result["metrics"].quality_score == 1.0

    assert Path("local_output/processed_sales.csv").exists()
    assert Path("local_output/metrics.json").exists()
