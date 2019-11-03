from aiolambda.logger import access_logger
from aiolambda.app import get_app


def main():
    app = get_app()
    app.run(port=8080, access_log=access_logger)
