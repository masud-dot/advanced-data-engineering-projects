import os
import re
from pathlib import Path

import yaml


CONFIG_DIR = Path(__file__).resolve().parent / "configs"


def _expand_environment_variables(value):
    """Recursively replace ${VAR} placeholders with environment values."""
    if isinstance(value, dict):
        return {
            key: _expand_environment_variables(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [_expand_environment_variables(item) for item in value]

    if isinstance(value, str):
        pattern = r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}"

        def replace(match):
            variable = match.group(1)
            return os.getenv(variable, match.group(0))

        return re.sub(pattern, replace, value)

    return value


def load_config(environment=None):
    """Load environment-specific YAML configuration."""
    environment = environment or os.getenv("ENVIRONMENT", "dev")
    config_path = CONFIG_DIR / f"{environment}.yaml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}

    return _expand_environment_variables(config)


if __name__ == "__main__":
    print(load_config())
