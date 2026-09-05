from performance.benchmark import benchmark


def test_benchmark_returns_valid_result():
    def operation():
        return sum(range(100))

    result = benchmark(
        operation,
        name="test_operation",
        iterations=2,
        warmup_runs=1,
    )

    assert result.name == "test_operation"
    assert result.iterations == 2
    assert result.average_seconds >= 0
    assert result.minimum_seconds >= 0
    assert result.maximum_seconds >= result.minimum_seconds
