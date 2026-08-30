SCHEMA_MAP={'crm':{'customer_id':'customer_id','customer_name':'name','country':'country'},'orders':{'cust_id':'customer_id','order_id':'order_id','amount':'amount'},'streaming':{'user_id':'customer_id','session_id':'session','event':'event_type'}}
def standardise(df,source):
    rename_map=SCHEMA_MAP[source]; df=df.rename(columns=rename_map); canonical_cols=list(rename_map.values()); return df[[c for c in canonical_cols if c in df.columns]]
