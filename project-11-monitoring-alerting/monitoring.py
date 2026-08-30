import functools,time
from metrics import PipelineMetrics
from logging_utils import log_pipeline_start,log_pipeline_success,log_pipeline_failure
from alerts import send_slack_alert
def with_monitoring(pipeline_name,max_retries=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            metrics=PipelineMetrics(pipeline_name); log_pipeline_start(pipeline_name)
            for attempt in range(1,max_retries+1):
                try:
                    result=func(*args,**kwargs); log_pipeline_success(pipeline_name,metrics.rows,metrics.duration()); return result
                except Exception as e:
                    metrics.record_error(); log_pipeline_failure(pipeline_name,str(e))
                    if attempt<max_retries: time.sleep(30*attempt)
                    else: send_slack_alert(f'Pipeline {pipeline_name} failed after {max_retries} retries: {e}',severity='critical'); raise
        return wrapper
    return decorator
