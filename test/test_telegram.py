import pytest

from aiohttp import web

from forwarder.telegram import send_alert


async def fake_send(request):
    assert request.match_info['bot_id'][0:3] == 'bot'
    body = await request.json()
    assert isinstance(body['chat_id'], int)
    assert isinstance(body['text'], str)
    return web.Response()


def get_fake_telegram():
    app = web.Application()
    app.add_routes([web.post('/{bot_id}/sendMessage', fake_send)])
    return app


@pytest.fixture
def fake_telegram_cli(loop, aiohttp_client):
    app = get_fake_telegram()
    server_config = {}
    return loop.run_until_complete(aiohttp_client(app, server_kwargs=server_config))


async def test_send_to_telegram(fake_telegram_cli, chat_id, alert_ok):
    alert_response = await send_alert(fake_telegram_cli, chat_id, alert_ok, '')
    assert alert_response == alert_ok
