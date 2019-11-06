import pytest

from aiolambda.app import get_app


BASE_URL = '/v1'


@pytest.fixture
def cli(loop, aiohttp_client):
    app = get_app()
    return loop.run_until_complete(aiohttp_client(app.app))


async def test_forward_alerts(cli, alerts_all_ok):
    resp = await cli.post(f'{BASE_URL}/alerts/1234567', json=alerts_all_ok)
    assert resp.status == 200
    assert await resp.json() == alerts_all_ok


async def test_ping(cli):
    resp = await cli.get(f'{BASE_URL}/ping')
    assert resp.status == 200
    assert await resp.json() == 'pong'
