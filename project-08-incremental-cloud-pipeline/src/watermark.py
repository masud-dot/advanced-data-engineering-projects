from datetime import datetime


def get_next_watermark(updated_at_values) -> datetime | None:
    """Return the maximum processed updated_at timestamp."""
    if not updated_at_values:
        return None

    return max(updated_at_values)
