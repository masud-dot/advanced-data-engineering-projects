from pathlib import Path
from typing import Any, Dict

import pandas as pd

from quality.engine import DataQualityEngine
from quality.reporter import build_quality_report, save_quality_report


BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_FILE = BASE_DIR / "configs" / "quality_rules.yaml"
SALES_FILE = BASE_DIR / "sample_data" / "sales_data.csv"
CUSTOMERS_FILE = BASE_DIR / "sample_data" / "customers.csv"
REPORT_FILE = BASE_DIR / "local_output" / "quality_report.json"


def run_quality_pipeline() -> Dict[str, Any]:
    sales_df = pd.read_csv(SALES_FILE)
    customers_df = pd.read_csv(CUSTOMERS_FILE)

    engine = DataQualityEngine(str(CONFIG_FILE))

    result = engine.validate(
        sales_df,
        reference_data={
            "customer_id": customers_df,
        },
    )

    quality_score = result["quality_score"]

    report = build_quality_report(
        dataset_name=result["dataset"],
        row_count=result["row_count"],
        checks=result["checks"],
        quality_score=quality_score.score,
        passed=result["passed"],
    )

    save_quality_report(
        report,
        str(REPORT_FILE),
    )

    return {
        "dataset": result["dataset"],
        "rows": result["row_count"],
        "quality_score": quality_score.score,
        "passed": result["passed"],
        "report_file": str(REPORT_FILE),
        "checks": result["checks"],
    }


if __name__ == "__main__":
    result = run_quality_pipeline()

    print("=" * 60)
    print("DATA QUALITY VALIDATION")
    print("=" * 60)
    print(f"Dataset       : {result['dataset']}")
    print(f"Rows          : {result['rows']}")
    print(f"Quality Score : {result['quality_score']:.2%}")
    print(f"Status        : {'PASS' if result['passed'] else 'FAIL'}")
    print("-" * 60)

    for name, check in result["checks"].items():
        if check is None:
            continue

        status = "PASS" if check.passed else "FAIL"
        print(f"{name:<25} {status}")
        print(f"  {check.message}")

    print("-" * 60)
    print(f"Report        : {result['report_file']}")
    print("=" * 60)
