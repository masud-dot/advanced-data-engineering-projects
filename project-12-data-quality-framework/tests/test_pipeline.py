import json

from pipelines.quality_pipeline import run_quality_pipeline


def test_quality_pipeline_passes_and_creates_report():
    result = run_quality_pipeline()

    assert result["passed"] is True
    assert result["quality_score"] == 1.0
    assert result["rows"] == 10

    with open(
        result["report_file"],
        "r",
        encoding="utf-8",
    ) as file:
        report = json.load(file)

    assert report["status"] == "PASS"
    assert report["quality_score"] == 1.0
    assert report["row_count"] == 10
