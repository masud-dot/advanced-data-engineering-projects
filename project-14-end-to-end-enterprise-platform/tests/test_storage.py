from ingestion.source_ingestion import SourceIngestion
from storage.data_lake import DataLake


def test_bronze_and_silver_storage(tmp_path):
    lake = DataLake(tmp_path / "data_lake")
    datasets = SourceIngestion("sample_data").load_all()

    lake.write_bronze(datasets)

    assert len(lake.read_bronze("orders")) == 10
    assert len(lake.read_bronze("customers")) == 5
    assert len(lake.read_bronze("products")) == 5

    lake.write_silver(datasets)

    assert len(lake.read_silver("orders")) == 10
