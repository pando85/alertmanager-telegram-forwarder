from aiohttp.web import Response, json_response
from aiolambda.typing import Maybe

from forwarder.errors import ResponseError


def return_error(error: Exception) -> Response:
    if isinstance(error, ResponseError):
        return json_response(error.message, status=error.status_code)
    return json_response('Unknow error', status=500)


def return_200(maybe_json: Maybe[dict]) -> Response:
    if isinstance(maybe_json, Exception):
        return return_error(maybe_json)
    return json_response(maybe_json, status=200)
