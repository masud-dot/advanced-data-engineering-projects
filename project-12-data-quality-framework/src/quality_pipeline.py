from pipelines.quality_pipeline import run_quality_pipeline


if __name__ == "__main__":
    result = run_quality_pipeline()

    print("=" * 60)
    print("DATA QUALITY FRAMEWORK")
    print("=" * 60)
    print(f"Dataset       : {result['dataset']}")
    print(f"Rows          : {result['rows']}")
    print(f"Quality Score : {result['quality_score']:.2%}")
    print(
        f"Overall Status: "
        f"{'PASS' if result['passed'] else 'FAIL'}"
    )
    print(f"Report        : {result['report_file']}")
    print("=" * 60)
