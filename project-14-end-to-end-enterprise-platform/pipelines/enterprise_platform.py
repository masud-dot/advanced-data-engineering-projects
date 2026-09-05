from pathlib import Path
import json

from ingestion.source_ingestion import SourceIngestion
from processing.transformation import DataTransformer
from processing.enrichment import DataEnricher
from storage.data_lake import DataLake
from warehouse.analytics import AnalyticsWarehouse
from quality.platform_quality import PlatformQuality
from monitoring.platform_monitor import PlatformMonitor
from orchestration.workflow import PipelineWorkflow


class EnterpriseDataPlatform:
    """Runs the complete end-to-end enterprise data platform."""

    def __init__(self, config=None):
        config = config or {}

        self.ingestion = SourceIngestion(
            config.get("source_dir", "sample_data")
        )

        self.transformer = DataTransformer()
        self.enricher = DataEnricher()

        self.data_lake = DataLake(
            config.get("data_lake_root", "data_lake")
        )

        self.warehouse = AnalyticsWarehouse()

        self.quality = PlatformQuality()

        self.monitor = PlatformMonitor(
            runtime_threshold_seconds=config.get(
                "runtime_threshold_seconds", 60
            ),
            minimum_quality_score=config.get(
                "minimum_quality_score", 95
            ),
        )

        self.workflow = PipelineWorkflow(
            retries=config.get("retries", 3),
            retry_delay_seconds=config.get("retry_delay_seconds", 5),
        )

    def ingest(self):
        datasets = self.ingestion.load_all()

        self.data_lake.write_bronze(datasets)

        return datasets

    def transform(self, datasets):
        return self.transformer.transform_all(datasets)

    def enrich(self, datasets):
        return self.enricher.enrich_all(datasets)

    def store_silver(self, datasets):
        self.data_lake.write_silver(datasets)

    def build_warehouse(self, datasets):
        warehouse_data = self.warehouse.build_all(datasets)

        self.data_lake.write_gold(
            {
                "fact_orders": warehouse_data["fact_orders"],
                "dim_customer": warehouse_data["dim_customer"],
                "dim_product": warehouse_data["dim_product"],
                "daily_sales": warehouse_data["daily_sales"],
                "product_performance": warehouse_data["product_performance"],
                "customer_performance": warehouse_data["customer_performance"],
            }
        )

        return warehouse_data

    def run(self):
        start_time = self.monitor.start()

        datasets = {}
        transformed = {}
        enriched = {}
        warehouse_data = {}
        quality_result = {}
        pipeline_error_count = 0

        try:
            datasets = self.ingest()

            transformed = self.transform(datasets)

            enriched = self.enrich(transformed)

            self.store_silver(enriched)

            warehouse_data = self.build_warehouse(enriched)

            quality_result = self.quality.validate(
                enriched["customers"],
                enriched["products"],
                enriched["orders"],
            )

        except Exception:
            pipeline_error_count = 1
            raise

        finally:
            input_rows = len(datasets.get("orders", []))
            output_rows = len(
                warehouse_data.get("fact_orders", [])
            )

            quality_score = quality_result.get("score", 0.0)

            metrics = self.monitor.build_metrics(
                start_time=start_time,
                input_rows=input_rows,
                output_rows=output_rows,
                quality_score=quality_score,
                error_count=pipeline_error_count,
            )

        return {
            "status": "SUCCESS" if metrics["overall_healthy"] else "UNHEALTHY",
            "quality": quality_result,
            "monitoring": metrics,
            "warehouse": {
                name: len(data)
                for name, data in warehouse_data.items()
            },
            "workflow": {
                "stages": [
                    "ingestion",
                    "bronze_storage",
                    "transformation",
                    "enrichment",
                    "silver_storage",
                    "warehouse",
                    "gold_storage",
                    "data_quality",
                    "monitoring",
                ]
            },
        }


def main():
    platform = EnterpriseDataPlatform()

    result = platform.run()

    output_path = Path("data_lake/platform_run_report.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, default=str)
    )

    print("Enterprise Data Platform")
    print("========================")
    print(f"Status: {result['status']}")
    print(
        f"Quality Score: "
        f"{result['quality']['score']}%"
    )
    print(
        f"Orders: "
        f"{result['warehouse']['fact_orders']}"
    )
    print(
        f"Customers: "
        f"{result['warehouse']['dim_customer']}"
    )
    print(
        f"Products: "
        f"{result['warehouse']['dim_product']}"
    )
    print(
        f"Runtime: "
        f"{result['monitoring']['runtime_seconds']} seconds"
    )
    print(f"Report: {output_path}")


if __name__ == "__main__":
    main()
