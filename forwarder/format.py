from jinja2 import Template

from forwarder.config import TEMPLATE_PATH
from forwarder.typing import Alert


# Load template at boot
with open(TEMPLATE_PATH, 'r') as f:
    template = Template(f.read())


def get_message(alert: Alert) -> str:

    return template.render(alert=alert)
