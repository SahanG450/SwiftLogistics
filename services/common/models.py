"""Shared Pydantic models for request/response schemas."""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime


class LocationSchema(BaseModel):
    """Geographic location."""
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lng: float = Field(..., ge=-180, le=180, description="Longitude")
    address: Optional[str] = Field(None, description="Address string")


class PackageDetailsSchema(BaseModel):
    """Package information."""
    weight: float = Field(..., gt=0, description="Weight in kg")
    description: Optional[str] = Field(None, description="Package description")
    dimensions: Optional[Dict[str, float]] = Field(None, description="Dimensions (length, width, height)")
    fragile: bool = Field(False, description="Is package fragile")


class OrderCreateRequest(BaseModel):
    """Request schema for creating an order."""
    pickupLocation: LocationSchema
    deliveryAddress: LocationSchema
    packageDetails: PackageDetailsSchema
    scheduledPickupTime: Optional[datetime] = None
    specialInstructions: Optional[str] = None


class OrderResponse(BaseModel):
    """Response schema for order."""
    orderId: str
    status: str
    message: Optional[str] = None
    customerId: Optional[str] = None
    createdAt: Optional[datetime] = None


class UserLoginRequest(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class UserRegisterRequest(BaseModel):
    """User registration request."""
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: Optional[str] = None
    company: Optional[str] = None


class TokenResponse(BaseModel):
    """Authentication token response."""
    token: str
    user: Dict[str, Any]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    service: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
