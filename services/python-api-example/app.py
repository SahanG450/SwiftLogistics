"""
SwiftLogistics Python API with MongoDB Integration
This example shows how to create REST API endpoints that connect to MongoDB
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import os
import sys

# Add shared database to path
sys.path.append('/app/shared')
from database.mongodb import get_database, MongoDBClient, close_database_connection

# Initialize FastAPI app
app = FastAPI(
    title="SwiftLogistics API",
    description="API for managing logistics orders, shipments, and drivers",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== DATA MODELS ====================

class Order(BaseModel):
    """Order model for creating new orders"""
    order_id: Optional[str] = None
    client_id: str
    pickup_location: str
    delivery_location: str
    package_details: str
    status: str = "pending"
    created_at: Optional[datetime] = None
    
class OrderResponse(BaseModel):
    """Order response model"""
    order_id: str
    client_id: str
    pickup_location: str
    delivery_location: str
    package_details: str
    status: str
    created_at: datetime
    
class Shipment(BaseModel):
    """Shipment model"""
    shipment_id: Optional[str] = None
    order_id: str
    driver_id: Optional[str] = None
    vehicle_id: Optional[str] = None
    status: str = "pending"
    pickup_time: Optional[datetime] = None
    delivery_time: Optional[datetime] = None
    
class Driver(BaseModel):
    """Driver model"""
    driver_id: Optional[str] = None
    name: str
    email: str
    phone: str
    license_number: str
    status: str = "available"
    
# ==================== STARTUP/SHUTDOWN ====================

@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB on startup"""
    print("🚀 Starting SwiftLogistics API...")
    mongodb_uri = os.getenv(
        "MONGODB_URI",
        "mongodb://admin:admin123@mongodb:27017/swiftlogistics?authSource=admin"
    )
    try:
        await MongoDBClient.connect(mongodb_uri)
        print("✅ Connected to MongoDB successfully!")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown"""
    print("🛑 Shutting down SwiftLogistics API...")
    await close_database_connection()
    print("✅ MongoDB connection closed")

# ==================== HEALTH CHECK ====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SwiftLogistics API",
        "mongodb_connected": MongoDBClient.is_connected(),
        "timestamp": datetime.utcnow()
    }

# ==================== ORDERS ENDPOINTS ====================

@app.post("/api/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: Order):
    """
    Create a new order
    
    Endpoint: POST http://localhost:3000/api/orders
    Body: {
        "client_id": "CLIENT-001",
        "pickup_location": "123 Main St",
        "delivery_location": "456 Oak Ave",
        "package_details": "Electronics - Handle with care"
    }
    """
    db = await get_database()
    
    # Generate order ID
    count = await db.orders.count_documents({})
    order_id = f"ORDER-{count + 1:06d}"
    
    # Prepare order document
    order_data = order.dict()
    order_data["order_id"] = order_id
    order_data["created_at"] = datetime.utcnow()
    
    # Insert into MongoDB
    result = await db.orders.insert_one(order_data)
    
    if result.inserted_id:
        print(f"✅ Order created: {order_id}")
        return order_data
    else:
        raise HTTPException(status_code=500, detail="Failed to create order")

@app.get("/api/orders", response_model=List[OrderResponse])
async def get_all_orders(status: Optional[str] = None, limit: int = 100):
    """
    Get all orders with optional status filter
    
    Endpoint: GET http://localhost:3000/api/orders
    Query params: ?status=pending&limit=10
    """
    db = await get_database()
    
    # Build query
    query = {}
    if status:
        query["status"] = status
    
    # Fetch orders
    cursor = db.orders.find(query).limit(limit).sort("created_at", -1)
    orders = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string for JSON serialization
    for order in orders:
        order["_id"] = str(order["_id"])
    
    return orders

@app.get("/api/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    """
    Get a specific order by ID
    
    Endpoint: GET http://localhost:3000/api/orders/ORDER-000001
    """
    db = await get_database()
    
    order = await db.orders.find_one({"order_id": order_id})
    
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    
    order["_id"] = str(order["_id"])
    return order

@app.put("/api/orders/{order_id}/status")
async def update_order_status(order_id: str, status: str):
    """
    Update order status
    
    Endpoint: PUT http://localhost:3000/api/orders/ORDER-000001/status
    Body: { "status": "in-transit" }
    """
    db = await get_database()
    
    result = await db.orders.update_one(
        {"order_id": order_id},
        {"$set": {"status": status, "updated_at": datetime.utcnow()}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    
    return {"message": f"Order {order_id} status updated to {status}"}

@app.delete("/api/orders/{order_id}")
async def delete_order(order_id: str):
    """
    Delete an order
    
    Endpoint: DELETE http://localhost:3000/api/orders/ORDER-000001
    """
    db = await get_database()
    
    result = await db.orders.delete_one({"order_id": order_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    
    return {"message": f"Order {order_id} deleted successfully"}

# ==================== SHIPMENTS ENDPOINTS ====================

@app.post("/api/shipments", status_code=status.HTTP_201_CREATED)
async def create_shipment(shipment: Shipment):
    """
    Create a new shipment
    
    Endpoint: POST http://localhost:3000/api/shipments
    """
    db = await get_database()
    
    # Generate shipment ID
    count = await db.shipments.count_documents({})
    shipment_id = f"SHIP-{count + 1:06d}"
    
    shipment_data = shipment.dict()
    shipment_data["shipment_id"] = shipment_id
    shipment_data["created_at"] = datetime.utcnow()
    
    await db.shipments.insert_one(shipment_data)
    
    print(f"✅ Shipment created: {shipment_id}")
    return shipment_data

@app.get("/api/shipments")
async def get_all_shipments(driver_id: Optional[str] = None, status: Optional[str] = None):
    """
    Get all shipments with optional filters
    
    Endpoint: GET http://localhost:3000/api/shipments?driver_id=DRV-001&status=in-transit
    """
    db = await get_database()
    
    query = {}
    if driver_id:
        query["driver_id"] = driver_id
    if status:
        query["status"] = status
    
    cursor = db.shipments.find(query).limit(100)
    shipments = await cursor.to_list(length=100)
    
    for shipment in shipments:
        shipment["_id"] = str(shipment["_id"])
    
    return shipments

# ==================== DRIVERS ENDPOINTS ====================

@app.post("/api/drivers", status_code=status.HTTP_201_CREATED)
async def create_driver(driver: Driver):
    """
    Create a new driver
    
    Endpoint: POST http://localhost:3000/api/drivers
    Body: {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "license_number": "DL123456"
    }
    """
    db = await get_database()
    
    # Check if email already exists
    existing = await db.drivers.find_one({"email": driver.email})
    if existing:
        raise HTTPException(status_code=400, detail="Driver with this email already exists")
    
    # Generate driver ID
    count = await db.drivers.count_documents({})
    driver_id = f"DRV-{count + 1:04d}"
    
    driver_data = driver.dict()
    driver_data["driver_id"] = driver_id
    driver_data["created_at"] = datetime.utcnow()
    
    await db.drivers.insert_one(driver_data)
    
    print(f"✅ Driver created: {driver_id}")
    return driver_data

@app.get("/api/drivers")
async def get_all_drivers(status: Optional[str] = None):
    """
    Get all drivers
    
    Endpoint: GET http://localhost:3000/api/drivers?status=available
    """
    db = await get_database()
    
    query = {}
    if status:
        query["status"] = status
    
    cursor = db.drivers.find(query).limit(100)
    drivers = await cursor.to_list(length=100)
    
    for driver in drivers:
        driver["_id"] = str(driver["_id"])
    
    return drivers

@app.get("/api/drivers/{driver_id}")
async def get_driver(driver_id: str):
    """
    Get a specific driver
    
    Endpoint: GET http://localhost:3000/api/drivers/DRV-0001
    """
    db = await get_database()
    
    driver = await db.drivers.find_one({"driver_id": driver_id})
    
    if not driver:
        raise HTTPException(status_code=404, detail=f"Driver {driver_id} not found")
    
    driver["_id"] = str(driver["_id"])
    return driver

# ==================== STATISTICS ENDPOINTS ====================

@app.get("/api/stats")
async def get_statistics():
    """
    Get system statistics
    
    Endpoint: GET http://localhost:3000/api/stats
    """
    db = await get_database()
    
    total_orders = await db.orders.count_documents({})
    pending_orders = await db.orders.count_documents({"status": "pending"})
    completed_orders = await db.orders.count_documents({"status": "delivered"})
    total_drivers = await db.drivers.count_documents({})
    available_drivers = await db.drivers.count_documents({"status": "available"})
    total_shipments = await db.shipments.count_documents({})
    
    return {
        "orders": {
            "total": total_orders,
            "pending": pending_orders,
            "completed": completed_orders
        },
        "drivers": {
            "total": total_drivers,
            "available": available_drivers
        },
        "shipments": {
            "total": total_shipments
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)
