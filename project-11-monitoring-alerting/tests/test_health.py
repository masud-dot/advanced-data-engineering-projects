from datetime import datetime, timedelta, timezone

from monitoring.health import (
    check_duration,
    check_error_rate,
    check_freshness,
    check_output_volume,
    check_quality_score,
)


def test_output_volume_healthy():
    result = check_output_volume(100, 1)

    assert result.healthy
    assert result.status == "HEALTHY"


def test_output_volume_unhealthy():
    result = check_output_volume(0, 1)

    assert not result.healthy
    assert result.status == "UNHEALTHY"


def test_error_rate():
    healthy = check_error_rate(100, 5, 0.10)
    unhealthy = check_error_rate(100, 20, 0.10)

    assert healthy.healthy
    assert not unhealthy.healthy


def test_duration():
    healthy = check_duration(5, 30)
    unhealthy = check_duration(45, 30)

    assert healthy.healthy
    assert not unhealthy.healthy


def test_quality_score():
    healthy = check_quality_score(0.99, 0.95)
    unhealthy = check_quality_score(0.80, 0.95)

    assert healthy.healthy
    assert not unhealthy.healthy


def test_freshness():
    recent = datetime.now(timezone.utc) - timedelta(minutes=5)
    old = datetime.now(timezone.utc) - timedelta(minutes=120)

    assert check_freshness(recent, 60).healthy
    assert not check_freshness(old, 60).healthy
    assert not check_freshness(None, 60).healthy
