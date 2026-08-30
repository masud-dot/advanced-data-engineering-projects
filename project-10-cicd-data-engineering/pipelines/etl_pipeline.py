import pandas as pd

def process_data(file_path='sales.csv'):
    df=pd.read_csv(file_path)
    df['tax_amount']=df['amount']*0.18
    df['total_amount']=df['amount']+df['tax_amount']
    return df
