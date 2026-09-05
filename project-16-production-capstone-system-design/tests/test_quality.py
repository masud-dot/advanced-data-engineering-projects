from ingestion.batch_ingestion import BatchIngestion
from processing.stream_processor import SimulatedSparkProcessor
from quality.quality_engine import ProductionQualityEngine


def test_quality_passes_for_sample_data():
    raw = BatchIngestion("sample_data/transactions.csv").load()
    processed = SimulatedSparkProcessor().transform(raw)

    result = ProductionQualityEngine().validate_transactions(processed)

    assert result["status"] == "PASS"
    assert result["score"] == 100.0
