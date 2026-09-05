from pathlib import Path
from time import perf_counter

import pandas as pd
import yaml

from performance.benchmark import benchmark
from performance.memory import memory_usage_mb, optimize_dataframe_memory
from performance.metrics import calculate_metrics
from performance.report import save_performance_report
from performance.vectorization import (
    apply_vectorized_discount,
    classify_amount_vectorized,
)


BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_FILE = BASE_DIR / "configs" / "performance.yaml"
DATA_FILE = BASE_DIR / "sample_data" / "sales_data.csv"


def load_config():
    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_FILE)


def baseline_transform(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    result["discount_rate"] = 0.10

    result["discounted_amount"] = result.apply(
        lambda row: row["amount"]
        * (1 - row["discount_rate"]),
        axis=1,
    )

    result["amount_category"] = result["amount"].apply(
        lambda amount:
        "LOW"
        if amount <= 500
        else "MEDIUM"
        if amount <= 1000
        else "HIGH"
    )

    return result


def optimized_transform(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    result["discount_rate"] = 0.10

    result = apply_vectorized_discount(
        result,
        amount_column="amount",
        discount_column="discount_rate",
    )

    result = classify_amount_vectorized(
        result,
        amount_column="amount",
    )

    return result


def run_performance_pipeline():
    config = load_config()
    df = load_data()

    iterations = config["benchmark"]["iterations"]
    warmup_runs = config["benchmark"]["warmup_runs"]

    baseline = benchmark(
        baseline_transform,
        df,
        name="baseline_transform",
        iterations=iterations,
        warmup_runs=warmup_runs,
    )

    optimized = benchmark(
        optimized_transform,
        df,
        name="optimized_transform",
        iterations=iterations,
        warmup_runs=warmup_runs,
    )

    start = perf_counter()

    optimized_df = optimized_transform(df)

    runtime = perf_counter() - start

    memory_before = memory_usage_mb(df)

    optimized_memory_df = optimize_dataframe_memory(
        optimized_df
    )

    memory_after = memory_usage_mb(
        optimized_memory_df
    )

    metrics = calculate_metrics(
        rows_processed=len(optimized_df),
        runtime_seconds=runtime,
        memory_mb=memory_after,
    )

    speedup = (
        baseline.average_seconds
        / optimized.average_seconds
        if optimized.average_seconds > 0
        else 0.0
    )

    result = {
        "dataset": DATA_FILE.name,
        "rows": len(df),
        "baseline": baseline,
        "optimized": optimized,
        "speedup": speedup,
        "memory_before_mb": memory_before,
        "memory_after_mb": memory_after,
        "metrics": metrics,
    }

    save_performance_report(
        result,
        BASE_DIR / "local_output" / "performance_report.json",
    )

    return result


if __name__ == "__main__":
    result = run_performance_pipeline()

    print(
        f"Report              : "
        f"{BASE_DIR / "local_output" / "performance_report.json"}"
    )
    print("=" * 65)
    print("PIPELINE PERFORMANCE OPTIMISATION")
    print("=" * 65)
    print(f"Dataset             : {result['dataset']}")
    print(f"Rows                : {result['rows']}")
    print("-" * 65)
    print(
        f"Baseline Avg        : "
        f"{result['baseline'].average_seconds:.6f} sec"
    )
    print(
        f"Optimized Avg       : "
        f"{result['optimized'].average_seconds:.6f} sec"
    )
    print(
        f"Speedup             : "
        f"{result['speedup']:.2f}x"
    )
    print("-" * 65)
    print(
        f"Memory Before       : "
        f"{result['memory_before_mb']:.4f} MB"
    )
    print(
        f"Memory After        : "
        f"{result['memory_after_mb']:.4f} MB"
    )
    print("-" * 65)
    print(
        f"Throughput          : "
        f"{result['metrics'].throughput_rows_per_second:.2f} "
        f"rows/sec"
    )
    print("=" * 65)
