from ingestion.batch_ingestion import BatchIngestion
from processing.currency_normalization import CurrencyNormalizer
from processing.enrichment import TransactionEnricher
from processing.stream_processor import SimulatedSparkProcessor
from analytics.customer_analytics import CustomerAnalytics
from analytics.executive_metrics import ExecutiveMetrics
from analytics.fraud_detection import FraudDetector


def prepare_transactions():
    transactions = BatchIngestion("sample_data/transactions.csv").load()
    customers = BatchIngestion("sample_data/customers.csv").load()

    processed = SimulatedSparkProcessor().transform(transactions)
    enriched = TransactionEnricher().enrich(processed, customers)
    normalized = CurrencyNormalizer().normalize(enriched)

    return FraudDetector().detect(normalized)


def test_currency_normalization():
    analyzed = prepare_transactions()

    assert "amount_usd" in analyzed.columns
    assert "usd_rate" in analyzed.columns
    assert analyzed["amount_usd"].notna().all()

    expected_total = round(analyzed["amount_usd"].sum(), 2)
    assert expected_total == 28465.21


def test_customer_analytics():
    analyzed = prepare_transactions()

    summary = CustomerAnalytics().build_customer_summary(analyzed)

    assert len(summary) == 8
    assert round(summary["total_amount"].sum(), 2) == round(
        analyzed["amount"].sum(), 2
    )


def test_executive_metrics_use_usd():
    analyzed = prepare_transactions()

    metrics = ExecutiveMetrics().calculate(analyzed)

    assert metrics["transaction_count"] == 30
    assert metrics["total_transaction_value"] == 28465.21
    assert metrics["average_transaction_value"] == 948.84


def test_fraud_detection():
    analyzed = prepare_transactions()

    assert "fraud_flag" in analyzed.columns
    assert analyzed["fraud_flag"].sum() == 4
