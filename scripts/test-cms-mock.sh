#!/bin/bash

# Test script for CMS Mock Service

set -e

echo "========================================="
echo "Testing CMS Mock Service"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Service details
SERVICE_NAME="CMS Mock"
SERVICE_URL="http://localhost:3001"
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
echo "3. Test Customer Endpoints"
echo "--------------------------------"

# Test GET /customers
customers_response=$(curl -s -o /dev/null -w "%{http_code}" $SERVICE_URL/customers 2>/dev/null || echo "000")
if [ "$customers_response" = "200" ]; then
    echo -e "${GREEN}✓ GET /customers works (HTTP $customers_response)${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ GET /customers failed (HTTP $customers_response)${NC}"
    ((FAILED++))
fi

# Test POST /customers
echo ""
echo "Creating test customer..."
create_response=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST $SERVICE_URL/customers \
    -H "Content-Type: application/json" \
    -d '{"name":"Test Customer","email":"test@example.com","phone":"+94771234567","address":"123 Test St, Colombo"}' \
    2>/dev/null || echo "000")

if [ "$create_response" = "200" ] || [ "$create_response" = "201" ]; then
    echo -e "${GREEN}✓ POST /customers works (HTTP $create_response)${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ POST /customers failed (HTTP $create_response)${NC}"
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
