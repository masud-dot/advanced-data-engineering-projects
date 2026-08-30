import pandas as pd
import pytest
from pipelines.etl_pipeline import process_data

@pytest.fixture
def sample_df(tmp_path):
    data=pd.DataFrame({'amount':[100,200,300]})
    path=tmp_path/'sales.csv'; data.to_csv(path,index=False); return str(path)

def test_tax_column_exists(sample_df): assert 'tax_amount' in process_data(sample_df).columns
def test_tax_calculation_correct(sample_df): assert abs(process_data(sample_df).iloc[0]['tax_amount']-18.0)<0.001
def test_no_null_values(sample_df): assert process_data(sample_df).isnull().sum().sum()==0
