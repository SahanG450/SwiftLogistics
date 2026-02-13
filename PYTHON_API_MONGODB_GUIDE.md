# Python API with MongoDB - Quick Start Guide

## 🚀 How MongoDB is Accessed Through API Endpoints

```
Client Request → API Endpoint (Port 3000) → MongoDB (Port 27017) → Response
```

## 📋 Setup & Run

### Option 1: Run Standalone (Without Docker)

```bash
# Install dependencies
cd services/python-api-example
pip install -r requirements.txt

# Set environment variable for MongoDB
export MONGODB_URI="mongodb://admin:admin123@localhost:27017/swiftlogistics?authSource=admin"

# Run the API
python app.py
```

### Option 2: Test with Existing MongoDB Container

```bash
# Make sure MongoDB container is running
docker ps | grep mongodb

# Run the API (it will connect to your existing MongoDB)
cd services/python-api-example
python app.py
```

## 🔌 API Endpoints - How to Use

### 1️⃣ **Create Order** (POST)
```bash
curl -X POST http://localhost:3000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "CLIENT-001",
    "pickup_location": "123 Main St, New York",
    "delivery_location": "456 Oak Ave, Boston",
    "package_details": "Electronics - Handle with care"
  }'
```

**What happens:**
1. Request hits `/api/orders` endpoint
2. Python code connects to MongoDB (port 27017)
3. Inserts data into `orders` collection
4. Returns created order with ID

### 2️⃣ **Get All Orders** (GET)
```bash
# Get all orders
curl http://localhost:3000/api/orders

# Filter by status
curl http://localhost:3000/api/orders?status=pending

# Limit results
curl http://localhost:3000/api/orders?limit=10
```

### 3️⃣ **Get Single Order** (GET)
```bash
curl http://localhost:3000/api/orders/ORDER-000001
```

### 4️⃣ **Update Order Status** (PUT)
```bash
curl -X PUT http://localhost:3000/api/orders/ORDER-000001/status \
  -H "Content-Type: application/json" \
  -d '{"status": "in-transit"}'
```

### 5️⃣ **Delete Order** (DELETE)
```bash
curl -X DELETE http://localhost:3000/api/orders/ORDER-000001
```

### 6️⃣ **Create Driver** (POST)
```bash
curl -X POST http://localhost:3000/api/drivers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "license_number": "DL123456"
  }'
```

### 7️⃣ **Get All Drivers** (GET)
```bash
# All drivers
curl http://localhost:3000/api/drivers

# Available drivers only
curl http://localhost:3000/api/drivers?status=available
```

### 8️⃣ **Create Shipment** (POST)
```bash
curl -X POST http://localhost:3000/api/shipments \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "ORDER-000001",
    "driver_id": "DRV-0001",
    "vehicle_id": "VEH-001"
  }'
```

### 9️⃣ **Get Statistics** (GET)
```bash
curl http://localhost:3000/api/stats
```

### 🔟 **Health Check** (GET)
```bash
curl http://localhost:3000/health
```

## 🔍 View Data in MongoDB

### Method 1: MongoDB Shell
```bash
# Connect to MongoDB
docker exec -it swiftlogistics-mongodb mongosh -u admin -p admin123 --authenticationDatabase admin

# Use database
use swiftlogistics

# View orders
db.orders.find().pretty()

# View drivers
db.drivers.find().pretty()

# View shipments
db.shipments.find().pretty()

# Count documents
db.orders.countDocuments()
```

### Method 2: VS Code MongoDB Extension
1. Click MongoDB icon in sidebar
2. Connect to: `mongodb://admin:admin123@localhost:27017/?authSource=admin`
3. Browse `swiftlogistics` database
4. View collections: orders, drivers, shipments

## 📊 How Data Flows

```
1. Client sends HTTP Request
   ↓
2. FastAPI receives request at endpoint (e.g., /api/orders)
   ↓
3. Python code calls: db = await get_database()
   ↓
4. MongoDBClient connects to mongodb://localhost:27017
   ↓
5. Execute query: db.orders.insert_one(data)
   ↓
6. MongoDB stores data in 'orders' collection
   ↓
7. Python returns response to client
```

## 🧪 Complete Test Flow

```bash
# 1. Start MongoDB (if not running)
docker start swiftlogistics-mongodb

# 2. Run the Python API
python app.py

# 3. Create an order
curl -X POST http://localhost:3000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "CLIENT-001",
    "pickup_location": "New York",
    "delivery_location": "Boston",
    "package_details": "Laptop"
  }'

# 4. Get all orders
curl http://localhost:3000/api/orders

# 5. Check MongoDB directly
docker exec -it swiftlogistics-mongodb mongosh -u admin -p admin123 --authenticationDatabase admin

# In MongoDB shell:
use swiftlogistics
db.orders.find().pretty()
```

## 🔧 Configuration Details

### MongoDB Connection (in code)
```python
# From shared/database/mongodb.py
mongodb_uri = "mongodb://admin:admin123@mongodb:27017/swiftlogistics?authSource=admin"

# Breakdown:
# - Protocol: mongodb://
# - Username: admin
# - Password: admin123
# - Host: mongodb (or localhost)
# - Port: 27017
# - Database: swiftlogistics
# - Auth Database: admin
```

### Environment Variables
```bash
MONGODB_URI=mongodb://admin:admin123@localhost:27017/swiftlogistics?authSource=admin
PORT=3000
```

## 📝 Code Explanation

### How Endpoints Connect to MongoDB

```python
@app.post("/api/orders")
async def create_order(order: Order):
    # Step 1: Get MongoDB database connection
    db = await get_database()
    
    # Step 2: Prepare data
    order_data = order.dict()
    order_data["order_id"] = "ORDER-000001"
    
    # Step 3: Insert into MongoDB collection
    result = await db.orders.insert_one(order_data)
    
    # Step 4: Return response
    return order_data
```

### MongoDB Collections Used
- `orders` - Store order information
- `drivers` - Store driver profiles
- `shipments` - Store shipment tracking
- `clients` - Store client information

## 🎯 Key Points

1. **Port 3000**: API endpoint (where you send requests)
2. **Port 27017**: MongoDB database (where data is stored)
3. **Connection**: API connects to MongoDB using Motor (async driver)
4. **Collections**: Similar to tables in SQL databases
5. **Documents**: Similar to rows in SQL databases

## 🐛 Troubleshooting

### MongoDB Connection Error
```bash
# Check if MongoDB is running
docker ps | grep mongodb

# If not running, start it
docker start swiftlogistics-mongodb

# Check logs
docker logs swiftlogistics-mongodb
```

### API Not Starting
```bash
# Check if port 3000 is available
lsof -i :3000

# Install dependencies
pip install -r requirements.txt
```

### Test Connection
```bash
# Test MongoDB connection
docker exec swiftlogistics-mongodb mongosh --eval "db.adminCommand('ping')"
```
