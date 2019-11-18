
from forwarder.format import get_message


def test_get_message(alert_ok):
    formated_alert = get_message(alert_ok)
    expected_output = ("✅ *Disk usage alert on CS30.evilcorp*\n"
                       "_disk usage 93% on rootfs device_\n")
    assert isinstance(formated_alert, str)
    assert formated_alert == expected_output
