.PHONY: help install run dev build docker-build docker-run docker-stop clean test

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

install: ## Install dependencies using uv
	uv sync

run: ## Run the bot locally
	uv run python main.py

dev: install run ## Install dependencies and run the bot

build: ## Build the Docker image
	docker build -t slack-copilot:latest .

docker-build: build ## Alias for build

docker-run: ## Run the bot using Docker Compose
	docker-compose up -d

docker-stop: ## Stop the Docker containers
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

clean: ## Clean up temporary files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf .ruff_cache

setup: ## Run the setup script
	./setup.sh
