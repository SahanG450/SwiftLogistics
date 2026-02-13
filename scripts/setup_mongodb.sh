#!/bin/bash
# MongoDB Setup and Test Script for SwiftLogistics

set -e  # Exit on error

echo "======================================"
echo "SwiftLogistics MongoDB Setup"
echo "======================================"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is running
echo "1. Checking Docker..."
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}✗ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker is running${NC}"
echo ""

# Check if .env file exists
echo "2. Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}! .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env file${NC}"
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi
echo ""

# Start MongoDB
echo "3. Starting MongoDB..."
docker-compose up -d mongodb
echo -e "${GREEN}✓ MongoDB container started${NC}"
echo ""

# Wait for MongoDB to be ready
echo "4. Waiting for MongoDB to be ready..."
for i in {1..30}; do
    if docker exec swiftlogistics-mongodb mongosh --eval "db.adminCommand('ping')" --quiet > /dev/null 2>&1; then
        echo -e "${GREEN}✓ MongoDB is ready${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}✗ MongoDB failed to start after 30 seconds${NC}"
        exit 1
    fi
    echo "   Waiting... ($i/30)"
    sleep 1
done
echo ""

# Install Python dependencies
echo "5. Installing Python dependencies..."
cd shared/database
if [ ! -d "venv" ]; then
    echo "   Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Run MongoDB test
echo "6. Running MongoDB connection test..."
echo "======================================"
python test_mongodb.py
TEST_RESULT=$?
echo "======================================"
echo ""

if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo ""
    echo "======================================"
    echo "MongoDB is ready to use!"
    echo "======================================"
    echo ""
    echo "Connection Details:"
    echo "  Host: localhost"
    echo "  Port: 27017"
    echo "  Database: swiftlogistics"
    echo "  Username: admin"
    echo "  Password: admin123"
    echo ""
    echo "MongoDB URI:"
    echo "  mongodb://admin:admin123@localhost:27017/swiftlogistics?authSource=admin"
    echo ""
    echo "Management UI (Compass):"
    echo "  Use MongoDB Compass to connect with the URI above"
    echo ""
    echo "Next Steps:"
    echo "  1. Review MONGODB_INTEGRATION.md for usage examples"
    echo "  2. Check example_service.py for a complete service example"
    echo "  3. Integrate MongoDB into your services"
    echo ""
else
    echo -e "${RED}✗ Some tests failed. Please check the output above.${NC}"
    exit 1
fi
