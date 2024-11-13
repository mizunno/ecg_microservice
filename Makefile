.PHONY: help install test lint format clean run docker-build docker-run

# Python settings
PYTHON := python3.10.9
VENV := venv
UV := uv
PYTEST := $(VENV)/bin/pytest
BLACK := $(VENV)/bin/black

help:
	@echo "Available commands:"
	@echo "install      - Install dependencies in a virtual environment"
	@echo "test         - Run tests with coverage"
	@echo "format       - Format code with black"
	@echo "clean        - Remove virtual environment and cache files"
	@echo "run          - Run the FastAPI application"
	@echo "docker-build - Build Docker image"
	@echo "docker-run   - Run application in Docker container"

$(VENV)/bin/activate:
	$(UV) venv $(VENV)

install: $(VENV)/bin/activate
	$(UV) pip install -r requirements.txt
	$(UV) pip install flake8 black pytest-cov

test:
	$(PYTEST) app/tests/ -v --cov=app

format:
	$(BLACK) app/

clean:
	rm -rf $(VENV)
	rm -rf .pytest_cache
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run: install
	$(VENV)/bin/fastapi dev app/main.py

docker-build:
	docker build -t ecg-service .

docker-run:
	docker run -p 8000:8000 ecg-service
