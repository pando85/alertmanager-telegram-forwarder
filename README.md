# alertmanager-telegram-forwarder [![Build Status](https://travis-ci.org/pando85/alertmanager-telegram-forwarder.svg?branch=master)](https://travis-ci.org/pando85/alertmanager-telegram-forwarder)

Alertmanager webhook to forward notifications to telegram.

## Lint

Lint: `make lint`

## Dev

Run app: `make run`

## Tests

Run tests: `make test`

### Production

**Warning**: aiohttp is [slower with gnunicorn](https://docs.aiohttp.org/en/stable/deployment.html#start-gunicorn). Basic `python -m my_app` execution is prefered.
