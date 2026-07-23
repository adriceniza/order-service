.PHONY: run test

run:
	uv run uvicorn app.main:app --reload

test:
	uv run python -m pytest tests -vv