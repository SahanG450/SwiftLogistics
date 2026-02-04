# SwiftLogistics Makefile

.PHONY: all setup start stop restart logs clean test help

# Default target
all: help

# Setup environment and dependencies
setup:
	@echo "📦 Installing dependencies..."
	@bash scripts/setup-all.sh

# Start all services
start:
	@echo "🚀 Starting SwiftLogistics..."
	@bash scripts/start-all.sh

# Stop all services
stop:
	@echo "🛑 Stopping services..."
	@docker compose down
	@echo "✓ Services stopped"

# Restart all services
restart: stop start

# View logs
logs:
	@docker compose logs -f

# Run tests/health checks
test:
	@echo "🧪 Running health checks..."
	@bash scripts/test-health.sh

# Clean up artifacts and temporary files
clean: stop
	@echo "🧹 Cleaning up..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name "node_modules" -exec rm -rf {} +
	@rm -rf services/mocks/*/venv
	@echo "✓ Cleanup complete"

# Show help
help:
	@echo "SwiftLogistics Management Commands:"
	@echo "  make start   - Start all services (Docker)"
	@echo "  make stop    - Stop all services"
	@echo "  make restart - Restart all services"
	@echo "  make logs    - Follow service logs"
	@echo "  make test    - Run health checks"
	@echo "  make clean   - Remove temp files and containers"
