from prometheus_client import Counter,Histogram,start_http_server
pipeline_runs=Counter('pipeline_runs_total','Total pipeline executions',['pipeline_name','status'])
pipeline_duration=Histogram('pipeline_duration_seconds','Pipeline execution time',['pipeline_name'])
rows_processed=Counter('rows_processed_total','Total rows processed',['pipeline_name'])
start_http_server(8000)
