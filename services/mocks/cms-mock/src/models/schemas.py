from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# Customer Models
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


# Driver Models
class DriverStatus(str, Enum):
    AVAILABLE = "available"
    ON_ROUTE = "on_route"
    OFFLINE = "offline"
    INACTIVE = "inactive"


class DriverCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    phone: str
    license_number: str
    vehicle_type: Optional[str] = None
    vehicle_plate: Optional[str] = None


class DriverUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[str] = Field(None, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    phone: Optional[str] = None
    license_number: Optional[str] = None
    vehicle_type: Optional[str] = None
    vehicle_plate: Optional[str] = None
    status: Optional[DriverStatus] = None


class Driver(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    license_number: str
    vehicle_type: Optional[str] = None
    vehicle_plate: Optional[str] = None
    status: DriverStatus = DriverStatus.AVAILABLE
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# Client Models
class MembershipLevel(str, Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"


class ClientCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    phone: str
    company: str
    address: Optional[str] = None
    membership_level: MembershipLevel = MembershipLevel.BRONZE


class ClientUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[str] = Field(None, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    phone: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    membership_level: Optional[MembershipLevel] = None


class Client(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    company: str
    address: Optional[str] = None
    membership_level: MembershipLevel
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# Admin Models
class AdminRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"


class AdminCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    password: str = Field(..., min_length=8)
    role: AdminRole = AdminRole.VIEWER


class AdminUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = Field(None, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[AdminRole] = None


class Admin(BaseModel):
    id: str
    username: str
    email: str
    role: AdminRole
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# Order Models
class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_WAREHOUSE = "in_warehouse"
    READY_FOR_DELIVERY = "ready_for_delivery"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    FAILED = "failed"
    CANCELLED = "cancelled"


class DeliveryFailureReason(str, Enum):
    ADDRESS_NOT_FOUND = "address_not_found"
    RECIPIENT_UNAVAILABLE = "recipient_unavailable"
    REFUSED_DELIVERY = "refused_delivery"
    DAMAGED_PACKAGE = "damaged_package"
    WEATHER_CONDITIONS = "weather_conditions"
    OTHER = "other"


class ProofOfDelivery(BaseModel):
    signature: Optional[str] = None
    photo_url: Optional[str] = None
    recipient_name: Optional[str] = None
    notes: Optional[str] = None
    timestamp: Optional[str] = None


class OrderCreate(BaseModel):
    client_id: str
    delivery_address: Dict[str, Any]
    items: List[Dict[str, Any]]
    priority: str = "normal"
    special_instructions: Optional[str] = None


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    assigned_driver_id: Optional[str] = None
    assigned_route_id: Optional[str] = None
    proof_of_delivery: Optional[ProofOfDelivery] = None
    failure_reason: Optional[DeliveryFailureReason] = None
    special_instructions: Optional[str] = None


class Order(BaseModel):
    id: str
    order_number: str
    client_id: str
    delivery_address: Dict[str, Any]
    items: List[Dict[str, Any]]
    status: OrderStatus
    priority: str
    assigned_driver_id: Optional[str] = None
    assigned_route_id: Optional[str] = None
    proof_of_delivery: Optional[ProofOfDelivery] = None
    failure_reason: Optional[DeliveryFailureReason] = None
    special_instructions: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# Contract Models
class ContractStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
    TERMINATED = "terminated"


class ContractCreate(BaseModel):
    client_id: str
    start_date: str
    end_date: str
    pricing_tier: str
    monthly_volume: int
    rate_per_delivery: float
    terms: Optional[str] = None


class ContractUpdate(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    pricing_tier: Optional[str] = None
    monthly_volume: Optional[int] = None
    rate_per_delivery: Optional[float] = None
    status: Optional[ContractStatus] = None
    terms: Optional[str] = None


class Contract(BaseModel):
    id: str
    contract_number: str
    client_id: str
    start_date: str
    end_date: str
    pricing_tier: str
    monthly_volume: int
    rate_per_delivery: float
    status: ContractStatus
    terms: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# Billing Models
class BillingCreate(BaseModel):
    client_id: str
    period_start: str
    period_end: str
    total_deliveries: int
    amount: float
    due_date: str


class BillingUpdate(BaseModel):
    paid: Optional[bool] = None
    payment_date: Optional[str] = None
    payment_method: Optional[str] = None


class BillingInvoice(BaseModel):
    id: str
    invoice_number: str
    client_id: str
    period_start: str
    period_end: str
    total_deliveries: int
    amount: float
    paid: bool = False
    due_date: str
    payment_date: Optional[str] = None
    payment_method: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# Error Response
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
