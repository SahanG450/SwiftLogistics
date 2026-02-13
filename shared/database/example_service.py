"""
Example FastAPI service demonstrating MongoDB integration
This can be used as a template for your actual services
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uvicorn
import os
import logging

# Import MongoDB utilities from shared folder
import sys
sys.path.append('/app/shared')  # Adjust based on your project structure

from database import get_database, close_database_connection
from database.repositories import (
    OrderRepository,
    DriverRepository,
    ClientRepository,
    ShipmentRepository
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="SwiftLogistics MongoDB Example Service",
    description="Example service demonstrating MongoDB integration",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================================
# Pydantic Models (Request/Response)
# ========================================

class OrderCreate(BaseModel):
    order_id: str = Field(..., description="Unique order identifier")
    client_id: str = Field(..., description="Client identifier")
    pickup_address: str
    delivery_address: str
    items: List[dict] = Field(default_factory=list)
    total_amount: float = Field(..., gt=0)
    status: str = Field(default="pending")


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    driver_id: Optional[str] = None
    notes: Optional[str] = None


class DriverCreate(BaseModel):
    driver_id: str
    name: str
    email: str
    phone: str
    license_number: str
    vehicle_type: str
    status: str = Field(default="available")


class LocationUpdate(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


# ========================================
# Lifecycle Events
# ========================================

@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB on application startup"""
    try:
        db = await get_database()
        logger.info("✓ Connected to MongoDB successfully")
        
        # Optional: Initialize with sample data
        order_repo = OrderRepository(db)
        count = await order_repo.count()
        logger.info(f"Database contains {count} orders")
        
    except Exception as e:
        logger.error(f"✗ Failed to connect to MongoDB: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on application shutdown"""
    await close_database_connection()
    logger.info("✓ MongoDB connection closed")


# ========================================
# Health & Info Endpoints
# ========================================

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "SwiftLogistics MongoDB Example",
        "status": "running",
        "version": "1.0.0",
        "mongodb": "connected" if (await get_database()) else "disconnected"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint with database statistics"""
    try:
        db = await get_database()
        
        # Get counts from different collections
        order_repo = OrderRepository(db)
        driver_repo = DriverRepository(db)
        client_repo = ClientRepository(db)
        
        order_count = await order_repo.count()
        driver_count = await driver_repo.count()
        client_count = await client_repo.count()
        
        return {
            "status": "healthy",
            "database": "connected",
            "collections": {
                "orders": order_count,
                "drivers": driver_count,
                "clients": client_count
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


# ========================================
# Order Endpoints
# ========================================

@app.post("/orders", status_code=201)
async def create_order(order: OrderCreate):
    """Create a new order"""
    try:
        db = await get_database()
        order_repo = OrderRepository(db)
        
        # Check if order already exists
        existing = await order_repo.find_by_order_id(order.order_id)
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Order {order.order_id} already exists"
            )
        
        # Create order
        order_data = order.dict()
        order_id = await order_repo.create(order_data)
        
        logger.info(f"Created order: {order.order_id}")
        
        return {
            "message": "Order created successfully",
            "order_id": order.order_id,
            "id": order_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create order: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    """Get a specific order by ID"""
    try:
        db = await get_database()
        order_repo = OrderRepository(db)
        
        order = await order_repo.find_by_order_id(order_id)
        
        if not order:
            raise HTTPException(
                status_code=404,
                detail=f"Order {order_id} not found"
            )
        
        return order
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get order: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/orders")
async def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    client_id: Optional[str] = None
):
    """List orders with optional filtering and pagination"""
    try:
        db = await get_database()
        order_repo = OrderRepository(db)
        
        # Build query
        query = {}
        if status:
            query["status"] = status
        if client_id:
            query["client_id"] = client_id
        
        # Get orders
        orders = await order_repo.find_many(
            query=query,
            skip=skip,
            limit=limit,
            sort=[("created_at", -1)]
        )
        
        # Get total count
        total = await order_repo.count(query)
        
        return {
            "orders": orders,
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": (skip + limit) < total
        }
        
    except Exception as e:
        logger.error(f"Failed to list orders: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/orders/{order_id}")
async def update_order(order_id: str, update: OrderUpdate):
    """Update an order"""
    try:
        db = await get_database()
        order_repo = OrderRepository(db)
        
        # Build update data (only include non-None fields)
        update_data = {k: v for k, v in update.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="No fields to update"
            )
        
        # Update order
        success = await order_repo.update_one(
            {"order_id": order_id},
            update_data
        )
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Order {order_id} not found"
            )
        
        logger.info(f"Updated order: {order_id}")
        
        return {"message": "Order updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update order: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/orders/{order_id}/status")
async def update_order_status(order_id: str, status: str):
    """Update order status"""
    try:
        db = await get_database()
        order_repo = OrderRepository(db)
        
        success = await order_repo.update_status(order_id, status)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Order {order_id} not found"
            )
        
        logger.info(f"Updated order {order_id} status to: {status}")
        
        return {
            "message": "Order status updated",
            "order_id": order_id,
            "status": status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update order status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/orders/{order_id}")
async def delete_order(order_id: str):
    """Delete an order"""
    try:
        db = await get_database()
        order_repo = OrderRepository(db)
        
        success = await order_repo.delete_one({"order_id": order_id})
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Order {order_id} not found"
            )
        
        logger.info(f"Deleted order: {order_id}")
        
        return {"message": "Order deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete order: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Driver Endpoints
# ========================================

@app.post("/drivers", status_code=201)
async def create_driver(driver: DriverCreate):
    """Create a new driver"""
    try:
        db = await get_database()
        driver_repo = DriverRepository(db)
        
        # Check if driver already exists
        existing = await driver_repo.find_by_driver_id(driver.driver_id)
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Driver {driver.driver_id} already exists"
            )
        
        # Create driver
        driver_data = driver.dict()
        driver_id = await driver_repo.create(driver_data)
        
        logger.info(f"Created driver: {driver.driver_id}")
        
        return {
            "message": "Driver created successfully",
            "driver_id": driver.driver_id,
            "id": driver_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create driver: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/drivers/{driver_id}")
async def get_driver(driver_id: str):
    """Get a specific driver by ID"""
    try:
        db = await get_database()
        driver_repo = DriverRepository(db)
        
        driver = await driver_repo.find_by_driver_id(driver_id)
        
        if not driver:
            raise HTTPException(
                status_code=404,
                detail=f"Driver {driver_id} not found"
            )
        
        return driver
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get driver: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/drivers")
async def list_drivers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None
):
    """List drivers with optional filtering"""
    try:
        db = await get_database()
        driver_repo = DriverRepository(db)
        
        # Build query
        query = {}
        if status:
            query["status"] = status
        
        # Get drivers
        drivers = await driver_repo.find_many(
            query=query,
            skip=skip,
            limit=limit
        )
        
        total = await driver_repo.count(query)
        
        return {
            "drivers": drivers,
            "total": total,
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Failed to list drivers: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/drivers/{driver_id}/location")
async def update_driver_location(driver_id: str, location: LocationUpdate):
    """Update driver's current location"""
    try:
        db = await get_database()
        driver_repo = DriverRepository(db)
        shipment_repo = ShipmentRepository(db)
        
        # Update driver location
        success = await driver_repo.update_one(
            {"driver_id": driver_id},
            {
                "current_location": {
                    "latitude": location.latitude,
                    "longitude": location.longitude
                },
                "location_updated_at": datetime.utcnow()
            }
        )
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Driver {driver_id} not found"
            )
        
        # Also update active shipment location
        active_shipments = await shipment_repo.find_many({
            "driver_id": driver_id,
            "status": "in_transit"
        }, limit=1)
        
        if active_shipments:
            await shipment_repo.update_location(
                active_shipments[0]["shipment_id"],
                {"latitude": location.latitude, "longitude": location.longitude}
            )
        
        logger.info(f"Updated location for driver: {driver_id}")
        
        return {
            "message": "Driver location updated",
            "driver_id": driver_id,
            "location": location.dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update driver location: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Analytics Endpoints
# ========================================

@app.get("/analytics/orders-by-status")
async def orders_by_status():
    """Get order counts grouped by status"""
    try:
        db = await get_database()
        order_repo = OrderRepository(db)
        
        pipeline = [
            {
                "$group": {
                    "_id": "$status",
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"count": -1}
            }
        ]
        
        results = await order_repo.aggregate(pipeline)
        
        return {
            "statistics": results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Run Application
# ========================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "example_service:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
