
# Makefile for the Prompting Workbench project
.PHONY: help install setup run lint format lint-fix test clean

# Use SHELL to ensure bash is used for consistency
SHELL := /bin/bash

# If the first argument is "run"...
ifeq (run,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

# Default target: 'help'
help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies using uv in editable mode with dev dependencies."
	@echo "  setup      - Alias for install."
	@echo "  run        - Run the prompting_workbench CLI. Pass arguments with ARGS. Example: make run ARGS=\"--project my_first_project\""
	@echo "  lint       - Check for linting errors using ruff."
	@echo "  format     - Format the code using ruff."
	@echo "  lint-fix   - Fix linting errors automatically with ruff."
	@echo "  test       - Run tests with pytest."
	@echo "  clean      - Remove temporary files and build artifacts."

# Target to install dependencies
install:
	@echo "--- Installing dependencies using uv ---"
	uv sync --dev

# Alias for install
setup: install

# Target to run the CLI
run:
	@echo "--- Running Prompting Workbench CLI ---"
	@echo "Arguments: $(RUN_ARGS)"
	uv run prompting_workbench $(RUN_ARGS)

# Target for linting
lint:
	@echo "--- Linting with ruff ---"
	uv run ruff check .

# Target for formatting
format:
	@echo "--- Formatting with ruff ---"
	uv run ruff format .

# Target for fixing lint errors
lint-fix:
	@echo "--- Fixing lint errors with ruff ---"
	uv run ruff check . --fix

# Target for running tests
test:
	@echo "--- Running tests with pytest ---"
	uv run pytest

# Target to clean the project
clean:
	@echo "--- Cleaning up project ---"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .venv .pytest_cache .ruff_cache dist build *.egg-info
