from pipelines.enterprise_platform import EnterpriseDataPlatform


def test_enterprise_pipeline(tmp_path):
    platform = EnterpriseDataPlatform(
        {
            "source_dir": "sample_data",
            "data_lake_root": str(tmp_path / "data_lake"),
            "retries": 1,
            "retry_delay_seconds": 0,
        }
    )

    result = platform.run()

    assert result["status"] == "SUCCESS"
    assert result["quality"]["score"] == 100.0
    assert result["monitoring"]["overall_healthy"] is True
    assert result["monitoring"]["error_count"] == 0
    assert result["warehouse"]["fact_orders"] == 10
