from pathlib import Path
import pandas as pd


class BatchIngestion:
    """Local batch ingestion equivalent of a production source connector."""

    def __init__(self, source_path: str):
        self.source_path = Path(source_path)

    def load(self) -> pd.DataFrame:
        if not self.source_path.exists():
            raise FileNotFoundError(self.source_path)

        return pd.read_csv(self.source_path)
