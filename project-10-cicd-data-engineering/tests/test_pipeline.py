import pandas as pd
import pytest

from config_loader import load_config
from pipelines.etl_pipeline import process_data
from src.validation import validate_processed_data


@pytest.fixture
def sample_df(tmp_path):
    data = pd.DataFrame(
        {
            "transaction_id": [1, 2, 3],
            "amount": [100.00, 200.00, 300.00],
        }
    )

    path = tmp_path / "sales.csv"
    data.to_csv(path, index=False)
    return str(path)


def test_tax_column_exists(sample_df):
    result = process_data(sample_df)
    assert "tax_amount" in result.columns


def test_tax_calculation_correct(sample_df):
    result = process_data(sample_df)
    assert abs(result.iloc[0]["tax_amount"] - 18.0) < 0.001


def test_total_amount_calculation(sample_df):
    result = process_data(sample_df)
    assert abs(result.iloc[0]["total_amount"] - 118.0) < 0.001


def test_no_null_values(sample_df):
    result = process_data(sample_df)
    assert result.isnull().sum().sum() == 0


def test_validation_passes(sample_df):
    result = process_data(sample_df)
    assert validate_processed_data(result) is True


def test_negative_amount_rejected(tmp_path):
    data = pd.DataFrame(
        {
            "transaction_id": [1],
            "amount": [-100.00],
        }
    )

    path = tmp_path / "invalid.csv"
    data.to_csv(path, index=False)

    with pytest.raises(ValueError):
        process_data(path)


def test_missing_input_file():
    with pytest.raises(FileNotFoundError):
        process_data("does-not-exist.csv")


def test_dev_configuration():
    config = load_config("dev")
    assert config["database"]["host"] == "localhost"
    assert config["pipeline"]["batch_size"] == 1000
