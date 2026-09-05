import time
from dataclasses import dataclass, field


@dataclass
class PipelineMetrics:
    input_records: int = 0
    output_records: int = 0
    quality_score: float = 0.0
    errors: int = 0
    runtime_seconds: float = 0.0
    stages: dict = field(default_factory=dict)

    def start_timer(self):
        return time.perf_counter()

    def finish_timer(self, start: float):
        self.runtime_seconds = round(time.perf_counter() - start, 4)

    def to_dict(self) -> dict:
        return {
            "input_records": self.input_records,
            "output_records": self.output_records,
            "quality_score": self.quality_score,
            "errors": self.errors,
            "runtime_seconds": self.runtime_seconds,
            "stages": self.stages,
        }
