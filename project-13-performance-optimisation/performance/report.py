import json
from dataclasses import asdict
from pathlib import Path


def save_performance_report(result: dict, output_file: str):
    report = {
        "dataset": result["dataset"],
        "rows": result["rows"],
        "baseline": asdict(result["baseline"]),
        "optimized": asdict(result["optimized"]),
        "speedup": result["speedup"],
        "memory_before_mb": result["memory_before_mb"],
        "memory_after_mb": result["memory_after_mb"],
        "metrics": asdict(result["metrics"]),
    }

    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    return path
