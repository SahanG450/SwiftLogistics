.PHONY: help build up down logs clean restart ps

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build all Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d

up-build: ## Build and start all services
	docker-compose up --build -d

down: ## Stop all services
	docker-compose down

logs: ## Show logs from all services
	docker-compose logs -f

logs-api: ## Show API Gateway logs
	docker-compose logs -f api-gateway

logs-orchestrator: ## Show Orchestrator logs
	docker-compose logs -f orchestrator

logs-notification: ## Show Notification Service logs
	docker-compose logs -f notification-service

logs-cms: ## Show CMS Adapter logs
	docker-compose logs -f cms-adapter

logs-ros: ## Show ROS Adapter logs
	docker-compose logs -f ros-adapter

logs-wms: ## Show WMS Adapter logs
	docker-compose logs -f wms-adapter

ps: ## Show running containers
	docker-compose ps

restart: ## Restart all services
	docker-compose restart

restart-api: ## Restart API Gateway
	docker-compose restart api-gateway

restart-orchestrator: ## Restart Orchestrator
	docker-compose restart orchestrator

clean: ## Stop and remove all containers, networks, and volumes
	docker-compose down -v
	docker system prune -f

clean-all: ## Remove everything including images
	docker-compose down -v --rmi all
	docker system prune -af

shell-api: ## Open shell in API Gateway container
	docker-compose exec api-gateway sh

shell-orchestrator: ## Open shell in Orchestrator container
	docker-compose exec orchestrator sh

shell-mongo: ## Open MongoDB shell
	docker-compose exec mongodb mongosh -u admin -p admin123

rabbitmq-ui: ## Open RabbitMQ Management UI in browser
	@echo "Opening RabbitMQ Management UI at http://localhost:15672"
	@echo "Username: admin"
	@echo "Password: admin123"
	@which xdg-open > /dev/null && xdg-open http://localhost:15672 || open http://localhost:15672 || echo "Please open http://localhost:15672 in your browser"

status: ## Check status of all services
	@echo "=== Service Status ==="
	@docker-compose ps
	@echo ""
	@echo "=== Health Checks ==="
	@docker-compose ps --format json | jq -r '.[] | "\(.Service): \(.Health)"'

dev: ## Start services with live logs
	docker-compose up --build

prod: ## Start services in production mode
	docker-compose -f docker-compose.yml up -d
