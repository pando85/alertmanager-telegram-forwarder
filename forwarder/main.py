from forwarder.app import get_app
from forwarder.logger import access_logger
from forwarder.telegram import setup_telegram_client


def main():
    app = get_app(setup_telegram_client('https://api.telegram.org'))
    app.run(port=8080, access_log=access_logger)
