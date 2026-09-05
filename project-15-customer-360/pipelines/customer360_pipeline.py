import pandas as pd

from customer360.metrics import Customer360Metrics
from customer360.profile_builder import Customer360ProfileBuilder
from customer360.segmentation import CustomerSegmentation
from ingestion.customer_ingestion import CustomerIngestion
from monitoring.customer360_monitor import Customer360Monitor
from processing.customer_enrichment import CustomerEnricher
from processing.customer_standardization import CustomerStandardizer
from processing.transaction_processing import TransactionProcessor
from quality.customer360_quality import Customer360Quality
from storage.customer360_lake import Customer360Lake
from warehouse.customer_analytics import CustomerAnalyticsWarehouse


class Customer360Pipeline:
    """End-to-end Customer 360 unified analytics pipeline."""

    def __init__(self, source_dir="sample_data"):
        self.ingestion = CustomerIngestion(source_dir)
        self.standardizer = CustomerStandardizer()
        self.transaction_processor = TransactionProcessor()
        self.enricher = CustomerEnricher()
        self.profile_builder = Customer360ProfileBuilder()
        self.segmentation = CustomerSegmentation()
        self.metrics = Customer360Metrics()
        self.warehouse = CustomerAnalyticsWarehouse()
        self.quality = Customer360Quality()
        self.lake = Customer360Lake()
        self.monitor = Customer360Monitor()

    def run(self) -> dict:
        monitor_start = self.monitor.start()

        raw = self.ingestion.load_all()
        input_records = sum(
            len(dataframe) for dataframe in raw.values()
        )

        self.lake.write_bronze(raw)

        standardized = self.standardizer.standardize_all(raw)
        self.lake.write_silver(standardized)

        transactions = self.transaction_processor.process(
            standardized["orders"],
            standardized["products"],
        )

        transaction_metrics = (
            self.transaction_processor.customer_transaction_metrics(
                transactions
            )
        )

        activity_metrics = self.enricher.build_activity_metrics(
            standardized["activity"]
        )

        preferred_category = self.enricher.build_preferred_category(
            transactions
        )

        enriched = self.enricher.enrich(
            standardized["customers"],
            transaction_metrics,
            activity_metrics,
            preferred_category,
        )

        profile = self.profile_builder.build(enriched)
        profile = self.segmentation.segment(profile)

        summary = self.metrics.summary(profile)
        top_customers = self.metrics.top_customers(profile)
        segment_summary = self.segmentation.segment_summary(profile)

        customer_dimension = self.warehouse.build_customer_dimension(
            standardized["customers"]
        )
        customer_profile = self.warehouse.build_customer_profile(profile)
        transaction_fact = self.warehouse.build_transaction_fact(
            transactions
        )
        revenue_by_region = self.warehouse.revenue_by_region(profile)
        revenue_by_category = self.warehouse.revenue_by_category(
            transactions
        )
        segment_performance = self.warehouse.segment_performance(profile)

        quality_result = self.quality.validate(
            profile,
            standardized["customers"],
            transactions,
        )

        quality_score = quality_result["profile_quality"]["score"]

        gold_datasets = {
            "customer_360_profile": customer_profile,
            "dim_customer": customer_dimension,
            "fact_customer_transactions": transaction_fact,
            "revenue_by_region": revenue_by_region,
            "revenue_by_category": revenue_by_category,
            "segment_performance": segment_performance,
            "top_customers": top_customers,
            "segment_summary": segment_summary,
        }

        self.lake.write_gold(gold_datasets)

        monitoring = self.monitor.finish(
            monitor_start,
            input_records=input_records,
            output_records=len(profile),
            quality_score=quality_score,
        )

        return {
            "summary": summary,
            "quality": quality_result,
            "monitoring": monitoring,
            "top_customers": top_customers,
            "segment_summary": segment_summary,
            "revenue_by_region": revenue_by_region,
            "revenue_by_category": revenue_by_category,
            "segment_performance": segment_performance,
        }
