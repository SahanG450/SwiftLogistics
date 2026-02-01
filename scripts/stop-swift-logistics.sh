#!/bin/bash
# Stop all Swift Logistics Mock Services

echo "🛑 Stopping Swift Logistics Mock Services"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Stopping CMS Mock Service...${NC}"
pkill -f "cms-mock/app.py"
echo -e "${GREEN}✓ Stopped${NC}"

echo -e "${YELLOW}Stopping WMS Mock Service...${NC}"
pkill -f "wms-mock/app.py"
echo -e "${GREEN}✓ Stopped${NC}"

echo -e "${YELLOW}Stopping ROS Mock Service...${NC}"
pkill -f "ros-mock/app.py"
echo -e "${GREEN}✓ Stopped${NC}"

echo ""
echo "=========================================="
echo -e "${GREEN}✓ All services stopped!${NC}"
