# 🔌 How MongoDB Connects Through API Endpoints in SwiftLogistics

## Complete Data Flow Diagram

```
┌─────────────────┐
│   Client/User   │ (Browser, Postman, curl)
└────────┬────────┘
         │ HTTP Request
         │ POST http://localhost:3000/api/orders
         ▼
┌─────────────────────────────────────┐
│   Python API (FastAPI)              │
│   Port: 3000                        │
│   File: services/python-api/app.py  │
│                                     │
│   @app.post("/api/orders")          │
│   async def create_order():         │
│       db = await get_database() ←───┼─── Gets MongoDB connection
│       db.orders.insert_one(data)    │
└────────┬────────────────────────────┘
         │ MongoDB Driver (Motor)
         │ Connection String:
         │ mongodb://admin:admin123@localhost:27017
         ▼
┌─────────────────────────────────────┐
│   MongoDB Container                 │
│   Port: 27017                       │
│   Container: swiftlogistics-mongodb │
│                                     │
│   Database: swiftlogistics          │
│   Collections:                      │
│   ├── orders                        │
│   ├── drivers                       │
│   ├── shipments                     │
│   └── clients                       │
└─────────────────────────────────────┘
```

## Step-by-Step: How a Request Works

### Example: Creating an Order

```python
# 1. Client sends request
POST http://localhost:3000/api/orders
Body: {
  "client_id": "CLIENT-001",
  "pickup_location": "New York",
  "delivery_location": "Boston",
  "package_details": "Laptop"
}

# 2. FastAPI receives request
@app.post("/api/orders")
async def create_order(order: Order):
    # This endpoint is now active and listening

# 3. Connect to MongoDB
    db = await get_database()
    # Connects to: mongodb://localhost:27017/swiftlogistics
    
# 4. Insert data into MongoDB
    order_data = {
        "order_id": "ORDER-000001",
        "client_id": "CLIENT-001",
        "pickup_location": "New York",
        "delivery_location": "Boston",
        "package_details": "Laptop",
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    
    result = await db.orders.insert_one(order_data)
    # Inserts into 'orders' collection in MongoDB
    
# 5. Return response to client
    return order_data  # {"order_id": "ORDER-000001", ...}
```

## MongoDB Connection Code

### File: `shared/database/mongodb.py`

```python
from motor.motor_asyncio import AsyncIOMotorClient

class MongoDBClient:
    _client = None
    _database = None
    
    @classmethod
    async def connect(cls):
        # Connection details from your docker-compose.yml
        uri = "mongodb://admin:admin123@localhost:27017/swiftlogistics?authSource=admin"
        
        # Create MongoDB client
        cls._client = AsyncIOMotorClient(uri)
        
        # Test connection
        await cls._client.admin.command('ping')
        
        # Get database
        cls._database = cls._client['swiftlogistics']
        
        return cls._database
```

## API Endpoints That Use MongoDB

### 1. CREATE Order
```bash
POST http://localhost:3000/api/orders
→ MongoDB: db.orders.insert_one({...})
→ Returns: Created order with ID
```

### 2. GET All Orders
```bash
GET http://localhost:3000/api/orders
→ MongoDB: db.orders.find({})
→ Returns: List of all orders
```

### 3. GET Single Order
```bash
GET http://localhost:3000/api/orders/ORDER-000001
→ MongoDB: db.orders.find_one({"order_id": "ORDER-000001"})
→ Returns: Single order details
```

### 4. UPDATE Order Status
```bash
PUT http://localhost:3000/api/orders/ORDER-000001/status
→ MongoDB: db.orders.update_one({"order_id": "ORDER-000001"}, {"$set": {"status": "in-transit"}})
→ Returns: Success message
```

### 5. DELETE Order
```bash
DELETE http://localhost:3000/api/orders/ORDER-000001
→ MongoDB: db.orders.delete_one({"order_id": "ORDER-000001"})
→ Returns: Deletion confirmation
```

## Port Configuration

| Service | Port | Purpose |
|---------|------|---------|
| Python API | 3000 | HTTP REST API endpoints |
| MongoDB | 27017 | Database connection |
| RabbitMQ | 5672 | Message queue |
| RabbitMQ UI | 15672 | Management interface |

