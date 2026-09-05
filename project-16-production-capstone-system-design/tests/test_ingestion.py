from ingestion.batch_ingestion import BatchIngestion
from ingestion.event_stream import SimulatedKafkaStream


def test_batch_ingestion():
    ingestion = BatchIngestion("sample_data/transactions.csv")
    df = ingestion.load()

    assert len(df) == 30
    assert "transaction_id" in df.columns


def test_simulated_kafka():
    stream = SimulatedKafkaStream("sample_data/transactions.csv")

    assert stream.event_count() == 30
