from aiofunctools import compose
from aiohttp.web import Response

from aiolambda import logger

from forwarder.response import return_200
from forwarder.telegram import send_alerts
from forwarder.types import Alerts


async def forward_alerts(chat_id, **extra_args) -> Response:
    return await compose(
        Alerts.from_dict,
        logger.debug,
        send_alerts(extra_args['request'].app['telegram_client'], chat_id),
        logger.debug,
        return_200)(await extra_args['request'].json())


async def ping() -> Response:
    return compose(
        logger.debug,
        return_200)('pong')
