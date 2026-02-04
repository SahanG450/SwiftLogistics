"""Order document model using Beanie ODM."""

from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional, Dict, Any


class Order(Document):
    """Order document stored in MongoDB."""
    
    orderId: str = Field(..., description="Unique order identifier")
    customerId: str = Field(..., description="Customer ID")
    
    # Location data
    pickupLocation: Dict[str, Any]
    deliveryAddress: Dict[str, Any]
    
    # Package information
    packageDetails: Dict[str, Any]
    
    # Order metadata
    status: str = Field(default="RECEIVED", description="Order status")
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    
    # Integration status
    integrationStatus: Dict[str, str] = Field(
        default_factory=lambda: {
            "cms": "PENDING",
            "ros": "PENDING",
            "wms": "PENDING"
        }
    )
    
    # Additional fields
    scheduledPickupTime: Optional[datetime] = None
    specialInstructions: Optional[str] = None
    
    class Settings:
        name = "orders"
        indexes = [
            "orderId",
            "customerId",
            "status",
            "createdAt"
        ]
