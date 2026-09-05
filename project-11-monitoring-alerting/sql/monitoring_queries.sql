-- Project 11: Monitoring & Alerting System
-- Example SQL patterns for a production monitoring warehouse.
-- Adapt column/table names to the target platform.

-- 1. Recent pipeline executions
SELECT
    pipeline_name,
    run_id,
    status,
    started_at,
    ended_at,
    duration_seconds,
    input_rows,
    output_rows,
    error_count,
    quality_score
FROM pipeline_metrics
ORDER BY started_at DESC
LIMIT 20;


-- 2. Failed pipeline executions
SELECT
    pipeline_name,
    run_id,
    started_at,
    ended_at,
    error_count
FROM pipeline_metrics
WHERE status = 'FAILED'
ORDER BY started_at DESC;


-- 3. Slow pipeline executions
SELECT
    pipeline_name,
    run_id,
    duration_seconds,
    started_at
FROM pipeline_metrics
WHERE duration_seconds > 30
ORDER BY duration_seconds DESC;


-- 4. Data-volume anomalies
SELECT
    pipeline_name,
    run_id,
    input_rows,
    output_rows,
    started_at
FROM pipeline_metrics
WHERE output_rows < 1
   OR output_rows > input_rows
ORDER BY started_at DESC;


-- 5. Low-quality executions
SELECT
    pipeline_name,
    run_id,
    quality_score,
    error_count,
    started_at
FROM pipeline_metrics
WHERE quality_score < 0.95
ORDER BY quality_score ASC;


-- 6. Alert history
SELECT
    alert_id,
    pipeline_name,
    severity,
    rule,
    message,
    created_at
FROM pipeline_alerts
ORDER BY created_at DESC
LIMIT 50;


-- 7. Critical alerts
SELECT
    alert_id,
    pipeline_name,
    rule,
    message,
    created_at
FROM pipeline_alerts
WHERE severity = 'CRITICAL'
ORDER BY created_at DESC;


-- 8. Daily pipeline success rate
SELECT
    pipeline_name,
    CAST(started_at AS DATE) AS execution_date,
    COUNT(*) AS total_runs,
    SUM(
        CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END
    ) AS successful_runs,
    ROUND(
        100.0 *
        SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0),
        2
    ) AS success_rate_pct
FROM pipeline_metrics
GROUP BY
    pipeline_name,
    CAST(started_at AS DATE)
ORDER BY execution_date DESC;


-- 9. Average runtime by pipeline
SELECT
    pipeline_name,
    COUNT(*) AS total_runs,
    ROUND(AVG(duration_seconds), 3) AS avg_duration_seconds,
    ROUND(MAX(duration_seconds), 3) AS max_duration_seconds
FROM pipeline_metrics
GROUP BY pipeline_name
ORDER BY avg_duration_seconds DESC;
