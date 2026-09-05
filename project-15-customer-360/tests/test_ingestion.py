from ingestion.customer_ingestion import CustomerIngestion


def test_load_all_datasets():
    ingestion = CustomerIngestion()
    datasets = ingestion.load_all()

    assert set(datasets) == {
        "customers",
        "orders",
        "products",
        "activity",
    }

    assert len(datasets["customers"]) == 8
    assert len(datasets["orders"]) == 24
    assert len(datasets["products"]) == 8
    assert len(datasets["activity"]) == 24
