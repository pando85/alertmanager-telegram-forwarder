from aiofunctools import bind, compose
from aiohttp.web import Response

from forwarder import logger
from forwarder.response import return_200
from forwarder.telegram import send_alerts
from forwarder.typing import Alerts


async def forward_alerts(chat_id, **extra_args) -> Response:
    return await compose(
        logger.debug,
        Alerts.from_dict,
        logger.debug,
        send_alerts(extra_args['request'].app['telegram_client'], chat_id),
        logger.debug,
        bind(lambda x: x.as_dict()),
        return_200)(await extra_args['request'].json())


async def ping() -> Response:
    return compose(
        logger.debug,
        return_200)('pong')
