from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class InventoryStatus(str, Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    OUT_OF_STOCK = "out_of_stock"
    DAMAGED = "damaged"


# New Enums for Package Tracking
class PackageStatus(str, Enum):
    RECEIVED = "received"  # Package received from client
    INSPECTED = "inspected"  # Quality check completed
    STORED = "stored"  # Placed in warehouse location
    PICKED = "picked"  # Retrieved for delivery
    PACKED = "packed"  # Packed for loading
    LOADED = "loaded"  # Loaded onto vehicle
    IN_TRANSIT = "in_transit"  # On delivery route
    DELIVERED = "delivered"  # Successfully delivered
    RETURNED = "returned"  # Returned to warehouse


class PackageCondition(str, Enum):
    GOOD = "good"
    FAIR = "fair"
    DAMAGED = "damaged"
    LOST = "lost"


# Package Tracking Schemas for Swift Logistics
class PackageLocation(BaseModel):
    warehouse_id: str = "WH-MAIN-01"
    zone: Optional[str] = None
    aisle: Optional[str] = None
    rack: Optional[str] = None
    shelf: Optional[str] = None
    bin: Optional[str] = None


class PackageEvent(BaseModel):
    event_type: str  # e.g., "received", "moved", "loaded"
    timestamp: str
    location: Optional[str] = None
    performed_by: Optional[str] = None
    notes: Optional[str] = None


class PackageCreate(BaseModel):
    order_id: str
    tracking_number: Optional[str] = None  # Auto-generated if not provided
    client_id: str
    description: str
    weight: Optional[float] = None  # in kg
    dimensions: Optional[str] = None  # e.g., "30x20x15 cm"
    special_handling: Optional[str] = None


class PackageUpdate(BaseModel):
    status: Optional[PackageStatus] = None
    condition: Optional[PackageCondition] = None
    location: Optional[PackageLocation] = None
    assigned_vehicle_id: Optional[str] = None
    assigned_driver_id: Optional[str] = None
    notes: Optional[str] = None


class Package(BaseModel):
    id: str
    tracking_number: str
    order_id: str
    client_id: str
    description: str
    status: PackageStatus = PackageStatus.RECEIVED
    condition: PackageCondition = PackageCondition.GOOD
    location: Optional[PackageLocation] = None
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    special_handling: Optional[str] = None
    assigned_vehicle_id: Optional[str] = None
    assigned_driver_id: Optional[str] = None
    received_at: str
    loaded_at: Optional[str] = None
    delivered_at: Optional[str] = None
    events: List[PackageEvent] = []
    notes: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class WarehouseLocation(BaseModel):
    warehouse_id: str
    zone: Optional[str] = None
    aisle: Optional[str] = None
    rack: Optional[str] = None
    bin: Optional[str] = None


class InventoryCreate(BaseModel):
    sku: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=200)
    quantity: int = Field(..., ge=0)
    location: Optional[WarehouseLocation] = None
    unit_price: Optional[float] = Field(None, ge=0)
    reorder_level: Optional[int] = Field(None, ge=0)


class InventoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    quantity: Optional[int] = Field(None, ge=0)
    location: Optional[WarehouseLocation] = None
    status: Optional[InventoryStatus] = None
    unit_price: Optional[float] = Field(None, ge=0)
    reorder_level: Optional[int] = Field(None, ge=0)


class Inventory(BaseModel):
    id: str
    sku: str
    name: str
    quantity: int
    location: Optional[WarehouseLocation] = None
    status: InventoryStatus = InventoryStatus.AVAILABLE
    unit_price: Optional[float] = None
    reorder_level: Optional[int] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
