# alertmanager-telegram-forwarder [![Build Status](https://travis-ci.org/pando85/alertmanager-telegram-forwarder.svg?branch=master)](https://travis-ci.org/pando85/alertmanager-telegram-forwarder)  [![](https://images.microbadger.com/badges/image/pando85/alertmanager-telegram-forwarder.svg)](https://cloud.docker.com/repository/docker/pando85/alertmanager-telegram-forwarder) [![](https://images.microbadger.com/badges/version/pando85/alertmanager-telegram-forwarder.svg)](https://cloud.docker.com/repository/docker/pando85/alertmanager-telegram-forwarder) [![License](https://img.shields.io/github/license/pando85/alertmanager-telegram-forwarder.svg)](https://github.com/pando85/alertmanager-telegram-forwarder/blob/master/LICENSE)

Alertmanager webhook to forward notifications to telegram using templates and based in [OpenAPI specs](docs/api/v1/openapi.yaml).

## Config

| *Env* | *Description* | *Default* |
|---------|---------------|-----------|
|`API_SPECS_PATH`| OpenAPI specs path | `docs/api/v1/openapi.yaml` |
|`LOG_LEVEL`| Log level: `[DEBUG, INFO, WARNING, ERROR, CRITICAL]`| `INFO` |
|`TELEGRAM_BOT_TOKEN`| Telegram bot token | `` |
|`TEMPLATE_PATH`| Jinja2 template used to forward messages | | `forwarder/resources/templates/default.j2` |

### Alertmanager

Must set up a [webhook_config](https://prometheus.io/docs/alerting/configuration/#webhook_config) in `alertmanager.yml`. Replace `{CHAT_ID}` with a desired Telegram chat ID.

```yaml
receivers:
- name: telegram
  webhook_configs:
  - send_resolved: true
    http_config: {}
    url: http://alertmanager-telegram-forwarder:8080/v1/alerts/{CHAT_ID}
```

You can contact with [@myidbot](https://telegram.me/myidbot) to get your current chat ID.

## Deployment

- [Kubernetes example](k8s/example.yml)
