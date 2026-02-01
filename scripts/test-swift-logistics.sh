#!/bin/bash
# Test script for Swift Logistics Mock Services

echo "🚀 Testing Swift Logistics Mock Services"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test CMS Service
echo -e "${YELLOW}Testing CMS Mock Service (Port 3001)${NC}"
echo "-------------------------------------------"

echo -n "Health check: "
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3001/health 2>/dev/null)
if [ "$response" = "200" ]; then
    echo -e "${GREEN}✓ Healthy${NC}"
    curl -s http://localhost:3001/health | jq -r '.entity_counts | to_entries[] | "\(.key): \(.value)"'
else
    echo -e "${RED}✗ Failed (HTTP $response)${NC}"
fi

echo -n "Orders endpoint: "
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3001/api/orders/ 2>/dev/null)
if [ "$response" = "200" ]; then
    echo -e "${GREEN}✓ Working${NC}"
else
    echo -e "${RED}✗ Failed (HTTP $response)${NC}"
fi

echo -n "Contracts endpoint: "
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3001/api/contracts/ 2>/dev/null)
if [ "$response" = "200" ]; then
    echo -e "${GREEN}✓ Working${NC}"
else
    echo -e "${RED}✗ Failed (HTTP $response)${NC}"
fi

echo -n "Billing endpoint: "
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3001/api/billing/ 2>/dev/null)
if [ "$response" = "200" ]; then
    echo -e "${GREEN}✓ Working${NC}"
else
    echo -e "${RED}✗ Failed (HTTP $response)${NC}"
fi

echo ""

# Test WMS Service
echo -e "${YELLOW}Testing WMS Mock Service (Port 3002)${NC}"
echo "-------------------------------------------"

echo -n "Health check: "
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3002/health 2>/dev/null)
if [ "$response" = "200" ]; then
    echo -e "${GREEN}✓ Healthy${NC}"
    curl -s http://localhost:3002/health | jq -r '.package_count // "N/A" | "Packages: \(.)"'
else
    echo -e "${RED}✗ Failed (HTTP $response)${NC}"
fi

echo -n "Packages endpoint: "
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3002/api/packages/ 2>/dev/null)
if [ "$response" = "200" ]; then
    echo -e "${GREEN}✓ Working${NC}"
else
    echo -e "${RED}✗ Failed (HTTP $response)${NC}"
fi

echo ""

# Test ROS Service
echo -e "${YELLOW}Testing ROS Mock Service (Port 3003)${NC}"
echo "-------------------------------------------"

echo -n "Health check: "
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3003/health 2>/dev/null)
if [ "$response" = "200" ]; then
    echo -e "${GREEN}✓ Healthy${NC}"
    curl -s http://localhost:3003/health | jq -r '.manifest_count // "N/A" | "Manifests: \(.)"'
else
    echo -e "${RED}✗ Failed (HTTP $response)${NC}"
fi

echo -n "Manifests endpoint: "
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3003/api/manifests/ 2>/dev/null)
if [ "$response" = "200" ]; then
    echo -e "${GREEN}✓ Working${NC}"
else
    echo -e "${RED}✗ Failed (HTTP $response)${NC}"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✓ All tests completed!${NC}"
echo ""
echo "📚 API Documentation:"
echo "  CMS: http://localhost:3001/docs"
echo "  WMS: http://localhost:3002/docs"
echo "  ROS: http://localhost:3003/docs"
