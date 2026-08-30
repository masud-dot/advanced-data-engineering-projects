# Capacity Planning

## Kafka
- Current peak: 100K events/sec
- Projection: 500K events/sec
- Design: 50 partitions/topic, 3x replication, 30-day retention

## Spark
- Current: 500 GB/day
- Projection: 5 TB/day
- Design: EMR auto-scaling, 2–50 executors, spot capacity

## Redshift
- Current: 10 TB
- Projection: 100 TB
- Design: RA3 with separated storage/compute
