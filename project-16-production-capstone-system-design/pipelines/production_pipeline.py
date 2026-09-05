from pathlib import Path

from analytics.customer_analytics import CustomerAnalytics
from analytics.executive_metrics import ExecutiveMetrics
from analytics.fraud_detection import FraudDetector
from ingestion.batch_ingestion import BatchIngestion
from ingestion.event_stream import SimulatedKafkaStream
from monitoring.metrics import PipelineMetrics
from monitoring.prometheus_metrics import LocalPrometheusExporter
from processing.enrichment import TransactionEnricher
from processing.currency_normalization import CurrencyNormalizer
from processing.stream_processor import SimulatedSparkProcessor
from quality.quality_engine import ProductionQualityEngine
from storage.data_lake import LocalDataLake
from storage.iceberg_table import LocalIcebergTable
from warehouse.analytics_warehouse import LocalRedshiftWarehouse


class ProductionCapstonePipeline:
    """End-to-end production architecture simulation."""

    def __init__(self):
        self.data_root = Path("sample_data")

        self.batch = BatchIngestion(
            str(self.data_root / "transactions.csv")
        )
        self.stream = SimulatedKafkaStream(
            str(self.data_root / "transactions.csv")
        )

        self.processor = SimulatedSparkProcessor()
        self.enricher = TransactionEnricher()
        self.currency = CurrencyNormalizer()
        self.quality = ProductionQualityEngine()

        self.lake = LocalDataLake()
        self.iceberg = LocalIcebergTable()
        self.warehouse = LocalRedshiftWarehouse()

        self.fraud = FraudDetector()
        self.customer_analytics = CustomerAnalytics()
        self.executive = ExecutiveMetrics()

        self.metrics = PipelineMetrics()
        self.monitoring = LocalPrometheusExporter()

    def run(self) -> dict:
        timer = self.metrics.start_timer()

        customers = self.batch.load.__self__.source_path.parent / "customers.csv"
        customers_df = BatchIngestion(str(customers)).load()

        transactions = self.batch.load()

        self.metrics.input_records = len(transactions)
        self.metrics.stages["ingestion"] = "SUCCESS"

        # Bronze = raw ingested events.
        self.lake.write(transactions, "bronze", "transactions_raw")

        processed = self.processor.transform(transactions)
        self.metrics.stages["processing"] = "SUCCESS"

        enriched = self.enricher.enrich(processed, customers_df)
        self.metrics.stages["enrichment"] = "SUCCESS"

        normalized = self.currency.normalize(enriched)
        self.metrics.stages["currency_normalization"] = "SUCCESS"

        quality_report = self.quality.validate_transactions(processed)

        if quality_report["status"] != "PASS":
            self.metrics.errors += 1
            raise ValueError(f"Quality gate failed: {quality_report}")

        self.metrics.quality_score = quality_report["score"]
        self.metrics.stages["quality"] = "PASS"

        # Silver = validated and enriched transactions.
        self.iceberg.write("silver", "transactions", enriched)
        self.metrics.stages["storage"] = "SUCCESS"

        analyzed = self.fraud.detect(normalized)
        customer_summary = self.customer_analytics.build_customer_summary(analyzed)

        executive_metrics = self.executive.calculate(analyzed)

        # Gold = analytics-ready tables.
        self.iceberg.write("gold", "transactions_analytics", analyzed)
        self.warehouse.load("fact_transactions", analyzed)
        self.warehouse.load("customer_analytics", customer_summary)

        self.metrics.stages["warehouse"] = "SUCCESS"
        self.metrics.stages["analytics"] = "SUCCESS"

        self.metrics.output_records = len(analyzed)
        self.metrics.finish_timer(timer)

        metrics_payload = self.metrics.to_dict()
        metrics_payload["pipeline_status"] = "SUCCESS"

        self.monitoring.export(metrics_payload)
        self.metrics.stages["monitoring"] = "SUCCESS"

        return {
            "transactions": analyzed,
            "customer_summary": customer_summary,
            "quality": quality_report,
            "executive_metrics": executive_metrics,
            "metrics": metrics_payload,
        }
