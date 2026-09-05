from ingestion.source_ingestion import SourceIngestion
from processing.transformation import DataTransformer
from quality.platform_quality import PlatformQuality


def test_platform_quality():
    raw = SourceIngestion("sample_data").load_all()
    datasets = DataTransformer().transform_all(raw)

    result = PlatformQuality().validate(
        datasets["customers"],
        datasets["products"],
        datasets["orders"],
    )

    assert result["score"] == 100.0
    assert result["passed"] is True
    assert result["passed_checks"] == 8
    assert result["total_checks"] == 8
