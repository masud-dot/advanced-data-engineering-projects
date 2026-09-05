from monitoring.alerts import Alert


def send(alert: Alert) -> None:
    print(
        f"[ALERT] [{alert.severity}] "
        f"{alert.pipeline_name} | "
        f"{alert.rule} | "
        f"{alert.message}"
    )


def send_all(alerts: list[Alert]) -> None:
    for alert in alerts:
        send(alert)
