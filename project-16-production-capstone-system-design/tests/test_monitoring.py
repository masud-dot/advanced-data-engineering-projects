from monitoring.metrics import PipelineMetrics


def test_pipeline_metrics():
    metrics = PipelineMetrics(
        input_records=100,
        output_records=98,
        quality_score=100.0,
        errors=0,
    )

    result = metrics.to_dict()

    assert result["input_records"] == 100
    assert result["output_records"] == 98
    assert result["quality_score"] == 100.0
    assert result["errors"] == 0
