import os
from datetime import datetime,timezone
from sqlalchemy import create_engine,text
from alerts import send_slack_alert
engine=create_engine(os.getenv('DATABASE_URL','postgresql://postgres:admin@localhost:5432/data_engineering'))
def check_data_freshness(table,max_age_minutes=15):
    with engine.connect() as conn:
        latest=conn.execute(text(f'SELECT MAX(updated_at) FROM {table}')).scalar()
    if latest is None: return False
    age=(datetime.now(timezone.utc).replace(tzinfo=None)-latest).total_seconds()/60
    if age>max_age_minutes:
        send_slack_alert(f'Freshness alert: {table} last updated {age:.0f} min ago (threshold: {max_age_minutes} min)',severity='critical'); return False
    return True
