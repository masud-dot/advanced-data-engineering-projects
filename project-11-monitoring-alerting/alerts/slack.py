from monitoring.alerts import Alert


def build_slack_payload(alert: Alert) -> dict:
    return {
        "text": (
            f"[{alert.severity}] "
            f"{alert.pipeline_name}: "
            f"{alert.message}"
        )
    }


def send(alert: Alert) -> dict:
    """
    Build a Slack webhook payload.

    Actual HTTP delivery is intentionally not performed.
    """
    return build_slack_payload(alert)
