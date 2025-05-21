# Detect OS and set correct script folder
PYTHON_BIN ?= python
VENV := .venv

ifeq ($(OS),Windows_NT)
  VENV_BIN := $(VENV)/Scripts
  PYTHON := $(VENV_BIN)/python.exe
  PIP := $(VENV_BIN)/pip.exe
  PYTEST := $(VENV_BIN)/pytest.exe
  BLACK := $(VENV_BIN)/black.exe
  ISORT := $(VENV_BIN)/isort.exe
  PRE_COMMIT := $(VENV_BIN)/pre-commit.exe
else
  VENV_BIN := $(VENV)/bin
  PYTHON := $(VENV_BIN)/python
  PIP := $(VENV_BIN)/pip
  PYTEST := $(VENV_BIN)/pytest
  BLACK := $(VENV_BIN)/black
  ISORT := $(VENV_BIN)/isort
  PRE_COMMIT := $(VENV_BIN)/pre-commit
endif

REQ := requirements.txt
REQ_DEV := requirements-dev.txt

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Usage:"
	@echo "  make venv [PYTHON_BIN=...]  Create virtualenv with optional Python binary"
	@echo "  make install                Install runtime dependencies"
	@echo "  make dev-install            Install dev/test dependencies"
	@echo "  make test                   Run tests"
	@echo "  make lint                   Run flake8"
	@echo "  make format                 Run black + isort"
	@echo "  make check                  Run format, lint, test"
	@echo "  make clean                  Remove __pycache__ and *.pyc"

.PHONY: venv
venv:
	@test -d $(VENV) || $(PYTHON_BIN) -m venv $(VENV)
	@echo "✅ Virtual environment created using $(PYTHON_BIN)"

.PHONY: install
install: venv
	$(PIP) install -r $(REQ)

.PHONY: dev-install
dev-install: venv
	$(PIP) install -r $(REQ)
	$(PIP) install -r $(REQ_DEV)
	$(PIP) install pre-commit

.PHONY: pre-commit-install
pre-commit-install: venv
	$(PRE_COMMIT) install

.PHONY: pre-commit-run
pre-commit-run: venv
	$(PRE_COMMIT) run --all-files

.PHONY: test
test: dev-install venv
	$(PYTEST) -v tests/

.PHONY: build
build: clean venv
	$(PYTHON) -m pip install --upgrade build
	$(PYTHON) -m build

.PHONY: upload
upload: build
	$(PYTHON) -m pip install --upgrade twine
	$(PYTHON) -m twine upload dist/*

.PHONY: upload-test
upload-test: build
	$(PYTHON) -m pip install --upgrade twine
	$(PYTHON) -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: format
format: venv
	$(BLACK) components tests
	$(ISORT) components tests

.PHONY: lint
lint: venv
	$(VENV_BIN)/flake8 components tests

.PHONY: check
check: format lint test

.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
