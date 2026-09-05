from pipelines.monitored_pipeline import run_pipeline


def main() -> None:
    result = run_pipeline()

    metrics = result["metrics"]

    print("\n=== PIPELINE MONITORING SUMMARY ===")
    print(f"Pipeline       : {metrics.pipeline_name}")
    print(f"Run ID         : {metrics.run_id}")
    print(f"Status         : {metrics.status}")
    print(f"Input rows     : {metrics.input_rows}")
    print(f"Output rows    : {metrics.output_rows}")
    print(f"Errors         : {metrics.error_count}")
    print(f"Quality score  : {metrics.quality_score:.2%}")
    print(f"Duration       : {metrics.duration_seconds:.3f}s")

    print("\nHealth Checks:")
    for check in result["health_checks"]:
        print(f"- {check.name}: {check.status} — {check.message}")

    print(f"\nAlerts generated: {len(result['alerts'])}")

    if result["output_path"]:
        print(f"Output file    : {result['output_path']}")


if __name__ == "__main__":
    main()
