import json
import pytest

from aiolambda.app import get_app


BASE_URL = '/v1'
DATA_PATH = 'test/data'


@pytest.fixture
def cli(loop, aiohttp_client):
    app = get_app()
    return loop.run_until_complete(aiohttp_client(app.app))


@pytest.fixture(scope='session')
def alerts_all_ok():
    with open(f'{DATA_PATH}/all_ok.json', 'r') as json_data:
        return json.load(json_data)


async def test_forward_alerts(cli, alerts_all_ok):
    resp = await cli.post(f'{BASE_URL}/', json=alerts_all_ok)
    assert resp.status == 200
    assert await resp.json() == alerts_all_ok


async def test_ping(cli):
    resp = await cli.get(f'{BASE_URL}/ping')
    assert resp.status == 200
    assert await resp.json() == 'pong'
