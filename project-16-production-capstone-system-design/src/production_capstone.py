from pipelines.production_pipeline import ProductionCapstonePipeline


def main():
    pipeline = ProductionCapstonePipeline()
    result = pipeline.run()

    quality = result["quality"]
    executive = result["executive_metrics"]
    metrics = result["metrics"]

    print()
    print("=" * 60)
    print("PROJECT 16 — PRODUCTION CAPSTONE")
    print("=" * 60)

    print()
    print("ARCHITECTURE SIMULATION")
    print("Kafka -> Spark -> S3/Iceberg -> Redshift")
    print("Airflow -> Quality -> Prometheus")
    print()

    print("PIPELINE")
    print(f"Input Records:  {metrics['input_records']}")
    print(f"Output Records: {metrics['output_records']}")
    print(f"Runtime:        {metrics['runtime_seconds']}s")
    print(f"Pipeline Status: {metrics['pipeline_status']}")

    print()
    print("QUALITY")
    print(f"Quality Score:  {quality['score']:.2f}%")
    print(f"Quality Status: {quality['status']}")

    print()
    print("EXECUTIVE ANALYTICS")
    print(f"Transactions:   {executive['transaction_count']}")
    print(f"Total Value:    ${executive['total_transaction_value']:,.2f}")
    print(f"Average Value:  ${executive['average_transaction_value']:,.2f}")
    print(f"Fraud Flags:    {executive['fraud_transactions']}")

    print()
    print("STAGES")
    for stage, status in metrics["stages"].items():
        print(f"{stage:15} {status}")

    print()
    print("Production architecture simulation completed successfully.")


if __name__ == "__main__":
    main()
