import uuid
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

from alerts.console import send_all
from monitoring.logger import get_logger
from monitoring.monitor import MonitoringEngine


def load_config(path: str = "configs/monitoring.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def run_pipeline(
    input_path: str = "sample_data/sales_data.csv",
) -> dict:
    config = load_config()

    pipeline_config = config["pipeline"]
    thresholds = config["thresholds"]
    storage = config["storage"]
    logging_config = config["logging"]

    logger = get_logger(
        name=pipeline_config["name"],
        level=logging_config["level"],
        log_file=logging_config["log_file"],
    )

    pipeline_name = pipeline_config["name"]
    run_id = str(uuid.uuid4())

    started_at = datetime.now(timezone.utc)

    logger.info(
        "Pipeline started: %s",
        pipeline_name,
        extra={
            "run_id": run_id,
            "pipeline_name": pipeline_name,
        },
    )

    try:
        source = Path(input_path)

        if not source.exists():
            raise FileNotFoundError(
                f"Input file not found: {input_path}"
            )

        df = pd.read_csv(source)
        input_rows = len(df)

        invalid_amount = df["amount"] <= 0
        missing_transaction = df["transaction_id"].isna()

        invalid_mask = invalid_amount | missing_transaction

        error_count = int(invalid_mask.sum())

        clean_df = df.loc[~invalid_mask].copy()

        output_rows = len(clean_df)

        quality_score = (
            1 - (error_count / input_rows)
            if input_rows
            else 0.0
        )

        output_dir = Path("local_output")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / "processed_sales.csv"
        clean_df.to_csv(output_path, index=False)

        status = "SUCCESS"

    except Exception as exc:
        logger.exception("Pipeline failed: %s", exc)

        input_rows = 0
        output_rows = 0
        error_count = 1
        quality_score = 0.0
        status = "FAILED"

    ended_at = datetime.now(timezone.utc)

    engine = MonitoringEngine(
        pipeline_name=pipeline_name,
        thresholds=thresholds,
        metrics_file=storage["metrics_file"],
        alerts_file=storage["alerts_file"],
        logger=logger,
    )

    metrics = engine.create_metrics(
        run_id=run_id,
        status=status,
        started_at=started_at,
        ended_at=ended_at,
        input_rows=input_rows,
        output_rows=output_rows,
        error_count=error_count,
        quality_score=quality_score,
    )

    health_checks, alerts = engine.record(metrics)

    send_all(alerts)

    return {
        "metrics": metrics,
        "health_checks": health_checks,
        "alerts": alerts,
        "output_path": (
            str(output_path)
            if status == "SUCCESS"
            else None
        ),
    }
