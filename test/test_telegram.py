from forwarder.errors import ResponseError
from forwarder.telegram import send_alerts


async def test_send_to_telegram(fake_telegram_cli, chat_id, alerts_all_ok):
    alerts_response = await send_alerts(fake_telegram_cli, chat_id, alerts_all_ok)
    assert alerts_response == alerts_all_ok


async def test_send_to_telegram_fail(fake_telegram_cli_fail, chat_id, alerts_all_ok):
    alerts_response = await send_alerts(fake_telegram_cli_fail, chat_id, alerts_all_ok)
    expected_result = ResponseError(404, {'error': 'Not Found'})
    assert isinstance(alerts_response, ResponseError)
    assert alerts_response.status_code == expected_result.status_code
    assert alerts_response.message == expected_result.message
