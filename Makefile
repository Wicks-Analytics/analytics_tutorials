.PHONY: help install install-dev test lint format clean setup-data

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install project dependencies
	uv pip install -e .

install-dev:  ## Install project with development dependencies
	uv pip install -e ".[all]"
	pre-commit install

install-jupyter:  ## Install with Jupyter support
	uv pip install -e ".[jupyter]"

test:  ## Run tests
	pytest

test-cov:  ## Run tests with coverage report
	pytest --cov=. --cov-report=term-missing --cov-report=html

test-fast:  ## Run tests in parallel
	pytest -n auto

lint:  ## Run linting checks
	ruff check .

lint-fix:  ## Run linting and auto-fix issues
	ruff check . --fix

format:  ## Format code with ruff and black
	ruff format .
	black .

format-check:  ## Check code formatting without making changes
	ruff format --check .
	black --check .

quality:  ## Run all quality checks (lint + format check)
	ruff check .
	ruff format --check .
	black --check .

setup-data:  ## Generate sample data for tutorials
	python setup_database.py

clean:  ## Clean up generated files
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

pre-commit:  ## Run pre-commit hooks on all files
	pre-commit run --all-files

tutorial-beginner:  ## Run beginner tutorials
	python tutorials/01_beginner/01_lift_analysis.py
	python tutorials/01_beginner/02_roc_analysis.py
	python tutorials/01_beginner/03_regression_metrics.py

tutorial-setup:  ## Run setup tutorial
	python tutorials/00_getting_started/00_setup_and_polars_basics.py

convert-notebooks:  ## Convert Python scripts to Jupyter notebooks
	python convert_to_notebooks.py

ci:  ## Run CI checks locally (lint, format, test)
	@echo "Running linting..."
	ruff check .
	@echo "Running format check..."
	ruff format --check .
	black --check .
	@echo "Running tests..."
	pytest -v
	@echo "All CI checks passed!"
