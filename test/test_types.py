from forwarder.typing import Alert, Alerts


def test_alerts(alerts_all_ok):
    assert isinstance(alerts_all_ok, Alerts)
    assert all([isinstance(alert, Alert) for alert in alerts_all_ok.alerts])
