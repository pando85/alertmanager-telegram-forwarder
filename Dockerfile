FROM python:3.7-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY docs/api/v1/openapi.yaml ./docs/api/v1/openapi.yaml
COPY forwarder ./forwarder

CMD [ "python", "-m", "forwarder" ]

