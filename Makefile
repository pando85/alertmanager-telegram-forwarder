.PHONY: help requirements requirements_test lint test run

APP := forwarder
WORKON_HOME ?= .venv
VENV_BASE := $(WORKON_HOME)/${APP}
VENV_ACTIVATE := $(VENV_BASE)/bin/activate
PYTHON := ${VENV_BASE}/bin/python3

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

