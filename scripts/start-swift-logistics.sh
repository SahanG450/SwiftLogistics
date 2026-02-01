#!/bin/bash
# Start all Swift Logistics Mock Services

echo "🚀 Starting Swift Logistics Mock Services"
echo "=========================================="
echo ""

BASE_DIR="/home/snake/UCSC/UCSC/Year 2/sem 2/Middleware Architecture SCS2314/Assignment 4/SwiftLogistics"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Stop any existing services
echo "Stopping existing services..."
pkill -f "cms-mock/app.py" 2>/dev/null
pkill -f "wms-mock/app.py" 2>/dev/null
pkill -f "ros-mock/app.py" 2>/dev/null
sleep 2

# Start CMS Mock Service
echo -e "${YELLOW}Starting CMS Mock Service (Port 3001)...${NC}"
cd "$BASE_DIR/services/mocks/cms-mock"
nohup python app.py > /tmp/cms-mock.log 2>&1 &
CMS_PID=$!
echo -e "${GREEN}✓ Started (PID: $CMS_PID)${NC}"

# Start WMS Mock Service
echo -e "${YELLOW}Starting WMS Mock Service (Port 3002)...${NC}"
cd "$BASE_DIR/services/mocks/wms-mock"
nohup python app.py > /tmp/wms-mock.log 2>&1 &
WMS_PID=$!
echo -e "${GREEN}✓ Started (PID: $WMS_PID)${NC}"

# Start ROS Mock Service
echo -e "${YELLOW}Starting ROS Mock Service (Port 3003)...${NC}"
cd "$BASE_DIR/services/mocks/ros-mock"
nohup python app.py > /tmp/ros-mock.log 2>&1 &
ROS_PID=$!
echo -e "${GREEN}✓ Started (PID: $ROS_PID)${NC}"

echo ""
echo "Waiting for services to start..."
sleep 5

echo ""
echo "=========================================="
echo -e "${GREEN}✓ All services started!${NC}"
echo ""
echo "📋 Service Status:"
echo "  CMS Mock: http://localhost:3001 (PID: $CMS_PID)"
echo "  WMS Mock: http://localhost:3002 (PID: $WMS_PID)"
echo "  ROS Mock: http://localhost:3003 (PID: $ROS_PID)"
echo ""
echo "📚 API Documentation:"
echo "  CMS: http://localhost:3001/docs"
echo "  WMS: http://localhost:3002/docs"
echo "  ROS: http://localhost:3003/docs"
echo ""
echo "📊 Health Checks:"
echo "  curl http://localhost:3001/health"
echo "  curl http://localhost:3002/health"
echo "  curl http://localhost:3003/health"
echo ""
echo "🛑 To stop services:"
echo "  ./scripts/stop-swift-logistics.sh"
echo ""
echo "📝 Logs available at:"
echo "  /tmp/cms-mock.log"
echo "  /tmp/wms-mock.log"
echo "  /tmp/ros-mock.log"
