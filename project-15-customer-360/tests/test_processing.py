from ingestion.customer_ingestion import CustomerIngestion
from processing.customer_standardization import CustomerStandardizer
from processing.transaction_processing import TransactionProcessor


def test_transaction_processing():
    raw = CustomerIngestion().load_all()
    data = CustomerStandardizer().standardize_all(raw)

    processor = TransactionProcessor()
    transactions = processor.process(
        data["orders"],
        data["products"],
    )

    assert len(transactions) == 24
    assert transactions["revenue"].sum() == 11560
    assert transactions["category"].notna().all()


def test_customer_transaction_metrics():
    raw = CustomerIngestion().load_all()
    data = CustomerStandardizer().standardize_all(raw)

    processor = TransactionProcessor()
    transactions = processor.process(
        data["orders"],
        data["products"],
    )

    metrics = processor.customer_transaction_metrics(transactions)

    assert len(metrics) == 8
    assert metrics["order_count"].sum() == 24
    assert metrics["total_revenue"].sum() == 11560
