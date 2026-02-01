from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class CustomerStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    phone: Optional[str] = None
    address: Optional[str] = None
    company: Optional[str] = None


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[str] = Field(None, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    phone: Optional[str] = None
    address: Optional[str] = None
    company: Optional[str] = None
    status: Optional[CustomerStatus] = None


class Customer(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    company: Optional[str] = None
    status: CustomerStatus = CustomerStatus.ACTIVE
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
