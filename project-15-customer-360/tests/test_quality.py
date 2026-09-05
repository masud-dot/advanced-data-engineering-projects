from ingestion.customer_ingestion import CustomerIngestion
from processing.customer_standardization import CustomerStandardizer
from processing.transaction_processing import TransactionProcessor
from processing.customer_enrichment import CustomerEnricher
from customer360.profile_builder import Customer360ProfileBuilder
from customer360.segmentation import CustomerSegmentation
from quality.customer360_quality import Customer360Quality


def build_profile():
    raw = CustomerIngestion().load_all()
    data = CustomerStandardizer().standardize_all(raw)

    processor = TransactionProcessor()
    transactions = processor.process(
        data["orders"],
        data["products"],
    )

    transaction_metrics = processor.customer_transaction_metrics(
        transactions
    )

    enricher = CustomerEnricher()

    activity_metrics = enricher.build_activity_metrics(
        data["activity"]
    )

    preferred_category = enricher.build_preferred_category(
        transactions
    )

    enriched = enricher.enrich(
        data["customers"],
        transaction_metrics,
        activity_metrics,
        preferred_category,
    )

    profile = Customer360ProfileBuilder().build(enriched)
    return CustomerSegmentation().segment(profile), data, transactions


def test_customer360_quality():
    profile, data, transactions = build_profile()

    result = Customer360Quality().validate(
        profile,
        data["customers"],
        transactions,
    )

    assert result["profile_quality"]["score"] == 100
    assert result["profile_quality"]["status"] == "PASS"
    assert result["referential_integrity"]["passed"] is True
