from src.lakehouse_pipeline import load_raw_data, build_silver
from src.validation import validate_sales_data


def run_quality_checks():
    """Run the Silver-layer data quality checks."""
    raw = load_raw_data()
    silver = build_silver(raw)
    validate_sales_data(silver)

    print("All Silver quality checks passed.")
    print(f"Validated rows: {len(silver)}")


if __name__ == "__main__":
    run_quality_checks()
