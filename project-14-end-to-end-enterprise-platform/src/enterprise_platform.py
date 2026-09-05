import json
from pathlib import Path

from pipelines.enterprise_platform import EnterpriseDataPlatform


def main():
    platform = EnterpriseDataPlatform()
    result = platform.run()

    report_path = Path("data_lake/platform_run_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(result, indent=2, default=str),
        encoding="utf-8",
    )

    print("Enterprise Data Platform")
    print("========================")
    print(f"Status: {result['status']}")
    print(f"Quality Score: {result['quality']['score']}%")
    print(f"Orders: {result['warehouse']['fact_orders']}")
    print(f"Customers: {result['warehouse']['dim_customer']}")
    print(f"Products: {result['warehouse']['dim_product']}")
    print(f"Runtime: {result['monitoring']['runtime_seconds']} seconds")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
