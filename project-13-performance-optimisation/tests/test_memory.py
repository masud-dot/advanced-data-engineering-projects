import pandas as pd

from performance.memory import (
    memory_usage_mb,
    optimize_dataframe_memory,
)


def test_memory_usage_is_positive():
    df = pd.DataFrame(
        {
            "id": range(100),
            "category": ["A", "B"] * 50,
        }
    )

    assert memory_usage_mb(df) > 0


def test_memory_optimization_reduces_or_preserves_memory():
    df = pd.DataFrame(
        {
            "id": range(1000),
            "category": ["A", "B", "C", "D"] * 250,
        }
    )

    before = memory_usage_mb(df)
    optimized = optimize_dataframe_memory(df)
    after = memory_usage_mb(optimized)

    assert after <= before
