from ingestion.customer_ingestion import CustomerIngestion
from processing.customer_standardization import CustomerStandardizer


def test_standardize_all():
    raw = CustomerIngestion().load_all()
    standardized = CustomerStandardizer().standardize_all(raw)

    assert len(standardized["customers"]) == 8
    assert len(standardized["products"]) == 8
    assert len(standardized["orders"]) == 24
    assert len(standardized["activity"]) == 24

    assert standardized["customers"]["email"].str.islower().all()
    assert standardized["orders"]["quantity"].gt(0).all()
