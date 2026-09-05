import time


class Customer360Monitor:
    """Monitors Customer 360 pipeline execution and quality."""

    def __init__(
        self,
        runtime_threshold_seconds: float = 60,
        minimum_quality_score: float = 95,
    ):
        self.runtime_threshold_seconds = runtime_threshold_seconds
        self.minimum_quality_score = minimum_quality_score

    def start(self) -> float:
        return time.perf_counter()

    def finish(
        self,
        start_time: float,
        input_records: int,
        output_records: int,
        quality_score: float,
    ) -> dict:
        runtime = time.perf_counter() - start_time

        alerts = []

        if runtime > self.runtime_threshold_seconds:
            alerts.append(
                f"Runtime exceeded threshold: "
                f"{runtime:.2f}s > "
                f"{self.runtime_threshold_seconds:.2f}s"
            )

        if quality_score < self.minimum_quality_score:
            alerts.append(
                f"Quality score below threshold: "
                f"{quality_score:.2f}% < "
                f"{self.minimum_quality_score:.2f}%"
            )

        if output_records == 0:
            alerts.append("Pipeline produced zero output records.")

        return {
            "runtime_seconds": round(runtime, 4),
            "input_records": int(input_records),
            "output_records": int(output_records),
            "quality_score": round(float(quality_score), 2),
            "status": "SUCCESS" if not alerts else "WARNING",
            "alerts": alerts,
        }

    def check_quality(self, quality_score: float) -> bool:
        return quality_score >= self.minimum_quality_score

    def check_runtime(self, runtime_seconds: float) -> bool:
        return runtime_seconds <= self.runtime_threshold_seconds
