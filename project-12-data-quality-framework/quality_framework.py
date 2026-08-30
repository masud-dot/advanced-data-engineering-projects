import pandas as pd
from typing import List,Dict
EXPECTED_SCHEMA={'transaction_id':'int64','customer_id':'float64','amount':'float64','event_date':'object'}
REQUIRED_COLUMNS=['transaction_id','customer_id','amount']
def validate_schema(df)->List[str]:
    errors=[]
    for col,expected in EXPECTED_SCHEMA.items():
        if col not in df.columns: errors.append(f'Missing column: {col}')
        elif str(df[col].dtype)!=expected: errors.append(f'Type mismatch: {col} — expected {expected}, got {df[col].dtype}')
    return errors
def validate_nulls(df,required_cols)->Dict[str,int]:
    return {c:int(df[c].isnull().sum()) for c in required_cols if df[c].isnull().sum()>0}
def validate_ranges(df): return df[(df['amount']<=0)|(df['customer_id']<0)]
def validate_dates(df,date_col):
    x=df.copy(); x[date_col]=pd.to_datetime(x[date_col],errors='coerce'); return x[x[date_col].isnull()]
def detect_duplicates(df,key_cols): return df[df.duplicated(subset=key_cols,keep=False)]
def run_quality_framework(df):
    results={}
    results['schema_valid']=len(validate_schema(df))==0
    results['nulls_valid']=len(validate_nulls(df,REQUIRED_COLUMNS))==0
    results['ranges_valid']=len(validate_ranges(df))==0
    results['dates_valid']=len(validate_dates(df,'event_date'))==0
    results['no_duplicates']=len(detect_duplicates(df,['transaction_id']))==0
    if not all(results.values()): raise ValueError(f'Quality gate FAILED. Failed checks: {[k for k,v in results.items() if not v]}')
    return results
if __name__=='__main__':
    df=pd.read_csv('transactions.csv'); results=run_quality_framework(df)
    report=pd.DataFrame([{'Check':k,'Passed':v,'Status':'PASS' if v else 'FAIL'} for k,v in results.items()]); report.to_csv('reports/quality_report.csv',index=False); print(report.to_string(index=False))
