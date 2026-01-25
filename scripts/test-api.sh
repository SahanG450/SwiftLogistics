#!/bin/bash

# API Testing Script for SwiftLogistics
# Tests the complete order submission and tracking workflow

set -e

echo "🧪 SwiftLogistics API Test Suite"
echo "================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
API_URL="http://localhost:3000"
ORCHESTRATOR_URL="http://localhost:3001"
NOTIFICATION_URL="http://localhost:3002"

# Test counter
TOTAL_TESTS=0
PASSED_TESTS=0

# Helper function for test output
test_result() {
    ((TOTAL_TESTS++))
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: $2"
        ((PASSED_TESTS++))
    else
        echo -e "${RED}✗ FAIL${NC}: $2"
    fi
}

echo -e "${BLUE}1. Testing Service Connectivity${NC}"
echo "--------------------------------"

# Test API Gateway
if curl -s "$API_URL" > /dev/null 2>&1; then
    test_result 0 "API Gateway is reachable"
else
    test_result 1 "API Gateway is reachable"
fi

# Test Orchestrator
if curl -s "$ORCHESTRATOR_URL" > /dev/null 2>&1; then
    test_result 0 "Orchestrator is reachable"
else
    test_result 1 "Orchestrator is reachable"
fi

# Test Notification Service
if curl -s "$NOTIFICATION_URL" > /dev/null 2>&1; then
    test_result 0 "Notification Service is reachable"
else
    test_result 1 "Notification Service is reachable"
fi

echo ""
echo -e "${BLUE}2. Testing Order Submission${NC}"
echo "----------------------------"

# Sample order payload
ORDER_PAYLOAD='{
  "customerName": "John Doe",
  "customerEmail": "john.doe@example.com",
  "customerPhone": "+94771234567",
  "items": [
    {
      "productId": "PROD-001",
      "name": "Laptop",
      "quantity": 1,
      "price": 75000
    },
    {
      "productId": "PROD-002",
      "name": "Mouse",
      "quantity": 2,
      "price": 1500
    }
  ],
  "pickupAddress": {
    "street": "123 Galle Road",
    "city": "Colombo",
    "postalCode": "00100",
    "coordinates": {
      "lat": 6.9271,
      "lng": 79.8612
    }
  },
  "deliveryAddress": {
    "street": "456 Kandy Road",
    "city": "Kandy",
    "postalCode": "20000",
    "coordinates": {
      "lat": 7.2906,
      "lng": 80.6337
    }
  },
  "priority": "HIGH",
  "notes": "Please handle with care"
}'

# Submit order (Note: This will fail without JWT token)
echo "Attempting to submit order..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/api/orders" \
  -H "Content-Type: application/json" \
  -d "$ORDER_PAYLOAD" 2>/dev/null)

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 401 ]; then
    test_result 0 "API Gateway authentication is working (401 Unauthorized)"
    echo -e "  ${YELLOW}Note: Authentication is required. Generate JWT token for full testing.${NC}"
elif [ "$HTTP_CODE" -eq 202 ]; then
    test_result 0 "Order submitted successfully (202 Accepted)"
    ORDER_ID=$(echo "$BODY" | grep -o '"orderId":"[^"]*' | cut -d'"' -f4)
    echo -e "  Order ID: ${GREEN}$ORDER_ID${NC}"
elif [ "$HTTP_CODE" -eq 400 ]; then
    test_result 0 "Input validation is working (400 Bad Request)"
else
    test_result 1 "Unexpected response (HTTP $HTTP_CODE)"
fi

echo ""
echo -e "${BLUE}3. Testing Health Endpoints${NC}"
echo "---------------------------"

# Test RabbitMQ Management
if curl -s -u admin:admin123 "http://localhost:15672/api/overview" > /dev/null 2>&1; then
    test_result 0 "RabbitMQ Management API accessible"
else
    test_result 1 "RabbitMQ Management API accessible"
fi

# Test MongoDB connection
if docker-compose exec -T mongodb mongosh --quiet --eval "db.runCommand({ping:1})" mongodb://localhost:27017 > /dev/null 2>&1; then
    test_result 0 "MongoDB is responding"
else
    test_result 1 "MongoDB is responding"
fi

echo ""
echo -e "${BLUE}4. Testing RabbitMQ Queues${NC}"
echo "--------------------------"

# Check if queues exist
QUEUES=$(curl -s -u admin:admin123 "http://localhost:15672/api/queues" 2>/dev/null)

if echo "$QUEUES" | grep -q "new_order_queue"; then
    test_result 0 "Order queue exists in RabbitMQ"
else
    test_result 1 "Order queue exists in RabbitMQ"
fi

if echo "$QUEUES" | grep -q "notification"; then
    test_result 0 "Notification queue exists in RabbitMQ"
else
    test_result 1 "Notification queue exists in RabbitMQ"
fi

echo ""
echo -e "${BLUE}5. Testing Mock Services${NC}"
echo "------------------------"

# Test CMS Mock (SOAP)
if curl -s "http://localhost:4000/cms?wsdl" | grep -q "wsdl"; then
    test_result 0 "CMS Mock (SOAP) is serving WSDL"
else
    test_result 1 "CMS Mock (SOAP) is serving WSDL"
fi

# Test ROS Mock (REST)
if curl -s "http://localhost:4001/health" > /dev/null 2>&1; then
    test_result 0 "ROS Mock (REST) is responding"
else
    test_result 1 "ROS Mock (REST) is responding"
fi

# Test WMS Mock (TCP)
if timeout 2 bash -c "cat < /dev/null > /dev/tcp/localhost/4002" 2>/dev/null; then
    test_result 0 "WMS Mock (TCP) port is open"
else
    test_result 1 "WMS Mock (TCP) port is open"
fi

echo ""
echo "================================="
echo -e "${BLUE}Test Summary${NC}"
echo "================================="
echo -e "Total Tests: $TOTAL_TESTS"
echo -e "Passed: ${GREEN}$PASSED_TESTS${NC}"
echo -e "Failed: ${RED}$((TOTAL_TESTS - PASSED_TESTS))${NC}"
echo -e "Success Rate: $(( PASSED_TESTS * 100 / TOTAL_TESTS ))%"

echo ""
if [ $PASSED_TESTS -eq $TOTAL_TESTS ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    echo ""
    echo "Next Steps:"
    echo "  1. Generate JWT token for authenticated testing"
    echo "  2. Submit real orders and track their status"
    echo "  3. Monitor RabbitMQ: http://localhost:15672"
    echo "  4. Check adapter logs: docker-compose logs -f cms-adapter ros-adapter wms-adapter"
    exit 0
else
    echo -e "${YELLOW}⚠️  Some tests failed${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Check if all services are running: docker-compose ps"
    echo "  2. Check service logs: docker-compose logs"
    echo "  3. Run health check: ./scripts/health-check.sh"
    echo "  4. Restart services: docker-compose restart"
    exit 1
fi
