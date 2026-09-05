import time
from datetime import datetime, timezone


class PlatformMonitor:
    """Tracks runtime, volume, quality, and platform health."""

    def __init__(
        self,
        runtime_threshold_seconds=60,
        minimum_quality_score=95,
    ):
        self.runtime_threshold_seconds = runtime_threshold_seconds
        self.minimum_quality_score = minimum_quality_score

    def start(self):
        return time.perf_counter()

    def build_metrics(
        self,
        start_time,
        input_rows,
        output_rows,
        quality_score,
        error_count=0,
    ):
        runtime_seconds = round(time.perf_counter() - start_time, 4)

        runtime_healthy = (
            runtime_seconds <= self.runtime_threshold_seconds
        )
        quality_healthy = quality_score >= self.minimum_quality_score
        errors_healthy = error_count == 0

        overall_healthy = (
            runtime_healthy
            and quality_healthy
            and errors_healthy
        )

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "runtime_seconds": runtime_seconds,
            "input_rows": int(input_rows),
            "output_rows": int(output_rows),
            "error_count": int(error_count),
            "quality_score": float(quality_score),
            "runtime_healthy": runtime_healthy,
            "quality_healthy": quality_healthy,
            "errors_healthy": errors_healthy,
            "overall_healthy": overall_healthy,
            "status": "HEALTHY" if overall_healthy else "UNHEALTHY",
        }

    def evaluate(self, metrics):
        return {
            "status": metrics["status"],
            "healthy": metrics["overall_healthy"],
            "issues": [
                issue
                for issue, condition in [
                    (
                        "Runtime threshold exceeded",
                        not metrics["runtime_healthy"],
                    ),
                    (
                        "Minimum quality score not met",
                        not metrics["quality_healthy"],
                    ),
                    (
                        "Pipeline errors detected",
                        not metrics["errors_healthy"],
                    ),
                ]
                if condition
            ],
        }
