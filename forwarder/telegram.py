import aiohttp

from aiofunctools import bind
from typing import Callable
from toolz import curry

from forwarder.config import TELEGRAM_BOT_TOKEN
from forwarder.format import get_message
from forwarder.typing import Alerts, Maybe
from forwarder.errors import ResponseError


@curry
async def setup_telegram_client(telegram_url: str,
                                app: aiohttp.web.Application,
                                _useless_reference: aiohttp.web.Application,
                                ) -> aiohttp.web.Application:
    session = aiohttp.ClientSession()
    bot_endpoint = f'{telegram_url}/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

    async def send_to_telegram(message: dict):
        async with session.post(bot_endpoint, json=message) as resp:
            if resp.status != 200:
                return ResponseError(resp.status, await resp.json())
        return message
    app['telegram_client'] = send_to_telegram
    return app


@bind
async def send_alerts(client: Callable, chat_id: int, alerts: Alerts) -> Maybe[Alerts]:
    for alert in alerts.alerts:
        message = {
            'chat_id': chat_id,
            'text': get_message(alert),
            'parse_mode': 'Markdown',
        }
        maybe_message = await client(message)
        if isinstance(maybe_message, ResponseError):
            return maybe_message
    return alerts
