#!/bin/bash

# Test script for WMS Mock Service

set -e

echo "========================================="
echo "Testing WMS Mock Service"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Service details
SERVICE_NAME="WMS Mock"
SERVICE_URL="http://localhost:3003"
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
echo "3. Test Warehouse Endpoints"
echo "--------------------------------"

# Test GET /warehouses
warehouses_response=$(curl -s -o /dev/null -w "%{http_code}" $SERVICE_URL/warehouses 2>/dev/null || echo "000")
if [ "$warehouses_response" = "200" ]; then
    echo -e "${GREEN}✓ GET /warehouses works (HTTP $warehouses_response)${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ GET /warehouses failed (HTTP $warehouses_response)${NC}"
    ((FAILED++))
fi

# Test GET /inventory
inventory_response=$(curl -s -o /dev/null -w "%{http_code}" $SERVICE_URL/inventory 2>/dev/null || echo "000")
if [ "$inventory_response" = "200" ]; then
    echo -e "${GREEN}✓ GET /inventory works (HTTP $inventory_response)${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ GET /inventory failed (HTTP $inventory_response)${NC}"
    ((FAILED++))
fi

# Test POST /inventory/check
echo ""
echo "Testing inventory check..."
check_response=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST $SERVICE_URL/inventory/check \
    -H "Content-Type: application/json" \
    -d '{"items":[{"sku":"TEST001","quantity":10}]}' \
    2>/dev/null || echo "000")

if [ "$check_response" = "200" ] || [ "$check_response" = "201" ]; then
    echo -e "${GREEN}✓ POST /inventory/check works (HTTP $check_response)${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ POST /inventory/check failed (HTTP $check_response)${NC}"
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
