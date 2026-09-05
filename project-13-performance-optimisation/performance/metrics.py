from dataclasses import dataclass


@dataclass
class PerformanceMetrics:
    rows_processed: int
    runtime_seconds: float
    throughput_rows_per_second: float
    memory_mb: float


def calculate_metrics(
    rows_processed: int,
    runtime_seconds: float,
    memory_mb: float,
) -> PerformanceMetrics:
    throughput = (
        rows_processed / runtime_seconds
        if runtime_seconds > 0
        else 0.0
    )

    return PerformanceMetrics(
        rows_processed=rows_processed,
        runtime_seconds=runtime_seconds,
        throughput_rows_per_second=throughput,
        memory_mb=memory_mb,
    )
