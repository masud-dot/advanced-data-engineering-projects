from monitoring.alerts import Alert


def build_email_payload(
    alert: Alert,
    recipient: str,
) -> dict:
    return {
        "recipient": recipient,
        "subject": (
            f"[{alert.severity}] "

 f"{alert.pipeline_name} monitoring alert"
        ),
        "body": (
            f"Rule: {alert.rule}\n"
            f"Message: {alert.message}\n"
            f"Created: {alert.created_at}"
        ),
    }


def send(
    alert: Alert,
    recipient: str,
) -> dict:
    """
    Build an email payload.

    Actual SMTP delivery is intentionally not performed so that
    the project remains safe and locally executable.
    """
    return build_email_payload(alert, recipient)
