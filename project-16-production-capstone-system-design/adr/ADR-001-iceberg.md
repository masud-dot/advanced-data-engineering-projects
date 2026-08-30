# ADR-001: Use Apache Iceberg

**Status:** Accepted

## Context
We need ACID transactions, time travel, schema evolution, and multi-engine access over S3.

## Decision
Adopt Apache Iceberg for Silver and Gold table layers.

## Consequences
Teams need Iceberg-aware APIs and a catalog; compaction and metadata management become operational responsibilities.
