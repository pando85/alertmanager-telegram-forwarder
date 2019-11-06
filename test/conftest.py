import json
import pytest


DATA_PATH = 'test/data'


@pytest.fixture(scope='session')
def alerts_all_ok():
    with open(f'{DATA_PATH}/all_ok.json', 'r') as json_data:
        return json.load(json_data)
