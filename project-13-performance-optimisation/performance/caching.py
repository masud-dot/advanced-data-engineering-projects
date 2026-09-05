from pathlib import Path
from typing import Any, Callable
import hashlib
import json


class FileCache:
    def __init__(self, directory: str = "local_cache"):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _key(self, key: str) -> Path:
        digest = hashlib.sha256(
            key.encode("utf-8")
        ).hexdigest()

        return self.directory / f"{digest}.json"

    def get(self, key: str) -> Any:
        path = self._key(key)

        if not path.exists():
            return None

        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def set(self, key: str, value: Any) -> None:
        path = self._key(key)

        with path.open("w", encoding="utf-8") as file:
            json.dump(value, file, indent=2)

    def get_or_compute(
        self,
        key: str,
        function: Callable[[], Any],
    ) -> Any:
        cached = self.get(key)

        if cached is not None:
            return cached

        value = function()
        self.set(key, value)

        return value
