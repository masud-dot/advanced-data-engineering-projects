from pipelines.performance_pipeline import (
    run_performance_pipeline,
)


def test_performance_pipeline():
    result = run_performance_pipeline()

    assert result["rows"] == 10000
    assert result["baseline"].average_seconds >= 0
    assert result["optimized"].average_seconds >= 0
    assert result["speedup"] > 0
    assert result["memory_before_mb"] > 0
    assert result["memory_after_mb"] > 0
    assert (
        result["metrics"].throughput_rows_per_second > 0
    )
