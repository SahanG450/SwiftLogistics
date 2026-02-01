#!/bin/bash

# Docker Python Mock Services Management Script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
COMPOSE_FILE="$PROJECT_ROOT/docker-compose-python-mocks.yml"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_help() {
    echo "Docker Python Mock Services Manager"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build       Build all Docker images"
    echo "  up          Start all services (build if needed)"
    echo "  down        Stop and remove all containers"
    echo "  start       Start existing containers"
    echo "  stop        Stop running containers"
    echo "  restart     Restart all services"
    echo "  logs        Show logs from all services"
    echo "  status      Show status of all services"
    echo "  clean       Remove containers, images, and volumes"
    echo "  test        Run health checks on all services"
    echo "  help        Show this help message"
    echo ""
}

build_services() {
    echo -e "${BLUE}Building Docker images...${NC}"
    cd "$PROJECT_ROOT"
    docker-compose -f "$COMPOSE_FILE" build
    echo -e "${GREEN}✓ Build complete${NC}"
}

start_services() {
    echo -e "${BLUE}Starting services...${NC}"
    cd "$PROJECT_ROOT"
    docker-compose -f "$COMPOSE_FILE" up -d
    echo -e "${GREEN}✓ Services started${NC}"
    echo ""
    show_status
}

stop_services() {
    echo -e "${BLUE}Stopping services...${NC}"
    cd "$PROJECT_ROOT"
    docker-compose -f "$COMPOSE_FILE" stop
    echo -e "${GREEN}✓ Services stopped${NC}"
}

down_services() {
    echo -e "${BLUE}Stopping and removing containers...${NC}"
    cd "$PROJECT_ROOT"
    docker-compose -f "$COMPOSE_FILE" down
    echo -e "${GREEN}✓ Containers removed${NC}"
}

restart_services() {
    echo -e "${BLUE}Restarting services...${NC}"
    cd "$PROJECT_ROOT"
    docker-compose -f "$COMPOSE_FILE" restart
    echo -e "${GREEN}✓ Services restarted${NC}"
}

show_logs() {
    echo -e "${BLUE}Showing logs (Ctrl+C to exit)...${NC}"
    cd "$PROJECT_ROOT"
    docker-compose -f "$COMPOSE_FILE" logs -f
}

show_status() {
    echo -e "${BLUE}Service Status:${NC}"
    cd "$PROJECT_ROOT"
    docker-compose -f "$COMPOSE_FILE" ps
    echo ""
    
    # Check health
    echo -e "${BLUE}Health Status:${NC}"
    for service in cms-mock ros-mock wms-mock; do
        health=$(docker inspect --format='{{.State.Health.Status}}' "$service" 2>/dev/null || echo "not running")
        if [ "$health" = "healthy" ]; then
            echo -e "  ${GREEN}✓${NC} $service: $health"
        elif [ "$health" = "not running" ]; then
            echo -e "  ${RED}✗${NC} $service: $health"
        else
            echo -e "  ${YELLOW}⚠${NC} $service: $health"
        fi
    done
}

clean_services() {
    echo -e "${YELLOW}This will remove all containers, images, and volumes.${NC}"
    read -p "Are you sure? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}Cleaning up...${NC}"
        cd "$PROJECT_ROOT"
        docker-compose -f "$COMPOSE_FILE" down -v --rmi all
        echo -e "${GREEN}✓ Cleanup complete${NC}"
    else
        echo "Cancelled"
    fi
}

test_services() {
    echo -e "${BLUE}Running health checks...${NC}"
    echo ""
    
    # Wait for services to be ready
    sleep 5
    
    PASSED=0
    FAILED=0
    
    for service in "cms-mock:3001" "ros-mock:3002" "wms-mock:3003"; do
        name=$(echo $service | cut -d: -f1)
        port=$(echo $service | cut -d: -f2)
        
        echo -n "Testing $name... "
        response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$port/health)
        
        if [ "$response" = "200" ]; then
            echo -e "${GREEN}✓ PASSED${NC} (HTTP $response)"
            ((PASSED++))
        else
            echo -e "${RED}✗ FAILED${NC} (HTTP $response)"
            ((FAILED++))
        fi
    done
    
    echo ""
    echo "Results: ${GREEN}$PASSED passed${NC}, ${RED}$FAILED failed${NC}"
    
    if [ $FAILED -eq 0 ]; then
        echo -e "${GREEN}All services are healthy!${NC}"
        return 0
    else
        echo -e "${RED}Some services are unhealthy!${NC}"
        return 1
    fi
}

# Main command handling
case "${1:-help}" in
    build)
        build_services
        ;;
    up)
        start_services
        ;;
    down)
        down_services
        ;;
    start)
        cd "$PROJECT_ROOT"
        docker-compose -f "$COMPOSE_FILE" start
        echo -e "${GREEN}✓ Services started${NC}"
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    logs)
        show_logs
        ;;
    status)
        show_status
        ;;
    clean)
        clean_services
        ;;
    test)
        test_services
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
