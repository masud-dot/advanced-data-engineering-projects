from ingestion.source_ingestion import SourceIngestion
from processing.transformation import DataTransformer


def test_transform_all():
    raw = SourceIngestion("sample_data").load_all()
    transformed = DataTransformer().transform_all(raw)

    assert len(transformed["customers"]) == 5
    assert len(transformed["products"]) == 5
    assert len(transformed["orders"]) == 10
    assert transformed["orders"]["amount"].min() >= 0
