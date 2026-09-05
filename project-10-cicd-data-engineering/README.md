# Project 10 — CI/CD Pipeline for Data Engineering

A production-oriented reference implementation showing how a data engineering pipeline can be tested, validated, containerized, and prepared for automated deployment using GitHub Actions.

> **Important:** This repository uses synthetic data and local execution. Cloud deployment steps are represented as safe, reusable patterns rather than claiming a live production deployment.

## 1. Project Overview

A data pipeline is not production-ready simply because the transformation code works. Teams also need automated testing, data validation, environment-specific configuration, secure secret handling, reproducible packaging, deployment gates, and rollback planning.

This project demonstrates those practices with Python, PyTest, YAML configuration, Docker, SQL validation, and GitHub Actions.

### Pipeline flow

```text
Developer Change
       |
       v
   Git Push / PR
       |
       v
+-------------------+
| GitHub Actions CI |
+-------------------+
       |
       +--> Install dependencies
       +--> Compile Python
       +--> Run unit tests
       +--> Run ETL pipeline
       +--> Validate output
       +--> Validate SQL
       +--> Build Docker image
       |
       v
  CI Quality Gate
       |
       v
+-------------------+
| Release / CD Gate |
+-------------------+
       |
       +--> Pre-deployment tests
       +--> Build release image
       +--> Deployment step
       |
       v
 Production Platform
```

## 2. What This Project Demonstrates

- Python-based ETL processing
- Automated unit testing with PyTest
- Data-quality validation
- Environment-specific YAML configuration
- Environment-variable expansion
- Secure secret loading
- Docker containerization
- GitHub Actions CI
- GitHub Actions CD/deployment gate
- Manual pipeline execution
- SQL-based warehouse validation
- Production deployment and rollback patterns

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Pipeline implementation |
| Pandas | Data transformation |
| PyTest | Automated testing |
| PyYAML | Configuration loading |
| Docker | Reproducible packaging |
| GitHub Actions | CI/CD automation |
| SQL | Data validation |

## 4. Project Structure

```text
project-10-cicd-data-engineering/
│
├── .github/workflows/
│   ├── ci.yml
│   ├── cd.yml
│   └── pipeline.yml
├── configs/
│   ├── dev.yaml
│   └── prod.yaml
├── pipelines/
│   └── etl_pipeline.py
├── sample_data/
│   └── sample_sales.csv
├── sql/
│   └── validation.sql
├── src/
│   ├── pipeline.py
│   └── validation.py
├── tests/
│   └── test_pipeline.py
├── config_loader.py
├── secret_loader.py
├── pipeline.py
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md
```

## 5. ETL Pipeline

The example processes sales transactions containing:

```text
transaction_id
amount
```

The transformation adds:

```text
tax_amount
total_amount
```

The calculation is:

```text
tax_amount = amount × 0.18
total_amount = amount + tax_amount
```

The pipeline rejects missing required columns, null amounts, negative amounts, and missing input files.

## 6. Sample Data

The repository contains ten synthetic sales transactions. No production or personally identifiable data is included.

```csv
transaction_id,amount
1001,1250.00
1002,2400.00
1003,875.50
1004,3200.00
1005,1599.99
```

## 7. Data Validation

Validation is performed at both application and SQL levels.

`src/validation.py` checks:

- Required output columns
- Empty datasets
- Null values
- Negative amounts
- Total calculation accuracy
- Duplicate transaction IDs

`sql/validation.sql` provides warehouse-side checks for row count, null transaction IDs, negative amounts, duplicates, and calculation errors.

This reflects a common production principle: application tests and downstream data-quality checks complement each other.

## 8. Automated Testing

The PyTest suite covers:

1. Tax column creation
2. Tax calculation
3. Total calculation
4. Null-value handling
5. Complete validation
6. Negative amount rejection
7. Missing input file handling
8. Development configuration loading

Run:

```bash
python -m pytest -q
```

Expected result:

```text
8 passed
```

## 9. Environment Configuration

Configuration is separated by environment.

### Development

`configs/dev.yaml` uses local settings and a smaller batch size.

### Production

`configs/prod.yaml` uses environment variables such as:

```text
DB_HOST
```

This keeps environment-specific infrastructure settings outside application code.

Load configuration with:

```python
from config_loader import load_config

config = load_config("dev")
```

## 10. Secret Management

The project deliberately avoids hard-coded credentials.

`secret_loader.py` reads sensitive values from environment variables, including:

```text
DB_PASSWORD
AWS_ACCESS_KEY_ID
```

