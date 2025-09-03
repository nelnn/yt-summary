.PHONY: install test

install:
	uv sync --dev --all-extras

test:
	uv run pytest --cov=yt_summary

lint:
	uv run ruff check --fix
	uv run ruff format
	uv run ty check

lint-test:
	uv run ruff check tests/ --fix
	uv run ruff format tests/
