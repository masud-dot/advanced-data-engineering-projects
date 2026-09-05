from pathlib import Path
import json


class LocalPrometheusExporter:
    """
    Local metrics exporter.

    Production mapping: Prometheus counters/gauges/histograms.
    Local mapping: JSON metrics snapshot.
    """

    def __init__(self, output_dir: str = "monitoring_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(self, metrics: dict) -> Path:
        path = self.output_dir / "pipeline_metrics.json"

        with path.open("w", encoding="utf-8") as file:
            json.dump(metrics, file, indent=2)

        return path
