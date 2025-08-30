.PHONY: install test

install:
	uv sync --dev --all-extras

test:
	uv run pytest --cov=src

lint:
	uv run ruff check --fix
	uv run ruff format
	uv run ty check
