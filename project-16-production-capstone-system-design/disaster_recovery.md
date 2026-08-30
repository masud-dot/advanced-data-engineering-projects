# Disaster Recovery

Primary: us-east-1
DR: us-west-2

- S3 cross-region replication
- Kafka MirrorMaker 2
- Redshift snapshots replicated to DR
- Airflow metadata database with HA/failover
