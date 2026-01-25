#!/bin/bash

# Health Check Script for SwiftLogistics
# Verifies all services are running and responding correctly

set -e

echo "🏥 SwiftLogistics Health Check"
echo "=============================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check HTTP endpoint
check_http() {
    local service=$1
    local url=$2
    local expected_code=${3:-200}
    
    printf "Checking %-25s ... " "$service"
    
    if response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null); then
        if [ "$response" -eq "$expected_code" ] || [ "$response" -eq 404 ] || [ "$response" -eq 401 ]; then
            echo -e "${GREEN}✓ OK${NC} (HTTP $response)"
            return 0
        else
            echo -e "${RED}✗ FAIL${NC} (HTTP $response)"
            return 1
        fi
    else
        echo -e "${RED}✗ NOT REACHABLE${NC}"
        return 1
    fi
}

# Function to check TCP port
check_tcp() {
    local service=$1
    local host=$2
    local port=$3
    
    printf "Checking %-25s ... " "$service"
    
    if timeout 2 bash -c "cat < /dev/null > /dev/tcp/$host/$port" 2>/dev/null; then
        echo -e "${GREEN}✓ OK${NC} (Port $port open)"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (Port $port not reachable)"
        return 1
    fi
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}✗ Docker is not running${NC}"
    exit 1
fi

echo "Docker Status:"
echo ""

# Check container status
echo "Container Status:"
docker-compose ps --format table
echo ""

# Initialize counters
total=0
passed=0

# Check Infrastructure Services
echo "Infrastructure Services:"
echo "------------------------"

((total++))
if check_tcp "MongoDB" "localhost" "27017"; then ((passed++)); fi

((total++))
if check_tcp "RabbitMQ (AMQP)" "localhost" "5672"; then ((passed++)); fi

((total++))
if check_http "RabbitMQ Management" "http://localhost:15672"; then ((passed++)); fi

echo ""

# Check Application Services
echo "Application Services:"
echo "---------------------"

((total++))
if check_http "API Gateway" "http://localhost:3000/health" 404; then ((passed++)); fi

((total++))
if check_http "Orchestrator" "http://localhost:3001/health" 404; then ((passed++)); fi

((total++))
if check_http "Notification Service" "http://localhost:3002" 200; then ((passed++)); fi

echo ""

# Check Mock Services
echo "Mock Services:"
echo "--------------"

((total++))
if check_tcp "CMS Mock (SOAP)" "localhost" "4000"; then ((passed++)); fi

((total++))
if check_tcp "ROS Mock (REST)" "localhost" "4001"; then ((passed++)); fi

((total++))
if check_tcp "WMS Mock (TCP)" "localhost" "4002"; then ((passed++)); fi

echo ""

# Summary
echo "=============================="
echo "Summary:"
echo "--------"
echo -e "Total checks: $total"
echo -e "Passed: ${GREEN}$passed${NC}"
echo -e "Failed: ${RED}$((total - passed))${NC}"

if [ $passed -eq $total ]; then
    echo ""
    echo -e "${GREEN}✅ All services are healthy!${NC}"
    exit 0
else
    echo ""
    echo -e "${YELLOW}⚠️  Some services are not responding${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Check logs: docker-compose logs -f"
    echo "  2. Check service status: docker-compose ps"
    echo "  3. Restart services: docker-compose restart"
    exit 1
fi
