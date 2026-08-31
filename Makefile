.PHONY: help venv install lint test smoke preflight clean

PY ?= python3.12
VENV := .venv

help:
	@echo "Targets:"
	@echo "  venv       create local virtualenv"
	@echo "  install    install package + dev extras"
	@echo "  lint       ruff + bandit"
	@echo "  test       hermetic unit tests"
	@echo "  smoke      end-to-end smoke with synthetic inputs"
	@echo "  preflight  validate license manifests"

venv:
	$(PY) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip

install: venv
	$(VENV)/bin/pip install -e .[dev,data]

lint:
	$(VENV)/bin/ruff check src tests scripts
	$(VENV)/bin/ruff format --check src tests scripts
	$(VENV)/bin/bandit -q -r src

test:
	$(VENV)/bin/pytest -m "not gpu and not integration" --cov=medimage_model

smoke:
	$(VENV)/bin/python -m medimage_model.cli smoke

preflight:
	$(VENV)/bin/python scripts/license_preflight.py data/permissive_only/manifests

clean:
	rm -rf $(VENV) build dist *.egg-info .pytest_cache .ruff_cache .coverage htmlcov
