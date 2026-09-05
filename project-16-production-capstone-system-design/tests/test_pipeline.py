from pipelines.production_pipeline import ProductionCapstonePipeline


def test_end_to_end_pipeline():
    result = ProductionCapstonePipeline().run()

    assert result["quality"]["status"] == "PASS"
    assert result["quality"]["score"] == 100.0
    assert result["metrics"]["pipeline_status"] == "SUCCESS"
    assert result["metrics"]["input_records"] == 30
    assert result["metrics"]["output_records"] == 30
    assert len(result["customer_summary"]) == 8
