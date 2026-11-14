.PHONY: test lint format check pilot all clean

test:
	uv run pytest -q

lint:
	uv run ruff check .

format:
	uv run ruff format .

check: lint
	uv run ruff format --check .
	uv run pytest -q

pilot:
	uv run parity run --condition baseline --split pilot
	uv run parity label --split pilot
	uv run parity analyze --split pilot

all: check

clean:
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info
