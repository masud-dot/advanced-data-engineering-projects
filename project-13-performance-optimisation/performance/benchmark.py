from dataclasses import dataclass
from time import perf_counter
from typing import Callable, Any


@dataclass
class BenchmarkResult:
    name: str
    average_seconds: float
    minimum_seconds: float
    maximum_seconds: float
    iterations: int


def benchmark(
    func: Callable[..., Any],
    *args: Any,
    name: str = "benchmark",
    iterations: int = 3,
    warmup_runs: int = 1,
    **kwargs: Any,
) -> BenchmarkResult:
    for _ in range(warmup_runs):
        func(*args, **kwargs)

    durations = []

    for _ in range(iterations):
        start = perf_counter()
        func(*args, **kwargs)
        durations.append(perf_counter() - start)

    return BenchmarkResult(
        name=name,
        average_seconds=sum(durations) / len(durations),
        minimum_seconds=min(durations),
        maximum_seconds=max(durations),
        iterations=iterations,
    )
