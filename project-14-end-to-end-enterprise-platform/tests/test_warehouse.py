from ingestion.source_ingestion import SourceIngestion
from processing.transformation import DataTransformer
from processing.enrichment import DataEnricher
from warehouse.analytics import AnalyticsWarehouse


def test_warehouse_outputs():
    raw = SourceIngestion("sample_data").load_all()
    transformed = DataTransformer().transform_all(raw)
    enriched = DataEnricher().enrich_all(transformed)

    warehouse = AnalyticsWarehouse()
    result = warehouse.build_all(enriched)

    assert len(result["fact_orders"]) == 10
    assert len(result["dim_customer"]) == 5
    assert len(result["dim_product"]) == 5
    assert len(result["daily_sales"]) == 10
    assert len(result["product_performance"]) == 5
    assert len(result["customer_performance"]) == 5
