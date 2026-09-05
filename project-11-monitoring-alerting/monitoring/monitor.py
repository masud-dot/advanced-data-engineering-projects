from datetime import datetime
from typing import Any

from monitoring.alerts import Alert, evaluate_metrics, save_alerts
from monitoring.health import (
    HealthCheck,
    check_duration,
    check_error_rate,
    check_output_volume,
    check_quality_score,
)
from monitoring.metrics import PipelineMetrics


class MonitoringEngine:
    def __init__(
        self,
        pipeline_name: str,
        thresholds: dict[str, Any],
        metrics_file: str,
        alerts_file: str,
        logger,
    ):
        self.pipeline_name = pipeline_name
        self.thresholds = thresholds
        self.metrics_file = metrics_file
        self.alerts_file = alerts_file
        self.logger = logger

    def create_metrics(
        self,
        run_id: str,
        status: str,
        started_at: datetime,
        ended_at: datetime,
        input_rows: int,
        output_rows: int,
        error_count: int,
        quality_score: float,
    ) -> PipelineMetrics:
        duration = (ended_at - started_at).total_seconds()

        return PipelineMetrics(
            run_id=run_id,
            pipeline_name=self.pipeline_name,
            status=status,
            started_at=started_at.isoformat(),
            ended_at=ended_at.isoformat(),
            duration_seconds=round(duration, 3),
            input_rows=input_rows,
            output_rows=output_rows,
            error_count=error_count,
            quality_score=quality_score,
        )

    def run_health_checks(
        self,
        metrics: PipelineMetrics,
    ) -> list[HealthCheck]:
        return [
            check_output_volume(
                metrics.output_rows,
                self.thresholds["min_output_rows"],
            ),
            check_error_rate(
                metrics.input_rows,
                metrics.error_count,
                self.thresholds["max_error_rate"],
            ),
            check_duration(
                metrics.duration_seconds,
                self.thresholds["max_duration_seconds"],
            ),
            check_quality_score(
                metrics.quality_score,
                self.thresholds["min_quality_score"],
            ),
        ]

    def evaluate_alerts(
        self,
        metrics: PipelineMetrics,
    ) -> list[Alert]:
        alerts = evaluate_metrics(
            pipeline_name=metrics.pipeline_name,
            run_id=metrics.run_id,
            duration_seconds=metrics.duration_seconds,
            error_count=metrics.error_count,
            output_rows=metrics.output_rows,
            quality_score=metrics.quality_score,
            thresholds=self.thresholds,
        )

        if alerts:
            save_alerts(alerts, self.alerts_file)

        return alerts

    def record(
        self,
        metrics: PipelineMetrics,
    ) -> tuple[list[HealthCheck], list[Alert]]:
        metrics.save(self.metrics_file)

        health_checks = self.run_health_checks(metrics)
        alerts = self.evaluate_alerts(metrics)

        self.logger.info(
            "Monitoring completed: status=%s input_rows=%s output_rows=%s "
            "errors=%s quality=%.2f duration=%.3fs alerts=%s",
            metrics.status,
            metrics.input_rows,
            metrics.output_rows,
            metrics.error_count,
            metrics.quality_score,
            metrics.duration_seconds,
            len(alerts),
        )

        return health_checks, alerts
