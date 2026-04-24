SHELL := /usr/bin/env bash

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show the help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: lint
lint: ## Run linting checks
	poetry run ruff check --exit-non-zero-on-fix --diff
	poetry run ruff format --check --diff
	poetry run flake8 .

.PHONY: type-check
type-check: ## Run all type checkers we support
	poetry run mypy .

.PHONY: unit
unit: ## Run unit tests with pytest
	poetry run pytest

.PHONY: package
package: ## Check package dependencies
	poetry check
	poetry run pip check

.PHONY: test
test: lint type-check unit package ## Run all checks
