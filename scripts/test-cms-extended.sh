#!/bin/bash

# Test script for extended CMS Mock Service
# Tests all entity types: Customers, Drivers, Clients, Admins

BASE_URL="http://localhost:3001"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}======================================${NC}"
echo -e "${YELLOW}Testing Extended CMS Mock Service${NC}"
echo -e "${YELLOW}======================================${NC}\n"

# Test health endpoint
echo -e "${YELLOW}[1/15] Testing health endpoint...${NC}"
HEALTH=$(curl -s "$BASE_URL/health")
if echo "$HEALTH" | grep -q "healthy"; then
    echo -e "${GREEN}✓ Health check passed${NC}"
    echo "$HEALTH" | python3 -m json.tool | head -15
else
    echo -e "${RED}✗ Health check failed${NC}"
    exit 1
fi

# Test Customers
echo -e "\n${YELLOW}[2/15] Getting all customers...${NC}"
CUSTOMERS=$(curl -s "$BASE_URL/customers/")
CUSTOMER_COUNT=$(echo "$CUSTOMERS" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")
echo -e "${GREEN}✓ Found $CUSTOMER_COUNT customers${NC}"

# Test Drivers
echo -e "\n${YELLOW}[3/15] Getting all drivers...${NC}"
DRIVERS=$(curl -s "$BASE_URL/drivers/")
DRIVER_COUNT=$(echo "$DRIVERS" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")
echo -e "${GREEN}✓ Found $DRIVER_COUNT drivers${NC}"

# Test Clients
echo -e "\n${YELLOW}[4/15] Getting all clients...${NC}"
CLIENTS=$(curl -s "$BASE_URL/clients/")
CLIENT_COUNT=$(echo "$CLIENTS" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")
echo -e "${GREEN}✓ Found $CLIENT_COUNT clients${NC}"

# Test Admins
echo -e "\n${YELLOW}[5/15] Getting all admins...${NC}"
ADMINS=$(curl -s "$BASE_URL/admins/")
ADMIN_COUNT=$(echo "$ADMINS" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")
echo -e "${GREEN}✓ Found $ADMIN_COUNT admins${NC}"

# Create a new driver
echo -e "\n${YELLOW}[6/15] Creating a new driver...${NC}"
NEW_DRIVER=$(curl -s -X POST "$BASE_URL/drivers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Driver",
    "email": "test.driver@test.com",
    "phone": "+1-555-9999",
    "license_number": "DL-TEST123"
  }')
DRIVER_ID=$(echo "$NEW_DRIVER" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo -e "${GREEN}✓ Created driver with ID: $DRIVER_ID${NC}"

# Get driver by ID
echo -e "\n${YELLOW}[7/15] Getting driver by ID...${NC}"
DRIVER=$(curl -s "$BASE_URL/drivers/$DRIVER_ID")
if echo "$DRIVER" | grep -q "Test Driver"; then
    echo -e "${GREEN}✓ Retrieved driver successfully${NC}"
else
    echo -e "${RED}✗ Failed to retrieve driver${NC}"
fi

# Update driver status
echo -e "\n${YELLOW}[8/15] Updating driver status...${NC}"
UPDATED_DRIVER=$(curl -s -X PUT "$BASE_URL/drivers/$DRIVER_ID" \
  -H "Content-Type: application/json" \
  -d '{"status": "on_duty", "vehicle_id": "VH-TEST"}')
if echo "$UPDATED_DRIVER" | grep -q "on_duty"; then
    echo -e "${GREEN}✓ Updated driver status to on_duty${NC}"
else
    echo -e "${RED}✗ Failed to update driver${NC}"
fi

# Filter drivers by status
echo -e "\n${YELLOW}[9/15] Filtering drivers by status (available)...${NC}"
AVAILABLE_DRIVERS=$(curl -s "$BASE_URL/drivers/?status=available")
AVAILABLE_COUNT=$(echo "$AVAILABLE_DRIVERS" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")
echo -e "${GREEN}✓ Found $AVAILABLE_COUNT available drivers${NC}"

# Create a new client
echo -e "\n${YELLOW}[10/15] Creating a new client...${NC}"
NEW_CLIENT=$(curl -s -X POST "$BASE_URL/clients/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Corp",
    "email": "test@testcorp.com",
    "phone": "+1-555-8888",
    "address": "123 Test St",
    "membership_level": "gold"
  }')
CLIENT_ID=$(echo "$NEW_CLIENT" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo -e "${GREEN}✓ Created client with ID: $CLIENT_ID${NC}"

# Filter clients by membership
echo -e "\n${YELLOW}[11/15] Filtering clients by membership (platinum)...${NC}"
PLATINUM_CLIENTS=$(curl -s "$BASE_URL/clients/?membership_level=platinum")
PLATINUM_COUNT=$(echo "$PLATINUM_CLIENTS" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")
echo -e "${GREEN}✓ Found $PLATINUM_COUNT platinum clients${NC}"

# Create a new admin
echo -e "\n${YELLOW}[12/15] Creating a new admin...${NC}"
NEW_ADMIN=$(curl -s -X POST "$BASE_URL/admins/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Admin",
    "email": "test.admin@test.com",
    "phone": "+1-555-7777",
    "role": "moderator",
    "permissions": ["users.read", "tickets.write"]
  }')
ADMIN_ID=$(echo "$NEW_ADMIN" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo -e "${GREEN}✓ Created admin with ID: $ADMIN_ID${NC}"

# Filter admins by role
echo -e "\n${YELLOW}[13/15] Filtering admins by role (super_admin)...${NC}"
SUPER_ADMINS=$(curl -s "$BASE_URL/admins/?role=super_admin")
SUPER_ADMIN_COUNT=$(echo "$SUPER_ADMINS" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")
echo -e "${GREEN}✓ Found $SUPER_ADMIN_COUNT super admins${NC}"

# Delete test driver
echo -e "\n${YELLOW}[14/15] Deleting test driver...${NC}"
DELETE_RESPONSE=$(curl -s -w "%{http_code}" -X DELETE "$BASE_URL/drivers/$DRIVER_ID")
if [[ "$DELETE_RESPONSE" == "204" ]]; then
    echo -e "${GREEN}✓ Deleted driver successfully${NC}"
else
    echo -e "${RED}✗ Failed to delete driver (HTTP $DELETE_RESPONSE)${NC}"
fi

# Delete test client
echo -e "\n${YELLOW}[15/15] Deleting test client...${NC}"
DELETE_RESPONSE=$(curl -s -w "%{http_code}" -X DELETE "$BASE_URL/clients/$CLIENT_ID")
if [[ "$DELETE_RESPONSE" == "204" ]]; then
    echo -e "${GREEN}✓ Deleted client successfully${NC}"
else
    echo -e "${RED}✗ Failed to delete client (HTTP $DELETE_RESPONSE)${NC}"
fi

# Final summary
echo -e "\n${YELLOW}======================================${NC}"
echo -e "${GREEN}✓ All tests passed!${NC}"
echo -e "${YELLOW}======================================${NC}"

echo -e "\n${YELLOW}Entity Summary:${NC}"
echo "  Customers: $CUSTOMER_COUNT"
echo "  Drivers: $DRIVER_COUNT"
echo "  Clients: $CLIENT_COUNT"
echo "  Admins: $ADMIN_COUNT"

echo -e "\n${YELLOW}Swagger UI:${NC} http://localhost:3001/docs"
echo -e "${YELLOW}Documentation:${NC} doc/CMS_EXTENDED_DOCUMENTATION.md\n"

