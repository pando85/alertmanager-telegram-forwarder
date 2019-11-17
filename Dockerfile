FROM python:3.7-slim-buster AS compile-image

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.7-slim-buster
WORKDIR /usr/src/app

COPY --from=compile-image /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY docs/api/v1/openapi.yaml ./docs/api/v1/openapi.yaml
COPY forwarder ./forwarder

CMD [ "python", "-m", "forwarder" ]

