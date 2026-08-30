import requests,pandas as pd
def ingest_crm_api(api_url,api_key):
    headers={'Authorization':f'Bearer {api_key}'}; r=requests.get(api_url,headers=headers,timeout=30); r.raise_for_status(); return pd.DataFrame(r.json()['data'])
