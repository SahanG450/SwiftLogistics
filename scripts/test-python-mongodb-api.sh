#!/bin/bash

# Test Python API with MongoDB
echo "🧪 Testing SwiftLogistics Python API with MongoDB"
echo "=================================================="
echo ""

# Check if MongoDB is running
echo "1️⃣  Checking MongoDB status..."
docker ps | grep mongodb
if [ $? -eq 0 ]; then
    echo "✅ MongoDB is running"
else
    echo "❌ MongoDB is not running. Start with: docker start swiftlogistics-mongodb"
    exit 1
fi

echo ""
echo "2️⃣  Testing MongoDB connection..."
docker exec swiftlogistics-mongodb mongosh --eval "db.adminCommand('ping')" -u admin -p admin123 --authenticationDatabase admin

echo ""
echo "3️⃣  Creating test order via API..."
curl -X POST http://localhost:3000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "CLIENT-TEST-001",
    "pickup_location": "123 Test Street, New York",
    "delivery_location": "456 Demo Avenue, Boston",
    "package_details": "Test Package - Electronics"
  }'

echo ""
echo ""
echo "4️⃣  Getting all orders..."
curl http://localhost:3000/api/orders

echo ""
echo ""
echo "5️⃣  Viewing data directly in MongoDB..."
docker exec swiftlogistics-mongodb mongosh -u admin -p admin123 --authenticationDatabase admin --eval "
use swiftlogistics
print('Orders in database:')
db.orders.find().forEach(printjson)
"

echo ""
echo "✅ Test complete!"
