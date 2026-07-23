.PHONY: run test

run:
	uv run uvicorn src.main:app --reload

test:
	uv run python -m pytest tests -vvu