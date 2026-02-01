#!/bin/bash

# Test script for ROS Mock Service

set -e

echo "========================================="
echo "Testing ROS Mock Service"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Service details
SERVICE_NAME="ROS Mock"
SERVICE_URL="http://localhost:8002"
HEALTH_ENDPOINT="$SERVICE_URL/health"

# Test counters
PASSED=0
FAILED=0

echo "1. Health Check"
echo "--------------------------------"
response=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_ENDPOINT 2>/dev/null || echo "000")
if [ "$response" = "200" ]; then
    echo -e "${GREEN}✓ Health check passed (HTTP $response)${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ Health check failed (HTTP $response)${NC}"
    ((FAILED++))
fi

echo ""
echo "2. API Documentation"
echo "--------------------------------"
docs_response=$(curl -s -o /dev/null -w "%{http_code}" $SERVICE_URL/docs 2>/dev/null || echo "000")
if [ "$docs_response" = "200" ]; then
    echo -e "${GREEN}✓ API docs accessible (HTTP $docs_response)${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ API docs not accessible (HTTP $docs_response)${NC}"
    ((FAILED++))
fi

echo ""
echo "3. Test Route Endpoints"
echo "--------------------------------"

# Test GET /routes
routes_response=$(curl -s -o /dev/null -w "%{http_code}" $SERVICE_URL/routes 2>/dev/null || echo "000")
if [ "$routes_response" = "200" ]; then
    echo -e "${GREEN}✓ GET /routes works (HTTP $routes_response)${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ GET /routes failed (HTTP $routes_response)${NC}"
    ((FAILED++))
fi

# Test POST /routes/optimize
echo ""
echo "Testing route optimization..."
optimize_response=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST $SERVICE_URL/routes/optimize \
    -H "Content-Type: application/json" \
    -d '{"origin":"Colombo","destination":"Kandy","waypoints":["Kegalle"]}' \
    2>/dev/null || echo "000")

if [ "$optimize_response" = "200" ] || [ "$optimize_response" = "201" ]; then
    echo -e "${GREEN}✓ POST /routes/optimize works (HTTP $optimize_response)${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ POST /routes/optimize failed (HTTP $optimize_response)${NC}"
    ((FAILED++))
fi

echo ""
echo "========================================="
echo "Test Results for $SERVICE_NAME"
echo "========================================="
echo "Total tests: $((PASSED + FAILED))"
echo -e "${GREEN}Passed: $PASSED${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED${NC}"
else
    echo -e "${GREEN}Failed: $FAILED${NC}"
fi
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed!${NC}"
    exit 1
fi
