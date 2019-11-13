.PHONY: help requirements requirements_test lint test run

APP := forwarder
WORKON_HOME ?= .venv
VENV_BASE := $(WORKON_HOME)/${APP}
VENV_ACTIVATE := $(VENV_BASE)/bin/activate
PYTHON := ${VENV_BASE}/bin/python3

CONTAINER_CMD?=docker

IMAGE_NAME=$(if $(ENV_IMAGE_NAME),$(ENV_IMAGE_NAME),pando85/alertmanager-telegram-forwarder)
IMAGE_VERSION=$(if $(ENV_IMAGE_VERSION),$(ENV_IMAGE_VERSION),latest)

# get build server architecture
ARCH = $(shell uname -m)
ifeq ($(ARCH), aarch64)
  ARCH = arm64
else ifeq ($(ARCH), x86_64)
  ARCH = amd64
else
  $(error "Unsupported architecture: $(ARCH)")
endif


.DEFAULT: help
help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##/\n\t/'

venv:	## create virtualenv
	@if [ ! -d "$(VENV_BASE)" ]; then \
		virtualenv -p python3 $(VENV_BASE); \
	fi

requirements:	## install requirements
requirements: venv
	@echo Install requirements
	@${PYTHON} -m pip install -r requirements.txt > /dev/null

requirements_test:	## install test requirements
requirements_test: requirements
	@echo Install test requirements
	@${PYTHON} -m pip install -r requirements_test.txt > /dev/null

lint:	## run pycodestyle
lint: requirements_test
	@echo Running linter
	@${PYTHON} -m openapi_spec_validator docs/api/v1/openapi.yaml
	@${PYTHON} -m pycodestyle .
	@${PYTHON} -m flake8 ${APP} test
	@${PYTHON} -m mypy --ignore-missing-imports ${APP} test

test:	## run tests and show report
test: lint
	@echo Running tests
	@LOG_LEVEL=DEBUG ${PYTHON} -m coverage run -m pytest test
	@${PYTHON} -m coverage report -m

run:	## run project
run: requirements
	@${PYTHON} -m ${APP}

image:	## build docker image
image:
	$(CONTAINER_CMD) build -t $(IMAGE_NAME):$(IMAGE_VERSION) .

push-image: image
	$(CONTAINER_CMD) tag $(IMAGE_NAME):$(IMAGE_VERSION) $(IMAGE_NAME)-$(ARCH):$(IMAGE_VERSION)
	$(CONTAINER_CMD) push $(IMAGE_VERSION)-$(ARCH):$(IMAGE_VERSION)

# "docker manifest" requires experimental feature enabled
push-manifest: export DOCKER_CLI_EXPERIMENTAL=enabled
push-manifest:
	$(CONTAINER_CMD) manifest create \
		$(IMAGE_VERSION):$(IMAGE_VERSION) \
		$(IMAGE_VERSION)-amd64:$(IMAGE_VERSION) \
		$(IMAGE_VERSION)-arm64:$(IMAGE_VERSION)
	$(CONTAINER_CMD) manifest push --purge $(IMAGE_VERSION):$(IMAGE_VERSION)
