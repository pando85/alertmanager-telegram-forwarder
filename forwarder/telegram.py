import aiohttp

from aiolambda.typing import Maybe
from aiofunctools import bind

from forwarder.config import TELEGRAM_BOT_TOKEN
from forwarder.types import Alert, Alerts
from forwarder.errors import ResponseError


@bind
async def send_alerts(chat_id: int, alerts: Alerts) -> Maybe[Alerts]:
    async with aiohttp.ClientSession() as session:
        maybe_alerts = [await send_alert(session, chat_id, alert) for alert in alerts.alerts]
        for maybe_alert in maybe_alerts:
            if isinstance(maybe_alert, ResponseError):
                return maybe_alert
        return maybe_alerts


@bind
async def send_alert(
        session: aiohttp.ClientSession,
        chat_id: int,
        alert: Alert,
        base_url: str = 'https://api.telegram.org',
        ) -> Maybe[Alert]:
    bot_endpoint = f'{base_url}/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    message = {
        'chat_id': chat_id,
        'text': str(alert),
    }
    async with session.post(bot_endpoint, json=message) as resp:
        if resp.status != 200:
            return ResponseError(resp.status, await resp.json())
    return alert