## Connection String Breakdown

```
mongodb://admin:admin123@localhost:27017/swiftlogistics?authSource=admin
│         │     │         │         │      │             │
│         │     │         │         │      │             └─ Authentication database
│         │     │         │         │      └─ Database name
│         │     │         │         └─ Port number
│         │     │         └─ Hostname (localhost or mongodb)
│         │     └─ Password (from docker-compose.yml)
│         └─ Username (from docker-compose.yml)
└─ Protocol
```

## Testing the Connection

### Test 1: Check MongoDB is Running
```bash
docker ps | grep mongodb
# Should show: swiftlogistics-mongodb
```

### Test 2: Connect to MongoDB Shell
```bash
docker exec -it swiftlogistics-mongodb mongosh -u admin -p admin123 --authenticationDatabase admin
```

### Test 3: Start Python API
```bash
cd services/python-api-example
python app.py
# Output: "✅ Connected to MongoDB successfully!"
```

### Test 4: Create Order via API
```bash
curl -X POST http://localhost:3000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "CLIENT-001",
    "pickup_location": "New York",
    "delivery_location": "Boston",
    "package_details": "Laptop"
  }'
```

### Test 5: View Data in MongoDB
```bash
docker exec -it swiftlogistics-mongodb mongosh -u admin -p admin123 --authenticationDatabase admin

use swiftlogistics
db.orders.find().pretty()
```

## Environment Variables

### In `docker-compose.yml`:
```yaml
mongodb:
  environment:
    MONGO_INITDB_ROOT_USERNAME: admin
    MONGO_INITDB_ROOT_PASSWORD: admin123
    MONGO_INITDB_DATABASE: swiftlogistics
  ports:
    - "27017:27017"
```

### In Python API:
```python
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb://admin:admin123@mongodb:27017/swiftlogistics?authSource=admin"
)
```

## Collections in MongoDB

After running the API, these collections are created:

```javascript
swiftlogistics
├── orders          // Customer orders
├── drivers         // Driver information
├── shipments       // Shipment tracking
├── clients         // Client accounts
├── contracts       // Client contracts
└── invoices        // Billing information
```

## Common MongoDB Operations in API

### Insert (CREATE)
```python
await db.orders.insert_one({
    "order_id": "ORDER-001",
    "client_id": "CLIENT-001",
    "status": "pending"
})
```

### Find (READ)
```python
# Get all
orders = await db.orders.find({}).to_list(100)

# Get one
order = await db.orders.find_one({"order_id": "ORDER-001"})

# Filter
pending = await db.orders.find({"status": "pending"}).to_list(100)
```

### Update (UPDATE)
```python
await db.orders.update_one(
    {"order_id": "ORDER-001"},
    {"$set": {"status": "in-transit"}}
)
```

### Delete (DELETE)
```python
await db.orders.delete_one({"order_id": "ORDER-001"})
```

## Complete Request Flow Example

```
1. User Request
   curl POST http://localhost:3000/api/orders
   
2. FastAPI Route
   @app.post("/api/orders")
   
3. Get MongoDB Connection
   db = await get_database()
   # Connects to port 27017
   
4. Execute MongoDB Operation
   await db.orders.insert_one(order_data)
   
5. MongoDB Stores Data
   Collection: swiftlogistics.orders
   Document: {_id: ObjectId(...), order_id: "ORDER-001", ...}
   
6. Return Response
   return {"order_id": "ORDER-001", "status": "created"}
   
7. User Receives
   HTTP 201 Created
   {"order_id": "ORDER-001", ...}
```

## Summary

✅ **API Endpoint** (Port 3000) - Where you send HTTP requests  
✅ **MongoDB Database** (Port 27017) - Where data is stored  
✅ **Connection** - API connects to MongoDB using Motor driver  
✅ **Collections** - Like tables in SQL (orders, drivers, etc.)  
✅ **Documents** - Like rows in SQL (individual records)  

The API is the **interface** that allows you to interact with MongoDB through **HTTP requests** instead of using MongoDB commands directly!
