from ingestion.source_ingestion import SourceIngestion


def test_load_all():
    datasets = SourceIngestion("sample_data").load_all()

    assert set(datasets) == {"customers", "products", "orders"}
    assert len(datasets["customers"]) == 5
    assert len(datasets["products"]) == 5
    assert len(datasets["orders"]) == 10
