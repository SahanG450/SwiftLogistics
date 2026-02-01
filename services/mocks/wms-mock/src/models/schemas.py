from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class InventoryStatus(str, Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    OUT_OF_STOCK = "out_of_stock"
    DAMAGED = "damaged"


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
