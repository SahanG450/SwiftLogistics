# MongoDB Integration for SwiftLogistics

This guide explains how to connect and use MongoDB in your Python-based SwiftLogistics microservices.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [Basic Usage](#basic-usage)
- [Repository Pattern](#repository-pattern)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

The MongoDB integration provides:

- **Async/await support** using Motor (async MongoDB driver)
- **Connection pooling** for optimal performance
- **Repository pattern** for clean data access
- **Automatic indexing** for collections
- **Type-safe operations** with Pydantic models

## Installation

### 1. Install MongoDB Dependencies

Add to your service's `requirements.txt`:

```txt
motor==3.3.2
pymongo==4.6.1
```

Or install directly:

```bash
pip install motor==3.3.2 pymongo==4.6.1
```

### 2. Update Docker Compose

MongoDB is already configured in `docker-compose.yml`:

```yaml
mongodb:
  image: mongo:7.0
  container_name: swiftlogistics-mongodb
  ports:
    - "27017:27017"
  environment:
    MONGO_INITDB_ROOT_USERNAME: admin
    MONGO_INITDB_ROOT_PASSWORD: admin123
    MONGO_INITDB_DATABASE: swiftlogistics
```

### 3. Environment Variables

Create a `.env` file (or copy from `.env.example`):

```bash
MONGODB_URI=mongodb://admin:admin123@mongodb:27017/swiftlogistics?authSource=admin
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=admin123
MONGO_INITDB_DATABASE=swiftlogistics
```

## Configuration

### Database Connection

The `MongoDBClient` singleton manages connections:

```python
from shared.database import MongoDBClient, get_database

# Connect to MongoDB (usually done at app startup)
database = await MongoDBClient.connect()

# Or use convenience function
database = await get_database()
```

### FastAPI Integration

Integrate with FastAPI lifecycle:

```python
from fastapi import FastAPI
from shared.database import get_database, close_database_connection

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    """Connect to MongoDB on application startup"""
    await get_database()
    print("Connected to MongoDB")

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close MongoDB connection on application shutdown"""
    await close_database_connection()
    print("Closed MongoDB connection")
```

## Basic Usage

### Direct Database Access

```python
from shared.database import get_database

# Get database instance
db = await get_database()

# Insert a document
result = await db.orders.insert_one({
    "order_id": "ORD-001",
    "client_id": "CLI-123",
    "status": "pending",
    "items": ["item1", "item2"]
})

# Find a document
order = await db.orders.find_one({"order_id": "ORD-001"})

# Update a document
await db.orders.update_one(
    {"order_id": "ORD-001"},
    {"$set": {"status": "processing"}}
)

# Delete a document
await db.orders.delete_one({"order_id": "ORD-001"})
```

## Repository Pattern

### Using Built-in Repositories

```python
from shared.database import get_database
from shared.database.repositories import (
    OrderRepository,
    DriverRepository,
    ClientRepository,
    ShipmentRepository
)

# Initialize database
db = await get_database()

# Create repository instances
order_repo = OrderRepository(db)
driver_repo = DriverRepository(db)
client_repo = ClientRepository(db)
shipment_repo = ShipmentRepository(db)
```

### Create Operations

```python
# Create a new order
order_id = await order_repo.create({
    "order_id": "ORD-001",
    "client_id": "CLI-123",
    "status": "pending",
    "pickup_address": "123 Main St",
    "delivery_address": "456 Oak Ave",
    "items": [
        {"name": "Package 1", "weight": 10.5},
        {"name": "Package 2", "weight": 5.2}
    ],
    "total_amount": 125.00
})
```

### Read Operations

```python
# Find by custom ID
order = await order_repo.find_by_order_id("ORD-001")

# Find by MongoDB ObjectId
order = await order_repo.find_by_id("507f1f77bcf86cd799439011")

# Find multiple with pagination
orders = await order_repo.find_many(
    query={"status": "pending"},
    skip=0,
    limit=10,
    sort=[("created_at", -1)]
)

# Find by client
client_orders = await order_repo.find_by_client("CLI-123")

# Count documents
count = await order_repo.count({"status": "pending"})

# Check existence
exists = await order_repo.exists({"order_id": "ORD-001"})
```

### Update Operations

```python
# Update by custom ID
success = await order_repo.update_one(
    {"order_id": "ORD-001"},
    {"status": "processing", "assigned_driver": "DRV-456"}
)

# Update status (custom method)
success = await order_repo.update_status("ORD-001", "in_transit")

# Update multiple documents
count = await order_repo.update_many(
    {"status": "pending"},
    {"priority": "high"}
)
```

### Delete Operations

```python
# Delete by custom ID
success = await order_repo.delete_one({"order_id": "ORD-001"})

# Delete by MongoDB ObjectId
success = await order_repo.delete_by_id("507f1f77bcf86cd799439011")

# Delete multiple
count = await order_repo.delete_many({"status": "cancelled"})
```

## Examples

### Example 1: Order Management Service

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from shared.database import get_database
from shared.database.repositories import OrderRepository
from typing import List

app = FastAPI()

class OrderCreate(BaseModel):
    order_id: str
    client_id: str
    pickup_address: str
    delivery_address: str
    items: List[dict]
    total_amount: float

class OrderUpdate(BaseModel):
    status: str

@app.on_event("startup")
async def startup():
    await get_database()

@app.post("/orders")
async def create_order(order: OrderCreate):
    db = await get_database()
    order_repo = OrderRepository(db)

    # Check if order already exists
    existing = await order_repo.find_by_order_id(order.order_id)
    if existing:
        raise HTTPException(status_code=400, detail="Order already exists")

    # Create order
    order_id = await order_repo.create(order.dict())
    return {"message": "Order created", "id": order_id}

@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    db = await get_database()
    order_repo = OrderRepository(db)

    order = await order_repo.find_by_order_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order

@app.put("/orders/{order_id}/status")
async def update_order_status(order_id: str, update: OrderUpdate):
    db = await get_database()
    order_repo = OrderRepository(db)

    success = await order_repo.update_status(order_id, update.status)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": "Order status updated"}

@app.get("/orders/client/{client_id}")
async def get_client_orders(client_id: str, skip: int = 0, limit: int = 10):
    db = await get_database()
    order_repo = OrderRepository(db)

    orders = await order_repo.find_by_client(client_id, skip, limit)
    return {"orders": orders, "count": len(orders)}
```

### Example 2: Driver Location Tracking

```python
from fastapi import FastAPI
from pydantic import BaseModel
from shared.database import get_database
from shared.database.repositories import DriverRepository, ShipmentRepository

app = FastAPI()

class LocationUpdate(BaseModel):
    latitude: float
    longitude: float

@app.on_event("startup")
async def startup():
    await get_database()

@app.put("/drivers/{driver_id}/location")
async def update_driver_location(driver_id: str, location: LocationUpdate):
    db = await get_database()
    driver_repo = DriverRepository(db)

    # Update driver's current location
    success = await driver_repo.update_one(
        {"driver_id": driver_id},
        {
            "current_location": {
                "latitude": location.latitude,
                "longitude": location.longitude
            }
        }
    )

    # Also update active shipment location
    shipment_repo = ShipmentRepository(db)
    active_shipments = await shipment_repo.find_many({
        "driver_id": driver_id,
        "status": "in_transit"
    }, limit=1)

    if active_shipments:
        await shipment_repo.update_location(
            active_shipments[0]["shipment_id"],
            {"latitude": location.latitude, "longitude": location.longitude}
        )

    return {"message": "Location updated"}
```

### Example 3: Custom Repository

Create your own repository for specific needs:

```python
from shared.database.base_repository import BaseRepository
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Dict, Any

class CustomOrderRepository(BaseRepository):
    """Extended Order Repository with custom analytics"""

    def __init__(self, database: AsyncIOMotorDatabase):
        super().__init__(database, "orders")

    async def get_revenue_by_client(self) -> List[Dict[str, Any]]:
        """Get total revenue grouped by client"""
        pipeline = [
            {
                "$group": {
                    "_id": "$client_id",
                    "total_revenue": {"$sum": "$total_amount"},
                    "order_count": {"$sum": 1}
                }
            },
            {
                "$sort": {"total_revenue": -1}
            }
        ]
        return await self.aggregate(pipeline)

    async def get_orders_by_status_count(self) -> Dict[str, int]:
        """Get count of orders by status"""
        pipeline = [
            {
                "$group": {
                    "_id": "$status",
                    "count": {"$sum": 1}
                }
            }
        ]
        results = await self.aggregate(pipeline)
        return {result["_id"]: result["count"] for result in results}

# Usage
db = await get_database()
order_repo = CustomOrderRepository(db)
revenue_stats = await order_repo.get_revenue_by_client()
```

## Best Practices

### 1. Use Connection Pooling

The `MongoDBClient` automatically manages connection pooling. Don't create multiple connections.

```python
# ✅ Good - Reuse connection
db = await get_database()

# ❌ Bad - Don't create new connections
client = AsyncIOMotorClient(uri)  # Don't do this
```

### 2. Handle Errors Gracefully

```python
from pymongo.errors import DuplicateKeyError, ConnectionFailure

try:
    await order_repo.create(order_data)
except DuplicateKeyError:
    raise HTTPException(status_code=400, detail="Order ID already exists")
except ConnectionFailure:
    raise HTTPException(status_code=503, detail="Database unavailable")
```

### 3. Use Transactions for Critical Operations

```python
from motor.motor_asyncio import AsyncIOMotorClientSession

async def transfer_order(order_id: str, from_driver: str, to_driver: str):
    db = await get_database()

    async with await db.client.start_session() as session:
        async with session.start_transaction():
            # Update order
            await db.orders.update_one(
                {"order_id": order_id},
                {"$set": {"driver_id": to_driver}},
                session=session
            )

            # Update shipment
            await db.shipments.update_one(
                {"order_id": order_id},
                {"$set": {"driver_id": to_driver}},
                session=session
            )
```

### 4. Use Indexes for Performance

Indexes are automatically created for common fields. Add custom indexes if needed:

```python
@app.on_event("startup")
async def create_indexes():
    db = await get_database()

    # Create custom compound index
    await db.orders.create_index([
        ("client_id", 1),
        ("status", 1),
        ("created_at", -1)
    ])
```

### 5. Implement Pagination

Always use pagination for list endpoints:

```python
@app.get("/orders")
async def list_orders(skip: int = 0, limit: int = 20):
    db = await get_database()
    order_repo = OrderRepository(db)

    # Limit maximum page size
    limit = min(limit, 100)

    orders = await order_repo.find_many(
        skip=skip,
        limit=limit,
        sort=[("created_at", -1)]
    )

    total = await order_repo.count()

    return {
        "orders": orders,
        "total": total,
        "skip": skip,
        "limit": limit
    }
```

## Troubleshooting

### Connection Issues

**Problem:** "Could not connect to MongoDB"

**Solutions:**

1. Check if MongoDB is running:

   ```bash
   docker ps | grep mongodb
   ```

2. Verify connection string in `.env`:

   ```bash
   MONGODB_URI=mongodb://admin:admin123@mongodb:27017/swiftlogistics?authSource=admin
   ```

3. For local development (outside Docker):
   ```bash
   MONGODB_URI=mongodb://admin:admin123@localhost:27017/swiftlogistics?authSource=admin
   ```

### Authentication Errors

**Problem:** "Authentication failed"

**Solution:** Ensure credentials match in `.env` and `docker-compose.yml`:

```yaml
MONGO_INITDB_ROOT_USERNAME: admin
MONGO_INITDB_ROOT_PASSWORD: admin123
```

### Slow Queries

**Problem:** Queries are slow

**Solutions:**

1. Check if indexes exist:

   ```python
   indexes = await db.orders.list_indexes().to_list(length=None)
   print(indexes)
   ```

2. Add indexes for frequently queried fields
3. Use aggregation pipelines for complex queries
4. Enable MongoDB query profiling

### Memory Issues

**Problem:** High memory usage

**Solutions:**

1. Use pagination for large result sets
2. Limit document size
3. Use projection to fetch only needed fields:
   ```python
   order = await db.orders.find_one(
       {"order_id": "ORD-001"},
       {"order_id": 1, "status": 1, "_id": 0}
   )
   ```

## Additional Resources

- [Motor Documentation](https://motor.readthedocs.io/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [MongoDB Best Practices](https://www.mongodb.com/docs/manual/administration/production-notes/)
- [FastAPI with MongoDB](https://fastapi.tiangolo.com/advanced/nosql-databases/)

## Support

For issues or questions:

1. Check the logs: `docker logs swiftlogistics-mongodb`
2. Review this documentation
3. Contact the development team
