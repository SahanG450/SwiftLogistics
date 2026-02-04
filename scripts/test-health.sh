#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

check_url() {
    url=$1
    name=$2
    code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 2 "$url")
    if [ "$code" == "200" ] || [ "$code" == "404" ] || [ "$code" == "401" ]; then
        # 404/401 means service is up but maybe path is wrong/auth needed, still "ALIVE"
        echo -e "${GREEN}✓ $name is UP ($code)${NC}"
    else
        echo -e "${RED}✗ $name is DOWN ($code)${NC}"
    fi
}

echo "🏥 Running System Health Checks..."
echo "================================="

check_url "http://localhost:3000/health" "API Gateway"
check_url "http://localhost:3001/health" "Orchestrator"
check_url "http://localhost:3002/health" "Notification Service"
check_url "http://localhost:15672" "RabbitMQ Admin"

echo ""
echo "🐳 Docker Container Status:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "swift|mock"
