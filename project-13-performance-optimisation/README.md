# Pipeline Performance Optimisation

A production-style data engineering project demonstrating practical techniques for improving data pipeline performance using Python and Pandas.

The project compares a baseline transformation pipeline with an optimized implementation and measures execution time, speedup, memory consumption, and throughput.

## Project Overview

Data pipelines can become slow and resource-intensive as data volumes increase. This project demonstrates how common performance bottlenecks can be addressed through:

- Vectorized Pandas operations
- Batch and chunk processing
- Memory optimization
- Parallel processing
- File-based caching
- Partition-aware processing
- Benchmarking
- Performance metrics
- Automated performance reporting
- Configurable optimization settings

The project uses a sales transaction dataset and produces a measurable before-and-after performance comparison.

## Architecture

```text
                    +----------------------+
                    |    Sales Dataset     |
                    |    sales_data.csv    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |    Data Loading      |
                    +----------+-----------+
                               |
                 +-------------+-------------+
                 |                           |
                 v                           v
        +------------------+       +------------------+
        | Baseline         |       | Optimized        |
        | Transformation   |       | Transformation   |
        | Row-wise apply() |       | Vectorization    |
        +--------+---------+       +--------+---------+
                 |                          |
                 +------------+-------------+
                              |
                              v
                    +----------------------+
                    | Benchmarking         |
                    | Runtime / Speedup    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Memory Optimization  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Performance Metrics  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | JSON Performance     |
                    | Report               |
                    +----------------------+
```

## Project Structure

```text
project-13-performance-optimisation/
├── README.md
├── requirements.txt
├── Dockerfile
├── .gitignore
├── configs/
│   └── performance.yaml
├── performance/
│   ├── benchmark.py
│   ├── memory.py
│   ├── batching.py
│   ├── vectorization.py
│   ├── parallel.py
│   ├── caching.py
│   ├── partitioning.py
│   ├── metrics.py
│   ├── optimizer.py
│   └── report.py
├── pipelines/
│   └── performance_pipeline.py
├── sample_data/
│   └── sales_data.csv
├── sql/
│   └── performance_queries.sql
├── src/
│   └── performance_pipeline.py
├── tests/
│   ├── test_benchmark.py
│   ├── test_memory.py
│   ├── test_batching.py
│   ├── test_vectorization.py
│   ├── test_parallel.py
│   ├── test_caching.py
│   ├── test_partitioning.py
│   └── test_pipeline.py
└── local_output/
    └── performance_report.json
```

## Performance Techniques

### 1. Vectorization

The baseline implementation uses row-wise Pandas operations.

The optimized implementation uses vectorized operations that process complete columns efficiently.

This reduces Python-level iteration and can significantly improve execution time.

### 2. Memory Optimization

The project analyzes DataFrame memory usage and applies suitable optimizations such as:

- Integer downcasting
- Float downcasting
- Category conversion for suitable string columns

This reduces the memory footprint of the DataFrame.

### 3. Batch Processing

Large datasets can be divided into manageable batches.

This approach helps control memory consumption and makes processing suitable for larger workloads.

### 4. Parallel Processing

The project includes a reusable parallel mapping utility based on `ThreadPoolExecutor`.

Independent operations can be distributed across multiple workers where parallel execution is appropriate.

### 5. Caching

The file-based cache avoids repeating expensive computations when the same result can be reused.

### 6. Partition-Aware Processing

The partitioning utility groups data by a selected column such as `transaction_date`.

In production data platforms, partition-aware filtering can reduce the amount of data scanned.

### 7. Benchmarking

The benchmark framework measures:

- Average execution time
- Minimum execution time
- Maximum execution time
- Number of iterations

Warm-up runs are supported to improve measurement consistency.

## Performance Results

The sample benchmark produced the following results:

| Metric | Baseline | Optimized |
|---|---:|---:|
| Average runtime | 0.058656 sec | 0.003919 sec |
| Memory usage | 2.2953 MB | 0.3259 MB |
| Throughput | — | 3,264,453 rows/sec |

### Speed Improvement

The optimized transformation achieved approximately:

**14.97× faster execution**

The memory footprint was reduced from:

**2.2953 MB → 0.3259 MB**

The optimized pipeline processed approximately:

**3.26 million rows/sec**

These values are based on the included 10,000-row sample dataset and will vary depending on hardware, Python version, dataset size, and workload characteristics.

## Configuration

Performance settings are maintained in:

```text
configs/performance.yaml
```

Example configuration:

```yaml
benchmark:
  iterations: 3
  warmup_runs: 1

processing:
  batch_size: 1000
  workers: 4

memory:
  optimization_enabled: true
  memory_threshold_mb: 512

parallel:
  enabled: true
  workers: 4

caching:
  enabled: true
  cache_directory: local_cache

partitioning:
  enabled: true
  partition_column: transaction_date
```

## Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the performance pipeline:

```bash
python -m pipelines.performance_pipeline
```

The pipeline generates:

```text
local_output/performance_report.json
```

## Running Tests

Execute the complete test suite:

```bash
python -m pytest -q
```

The current test suite includes 14 passing tests covering:

- Benchmarking
- Memory optimization
- Batch processing
- Vectorized transformations
- Parallel processing
- Caching
- Partitioning
- End-to-end pipeline execution

## Docker

Build the Docker image:

```bash
docker build -t pipeline-performance-optimisation .
```

Run the container:

```bash
docker run --rm pipeline-performance-optimisation
```

## Performance Targets

The project defines configurable performance targets:

| Target | Threshold |
|---|---:|
| Maximum runtime | 10 seconds |
| Minimum throughput | 1,000 rows/sec |
| Maximum memory | 512 MB |

The included sample workload comfortably satisfies these targets.

## Production Considerations

For large-scale production workloads, the techniques demonstrated here can be extended with:

- Distributed processing using Spark
- Cloud object storage
- Database query optimization
- Partition pruning
- Columnar formats such as Parquet
- Predicate pushdown
- Incremental processing
- Distributed caching
- Workflow orchestration
- Production monitoring
- Resource-aware autoscaling

The important principle is to **measure first, identify the bottleneck, apply an appropriate optimization, and benchmark again**.

## Learning Outcomes

After completing this project, readers should understand how to:

1. Identify common pipeline performance bottlenecks.
2. Measure execution time reliably.
3. Compare baseline and optimized implementations.
4. Use Pandas vectorization effectively.
5. Reduce DataFrame memory consumption.
6. Process data in batches.
7. Apply parallel processing appropriately.
8. Introduce caching into data workflows.
9. Use partition-aware processing.
10. Build reusable performance measurement utilities.
11. Generate machine-readable performance reports.
12. Evaluate whether a pipeline meets defined performance targets.

## Disclaimer

This project is provided for educational and demonstration purposes. Benchmark results are environment-dependent and should not be treated as guaranteed production performance.
