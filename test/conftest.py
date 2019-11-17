import json
import pytest

from aiohttp import web

from forwarder.errors import ResponseError

from forwarder.typing import Alerts

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


async def fake_send(request):
    assert request.match_info['bot_id'][0:3] == 'bot'
    body = await request.json()
    assert isinstance(body['chat_id'], int)
    assert isinstance(body['text'], str)
    return web.Response()


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        if response.status != 404:
            return response
        message = response.message
    except web.HTTPException as ex:
        if ex.status != 404:
            raise
        message = ex.reason
    return web.json_response({'error': message}, status=404)


def get_fake_telegram():
    app = web.Application(middlewares=[error_middleware])
    app.add_routes([web.post('/{bot_id}/sendMessage', fake_send)])
    return app


def generate_fake_telegram_cli(loop, aiohttp_client, bot_endpoint):
    app = get_fake_telegram()
    session = loop.run_until_complete(aiohttp_client(app))

    async def send_to_telegram(message: dict):
        async with session.post(bot_endpoint, json=message) as resp:
            if resp.status != 200:
                return ResponseError(resp.status, await resp.json())
        return message
    return send_to_telegram


@pytest.fixture
def fake_telegram_cli(loop, aiohttp_client):
    return generate_fake_telegram_cli(loop, aiohttp_client, '/botMOCK_TOKEN/sendMessage')


@pytest.fixture
def fake_telegram_cli_fail(loop, aiohttp_client):
    return generate_fake_telegram_cli(loop, aiohttp_client, '/notFound')
