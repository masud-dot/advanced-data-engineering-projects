from pathlib import Path
import pandas as pd


class SimulatedKafkaStream:
    """Local simulation of a Kafka transaction event stream."""

    def __init__(self, source_path: str):
        self.source_path = Path(source_path)

    def read_events(self) -> pd.DataFrame:
        df = pd.read_csv(self.source_path)
        return df.copy()

    def event_count(self) -> int:
        return len(self.read_events())
