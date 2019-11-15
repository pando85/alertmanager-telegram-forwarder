import pytest

from aiohttp import web

from forwarder.errors import ResponseError
from forwarder.telegram import send_alerts


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


@pytest.fixture
def fake_telegram_cli(loop, aiohttp_client):
    app = get_fake_telegram()
    session = loop.run_until_complete(aiohttp_client(app))
    bot_endpoint = f'/botMOCK_TOKEN/sendMessage'

    async def send_to_telegram(message: dict):
        async with session.post(bot_endpoint, json=message) as resp:
            if resp.status != 200:
                return ResponseError(resp.status, await resp.json())
        return message
    return send_to_telegram


@pytest.fixture
def fake_telegram_cli_fail(loop, aiohttp_client):
    app = get_fake_telegram()
    session = loop.run_until_complete(aiohttp_client(app))
    bot_endpoint = f'/notFound'

    async def send_to_telegram(message: dict):
        async with session.post(bot_endpoint, json=message) as resp:
            if resp.status != 200:
                return ResponseError(resp.status, await resp.json())
        return message
    return send_to_telegram


async def test_send_to_telegram(fake_telegram_cli, chat_id, alerts_all_ok):
    alerts_response = await send_alerts(fake_telegram_cli, chat_id, alerts_all_ok)
    assert alerts_response == alerts_all_ok


async def test_send_to_telegram_fail(fake_telegram_cli_fail, chat_id, alerts_all_ok):
    alerts_response = await send_alerts(fake_telegram_cli_fail, chat_id, alerts_all_ok)
    expected_result = ResponseError(404, {'error': 'Not Found'})
    assert isinstance(alerts_response, ResponseError)
    assert alerts_response.status_code == expected_result.status_code
    assert alerts_response.message == expected_result.message
