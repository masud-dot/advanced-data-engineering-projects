# Failure Recovery

| Failure | Recovery | Target RTO |
|---|---|---|
| Kafka broker | Leader election | <30 sec |
| Spark job | Checkpoint restart | <5 min |
| S3 corruption | Cross-region restore | <1 hr |
| Redshift node | Automatic replacement | <15 min |
| Airflow scheduler | Standby scheduler | <2 min |
