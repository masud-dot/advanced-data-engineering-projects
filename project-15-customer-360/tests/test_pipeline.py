from pipelines.customer360_pipeline import Customer360Pipeline


def test_end_to_end_pipeline():
    result = Customer360Pipeline().run()

    assert result["summary"]["total_customers"] == 8
    assert result["summary"]["total_orders"] == 24
    assert result["summary"]["total_units"] == 37
    assert result["summary"]["total_revenue"] == 11560

    assert result["quality"]["profile_quality"]["score"] == 100
    assert result["quality"]["profile_quality"]["status"] == "PASS"

    assert result["monitoring"]["status"] == "SUCCESS"
    assert result["monitoring"]["output_records"] == 8
