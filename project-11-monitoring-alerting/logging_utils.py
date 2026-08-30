import logging,json
from datetime import datetime,timezone
logging.basicConfig(filename='logs/pipeline.log',level=logging.INFO,format='%(asctime)s | %(levelname)s | %(message)s')
def log_pipeline_start(name): logging.info(json.dumps({'event':'pipeline_started','pipeline':name,'timestamp':datetime.now(timezone.utc).isoformat()}))
def log_pipeline_success(name,rows,duration): logging.info(json.dumps({'event':'pipeline_completed','pipeline':name,'rows':rows,'duration':duration}))
def log_pipeline_failure(name,error): logging.error(json.dumps({'event':'pipeline_failed','pipeline':name,'error':error}))
