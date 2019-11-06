import json
import pytest

from forwarder.types import Alerts

DATA_PATH = 'test/data'


@pytest.fixture(scope='session')
def alerts_all_ok_dict():
    with open(f'{DATA_PATH}/all_ok.json', 'r') as json_data:
        return json.load(json_data)


@pytest.fixture(scope='session')
def alerts_all_ok(alerts_all_ok_dict):
    return Alerts.from_dict(alerts_all_ok_dict)


@pytest.fixture(scope='session')
def alert_ok(alerts_all_ok):
    return alerts_all_ok.alerts[0]


@pytest.fixture(scope='session')
def chat_id():
    return 1234567
