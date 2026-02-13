.PHONY: help build up down logs clean restart ps start-mocks stop-mocks logs-mocks health-mocks run-frontend install-frontend build-frontend run-backend run-backend-detached stop-backend run-all

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\\n", $$1, $$2}' $(MAKEFILE_LIST)

# Full System Commands
build: ## Build all Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d

up-build: ## Build and start all services
	docker-compose up --build -d

down: ## Stop all semakervices
	docker-compose down

# Mock Services Commands
start-mocks: ## Start only mock services (CMS, WMS, ROS)
	docker-compose up -d cms-mock wms-mock ros-mock

stop-mocks: ## Stop only mock services
	docker-compose stop cms-mock wms-mock ros-mock

restart-mocks: ## Restart all mock services
	docker-compose restart cms-mock wms-mock ros-mock

logs-mocks: ## Show logs from all mock services
	docker-compose logs -f cms-mock wms-mock ros-mock

logs-cms-mock: ## Show CMS Mock logs
	docker-compose logs -f cms-mock

logs-wms-mock: ## Show WMS Mock logs
	docker-compose logs -f wms-mock

logs-ros-mock: ## Show ROS Mock logs
	docker-compose logs -f ros-mock

health-mocks: ## Check health of all mock services
	@echo "=== Mock Services Health Check ==="
	@echo "CMS Mock (Port 3001):"
	@curl -s http://localhost:3001/health | jq || echo "  ❌ Not responding"
	@echo ""
	@echo "WMS Mock (Port 3002):"
	@curl -s http://localhost:3002/health | jq || echo "  ❌ Not responding"
	@echo ""
	@echo "ROS Mock (Port 3003):"
	@curl -s http://localhost:3003/health | jq || echo "  ❌ Not responding"

# Core Services Commands 
logs: ## Show logs from all services
	docker-compose logs -f

logs-api: ## Show API Gateway logs
	docker-compose logs -f api-gateway

logs-orchestrator: ## Show Orchestrator logs
	docker-compose logs -f orchestrator

logs-notification: ## Show Notification Service logs
	docker-compose logs -f notification-service

# Adapter Commands
logs-cms: ## Show CMS Adapter logs
	docker-compose logs -f cms-adapter

logs-ros: ## Show ROS Adapter logs
	docker-compose logs -f ros-adapter

logs-wms: ## Show WMS Adapter logs
	docker-compose logs -f wms-adapter

# Container Management
ps: ## Show running containers
	docker-compose ps

restart: ## Restart all services
	docker-compose restart

restart-api: ## Restart API Gateway
	docker-compose restart api-gateway

restart-orchestrator: ## Restart Orchestrator
	docker-compose restart orchestrator

# Cleanup Commands
clean: ## Stop and remove all containers, networks, and volumes
	docker-compose down -v
	docker system prune -f

clean-all: ## Remove everything including images
	docker-compose down -v --rmi all
	docker system prune -af

# Shell Access
shell-api: ## Open shell in API Gateway container
	docker-compose exec api-gateway sh

shell-orchestrator: ## Open shell in Orchestrator container
	docker-compose exec orchestrator sh

shell-cms-mock: ## Open shell in CMS Mock container
	docker-compose exec cms-mock sh

shell-wms-mock: ## Open shell in WMS Mock container
	docker-compose exec wms-mock sh

shell-ros-mock: ## Open shell in ROS Mock container
	docker-compose exec ros-mock sh

shell-mongo: ## Open MongoDB shell
	docker-compose exec mongodb mongosh -u admin -p admin123

# UI Access
rabbitmq-ui: ## Open RabbitMQ Management UI in browser
	@echo "Opening RabbitMQ Management UI at http://localhost:15672"
	@echo "Username: admin"
	@echo "Password: admin123"
	@which xdg-open > /dev/null && xdg-open http://localhost:15672 || open http://localhost:15672 || echo "Please open http://localhost:15672 in your browser"

# API Documentation
api-docs: ## Open API documentation for all mock services
	@echo "Opening Mock Service API Documentation..."
	@echo "CMS Mock: http://localhost:3001/docs"
	@echo "WMS Mock: http://localhost:3002/docs"
	@echo "ROS Mock: http://localhost:3003/docs"
	@which xdg-open > /dev/null && (xdg-open http://localhost:3001/docs & xdg-open http://localhost:3002/docs & xdg-open http://localhost:3003/docs) || (open http://localhost:3001/docs & open http://localhost:3002/docs & open http://localhost:3003/docs) || echo "Please open the URLs above in your browser"

# Status and Health
status: ## Check status of all services
	@echo "=== Service Status ==="
	@docker-compose ps
	@echo ""
	@echo "=== Infrastructure Services ==="
	@echo "MongoDB: http://localhost:27017"
	@echo "RabbitMQ: http://localhost:15672"
	@echo ""
	@echo "=== Mock Services ==="
	@echo "CMS Mock: http://localhost:3001"
	@echo "WMS Mock: http://localhost:3002"
	@echo "ROS Mock: http://localhost:3003"
	@echo ""
	@echo "=== Core Services ==="
	@echo "API Gateway: http://localhost:3000"

# Development Modes
dev: ## Start services with live logs
	docker-compose up --build

dev-mocks: ## Start only mock services with live logs (for testing)
	docker-compose up --build cms-mock wms-mock ros-mock

prod: ## Start services in production mode
	docker-compose -f docker-compose.yml up -d

# Quick Start Commands
quick-start: up health-mocks ## Quick start: build and start all services, then check mock health
	@echo ""
	@echo "✅ SwiftLogistics is starting up!"
	@echo "Run 'make status' to see all service URLs"

# Frontend Commands
run-frontend: ## Run the frontend development server
	@echo "Starting frontend development server..."
	cd frontend/swifttrack-logistics && npm run dev

install-frontend: ## Install frontend dependencies
	@echo "Installing frontend dependencies..."
	cd frontend/swifttrack-logistics && npm install

build-frontend: ## Build the frontend for production
	@echo "Building frontend for production..."
	cd frontend/swifttrack-logistics && npm run build

# Backend Commands
run-backend: ## Start all backend services using Docker Compose
	@echo "Starting all backend services..."
	docker-compose up --build

run-backend-detached: ## Start all backend services in detached mode
	@echo "Starting all backend services in background..."
	docker-compose up --build -d

stop-backend: ## Stop all backend services
	@echo "Stopping all backend services..."
	docker-compose down

# Combined Commands
run-all: ## Run both frontend and backend (backend in background, frontend in foreground)
	@echo "Starting backend services in background..."
	@make run-backend-detached
	@echo "Waiting for services to be ready..."
	@sleep 5
	@echo ""
	@echo "Starting frontend development server..."
	@echo "Backend services are running at:"
	@echo "  - API Gateway: http://localhost:3000"
	@echo "  - RabbitMQ UI: http://localhost:15672"
	@echo "  - MongoDB: http://localhost:27017"
	@echo ""
	@make run-frontend

test-mocks: ## Test all mock services with sample requests
	@echo "=== Testing Mock Services ==="
	@echo ""
	@echo "Testing CMS Mock..."
	@curl -s http://localhost:3001/health | jq || echo "❌ CMS Mock failed"
	@echo ""
	@echo "Testing WMS Mock..."
	@curl -s http://localhost:3002/health | jq || echo "❌ WMS Mock failed"
	@echo ""
	@echo "Testing ROS Mock..."
	@curl -s http://localhost:3003/health | jq || echo "❌ ROS Mock failed"
