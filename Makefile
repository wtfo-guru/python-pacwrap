SHELL:=/usr/bin/env bash

PROJECT ?= $(shell git rev-parse --show-toplevel)
DISTRO ?= ubuntu20.04
PYVERS = 3.10.9

.PHONY: black
black:
	poetry run isort .
	poetry run black .

.PHONY: mypy
mypy: black
	poetry run mypy pacwrap tests/*.py

.PHONY: ghlint
ghlint:
	# poetry run mypy pacwrap tests/**/*.py
	poetry run mypy pacwrap tests/*.py
	# poetry run flake8 .
	poetry run doc8 -q docs

.PHONY: lint
lint: mypy
	poetry run flake8 .
	poetry run doc8 -q docs

.PHONY: sunit
sunit:
	poetry run pytest -s tests

.PHONY: unit
unit:
	poetry run pytest tests

.PHONY: package
package:
	poetry check
	poetry run pip check
	poetry run safety check -i 51457 --full-report

.PHONY: ghtest
ghtest: ghlint package unit

.PHONY: test
test: lint package unit

.PHONY: work
work:
	docker run --rm -it --volume $(PROJECT):/project/ poetry-$(DISTRO)-$(PYVERS) /bin/bash

.PHONY: docs
docs:
	@cd docs && $(MAKE) $@

.PHONY: clean clean-build clean-pyc clean-test
clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -fr .mypy_cache
