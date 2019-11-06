from aiofunctools import compose
from aiohttp.web import Response

from aiolambda import logger

from forwarder.response import return_200


async def forward_alerts(chat_id, **extra_args) -> Response:
    return compose(
        logger.debug,
        return_200)(await extra_args['request'].json())


async def ping() -> Response:
    return compose(
        logger.debug,
        return_200)('pong')
