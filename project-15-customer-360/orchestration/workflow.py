import time


class Customer360Workflow:
    """Defines and executes Customer 360 pipeline stages."""

    STAGES = [
        "ingestion",
        "standardization",
        "transaction_processing",
        "customer_enrichment",
        "profile_building",
        "segmentation",
        "analytics",
        "quality",
        "storage",
        "monitoring",
    ]

    def __init__(self, retries: int = 3, retry_delay_seconds: int = 2):
        self.retries = retries
        self.retry_delay_seconds = retry_delay_seconds

    def stage_names(self) -> list[str]:
        return self.STAGES.copy()

    def execute_stage(self, stage_name: str, function, *args, **kwargs):
        """Execute a stage with configurable retries."""

        last_error = None

        for attempt in range(1, self.retries + 1):
            try:
                return function(*args, **kwargs)
            except Exception as exc:
                last_error = exc

                if attempt < self.retries:
                    time.sleep(self.retry_delay_seconds)

        raise RuntimeError(
            f"Stage '{stage_name}' failed after "
            f"{self.retries} attempts."
        ) from last_error

    def run(self, stages: dict) -> dict:
        """Execute registered stages in the defined order."""

        results = {}

        for stage_name in self.STAGES:
            if stage_name not in stages:
                continue

            results[stage_name] = self.execute_stage(
                stage_name,
                stages[stage_name],
            )

        return results
