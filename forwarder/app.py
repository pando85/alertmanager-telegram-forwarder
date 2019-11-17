import connexion
import os

from typing import Callable

from forwarder.config import API_SPECS_PATH


def get_app(setup_telegram_client: Callable) -> connexion.AioHttpApp:
    app = connexion.AioHttpApp(__name__)
    api = app.add_api(os.path.join(os.getcwd(), API_SPECS_PATH),
                      pass_context_arg_name='request',
                      strict_validation=True)
    app.app.on_startup.append(setup_telegram_client(api.subapp))
    return app
