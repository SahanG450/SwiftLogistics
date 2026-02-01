from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class RouteStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# New Enums for Driver Manifests
class ManifestStatus(str, Enum):
    DRAFT = "draft"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class DeliveryStatus(str, Enum):
    PENDING = "pending"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    FAILED = "failed"


class Coordinates(BaseModel):
    latitude: float
    longitude: float


class RouteStop(BaseModel):
    location: str
    coordinates: Optional[Coordinates] = None
    estimated_arrival: Optional[str] = None
    actual_arrival: Optional[str] = None


# Delivery Manifest Schemas for Driver App
class ManifestDelivery(BaseModel):
    order_id: str
    package_id: str
    tracking_number: str
    recipient_name: str
    delivery_address: str
    contact_phone: str
    coordinates: Optional[Coordinates] = None
    priority: str = "normal"  # low, normal, high, urgent
    special_instructions: Optional[str] = None
    estimated_delivery_time: Optional[str] = None
    status: DeliveryStatus = DeliveryStatus.PENDING


class ManifestCreate(BaseModel):
    driver_id: str
    vehicle_id: str
    route_id: str
    deliveries: List[ManifestDelivery]
    delivery_date: str


class ManifestUpdate(BaseModel):
    status: Optional[ManifestStatus] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    notes: Optional[str] = None


class DeliveryManifest(BaseModel):
    id: str
    manifest_number: str
    driver_id: str
    driver_name: Optional[str] = None
    vehicle_id: str
    route_id: str
    deliveries: List[ManifestDelivery]
    delivery_date: str
    status: ManifestStatus = ManifestStatus.DRAFT
    total_deliveries: int
    completed_deliveries: int = 0
    failed_deliveries: int = 0
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    notes: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# Route Optimization Request/Response
class OptimizationRequest(BaseModel):
    delivery_addresses: List[dict]  # List of addresses with coordinates
    vehicle_capacity: Optional[int] = None
    max_route_duration: Optional[int] = None  # in minutes
    start_location: Optional[Coordinates] = None
    priority_deliveries: Optional[List[str]] = []  # List of order IDs


class OptimizedRoute(BaseModel):
    route_id: str
    optimized_sequence: List[int]  # Indices of addresses in optimal order
    total_distance: float  # in kilometers
    estimated_duration: int  # in minutes
    waypoints: List[dict]
    created_at: str


class RouteCreate(BaseModel):
    origin: str
    destination: str
    vehicle_id: Optional[str] = None
    driver_id: Optional[str] = None
    stops: Optional[List[RouteStop]] = []
    estimated_duration: Optional[int] = None  # in minutes


class RouteUpdate(BaseModel):
    status: Optional[RouteStatus] = None
    vehicle_id: Optional[str] = None
    driver_id: Optional[str] = None
    stops: Optional[List[RouteStop]] = None
    actual_duration: Optional[int] = None


class Route(BaseModel):
    id: str
    origin: str
    destination: str
    vehicle_id: Optional[str] = None
    driver_id: Optional[str] = None
    stops: List[RouteStop] = []
    status: RouteStatus = RouteStatus.PLANNED
    estimated_duration: Optional[int] = None
    actual_duration: Optional[int] = None
    distance: Optional[float] = None  # in kilometers
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
