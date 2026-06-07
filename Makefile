VENV = venv/bin
PYTHON = $(VENV)/python
RUFF = $(VENV)/ruff
MYPY = $(VENV)/mypy
UVICORN = $(VENV)/uvicorn

.PHONY: db lint test run

db:
	docker compose up -d

lint:
	$(RUFF) check .
	$(MYPY) . --exclude tests/

test:
	$(PYTHON) -m pytest tests -q

run:
	$(UVICORN) main:app --reload --host 0.0.0.0 --port 8000

all: db lint test
	$(UVICORN) main:app --reload --host 0.0.0.0 --port 8000
