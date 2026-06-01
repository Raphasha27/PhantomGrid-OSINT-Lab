.PHONY: install test lint clean run

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

lint:
	ruff check .

clean:
	rm -rf __pycache__ .pytest_cache build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

run:
	uvicorn api.main:app --reload