A real production system should normally use a managed secret store or encrypted CI/CD secrets.

Never commit passwords, API keys, private keys, cloud credentials, or production connection strings.

## 11. Docker

Build the image:

```bash
docker build -t data-engineering-pipeline:local .
```

Run it:

```bash
docker run --rm data-engineering-pipeline:local
```

The container executes:

```text
python pipeline.py
```

Containerization provides a consistent runtime between development, CI, and deployment environments.

## 12. Continuous Integration

`.github/workflows/ci.yml` performs these quality gates:

```text
Checkout
   ↓
Setup Python
   ↓
Install dependencies
   ↓
Compile Python
   ↓
Run PyTest
   ↓
Run pipeline validation
   ↓
Validate SQL
   ↓
Build Docker image
```

It runs for pushes to `main` and `develop`, and pull requests targeting `main`.

A change should not be considered release-ready until the automated checks pass.

## 13. Continuous Delivery

`.github/workflows/cd.yml` supports manual execution and release execution when a version tag matching `v*` is pushed.

The workflow performs:

1. Dependency installation
2. Pre-deployment tests
3. Release Docker image build
4. Deployment hand-off

The deployment step is intentionally a placeholder because this repository does not claim access to a live production cloud environment.

## 14. Manual Pipeline Workflow

`.github/workflows/pipeline.yml` provides a manually triggered pipeline execution.

This can be useful for controlled re-runs, demonstrations, operational testing, troubleshooting, and validation after infrastructure changes.

## 15. Rollback Strategy

A production CI/CD system should provide a recovery path.

Recommended practices include:

### Immutable release artifacts

Build images using a unique version or commit SHA:

```text
data-engineering-pipeline:<commit-sha>
```

### Retain a known-good version

Keep the previous production artifact available so the deployment platform can switch back when required.

### Health checks

After deployment, validate application startup, pipeline execution, data-quality metrics, output availability, and monitoring signals.

```text
New Release
    |
    v
Health Check
    |
    +---- PASS ---> Continue
    |
    +---- FAIL ---> Roll Back
```

The exact rollback mechanism depends on the target platform.

## 16. Security Practices

This project follows baseline security practices:

- Keep credentials outside Git
- Use synthetic data
- Prefer managed secret stores
- Use least-privilege cloud identities
- Protect the production branch
- Require code review and CI checks before release

## 17. Local Execution

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the pipeline:

```bash
python pipeline.py
```

Run tests:

```bash
python -m pytest -q
```

Compile Python:

```bash
python -m compileall -q .
```

Run the complete validation:

```bash
python -m pytest -q && python pipeline.py && python -m compileall -q .
```

Expected successful execution includes:

```text
8 passed
Validation: PASSED
Rows processed: 10
```

## 18. Output

The local pipeline writes:

```text
local_output/processed_sales.csv
```

Generated runtime output is ignored by Git, keeping the repository focused on reproducible source code and sample input.

## 19. Production Extension

A real enterprise implementation could extend this pattern with:

- Apache Airflow orchestration
- Spark processing
- Cloud object storage
- Data warehouses or lakehouses
- Infrastructure as Code
- Kubernetes or managed container deployment
- Centralized logging
- Observability and alerting
- Data-quality frameworks
- Managed secrets
- Automated rollback
- Blue/green or canary deployment

These components are intentionally outside the scope of this local demonstration.

## 20. Validation Status

The local implementation has been validated with:

```text
Pandas import             PASS
NumPy random module       PASS
PyTest                    PASS
8 automated tests         PASS
ETL pipeline              PASS
10 sample rows processed  PASS
Data validation           PASS
Python compilation        PASS
```

The GitHub Actions workflows are provided as reusable CI/CD patterns. Live production cloud deployment has not been claimed.

## 21. Learning Outcomes

After completing this project, a data engineer should understand how to:

- Structure a testable data pipeline
- Build automated data-quality checks
- Separate configuration from application logic
- Handle secrets safely
- Package a pipeline with Docker
- Create CI quality gates
- Design a CD deployment gate
- Validate warehouse outputs with SQL
- Create reproducible release artifacts
- Plan rollback procedures
- Apply production engineering practices to data pipelines

## 22. Related Book

This repository accompanies:

**Advanced Data Engineering Projects with Python, SQL & Cloud**

The book focuses on practical, project-driven data engineering architectures and implementation patterns.

## License

This project is provided for educational and demonstration purposes. Apply appropriate security, compliance, testing, and deployment controls before adapting these patterns for production systems.
