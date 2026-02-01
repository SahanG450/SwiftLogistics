from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

from ..models.schemas import (
    Package,
    PackageCreate,
    PackageUpdate,
    PackageStatus,
    PackageCondition,
    PackageLocation,
)
from ..services.package_service import PackageService

router = APIRouter(prefix="/api/packages", tags=["Packages"])
package_service = PackageService()


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


@router.get("/", response_model=List[Package])
async def get_all_packages(
    status: Optional[PackageStatus] = Query(
        None, description="Filter by package status"
    ),
    client_id: Optional[str] = Query(None, description="Filter by client ID"),
    order_id: Optional[str] = Query(None, description="Filter by order ID"),
):
    """Get all packages with optional filtering"""
    return package_service.get_all_packages(
        status=status, client_id=client_id, order_id=order_id
    )


@router.get("/{package_id}", response_model=Package)
async def get_package(package_id: str):
    """Get a specific package by ID"""
    package = package_service.get_package(package_id)
    if not package:
        raise HTTPException(
            status_code=404, detail=f"Package with ID {package_id} not found"
        )
    return package


@router.get("/tracking/{tracking_number}", response_model=Package)
async def get_package_by_tracking(tracking_number: str):
    """Get a package by tracking number"""
    package = package_service.get_package_by_tracking(tracking_number)
    if not package:
        raise HTTPException(
            status_code=404,
            detail=f"Package with tracking number {tracking_number} not found",
        )
    return package


@router.post("/", response_model=Package, status_code=201)
async def create_package(package: PackageCreate):
    """Create a new package (receive from client)"""
    return package_service.create_package(package)


@router.put("/{package_id}", response_model=Package)
async def update_package(package_id: str, package: PackageUpdate):
    """Update an existing package"""
    updated_package = package_service.update_package(package_id, package)
    if not updated_package:
        raise HTTPException(
            status_code=404, detail=f"Package with ID {package_id} not found"
        )
    return updated_package


@router.delete("/{package_id}", status_code=204)
async def delete_package(package_id: str):
    """Delete a package"""
    if not package_service.delete_package(package_id):
        raise HTTPException(
            status_code=404, detail=f"Package with ID {package_id} not found"
        )


@router.post("/{package_id}/inspect", response_model=Package)
async def inspect_package(
    package_id: str,
    condition: PackageCondition = Query(
        ..., description="Package condition after inspection"
    ),
    notes: Optional[str] = Query(None, description="Inspection notes"),
):
    """Inspect a package (quality check)"""
    package = package_service.inspect_package(package_id, condition, notes)
    if not package:
        raise HTTPException(
            status_code=404, detail=f"Package with ID {package_id} not found"
        )
    return package


@router.post("/{package_id}/store", response_model=Package)
async def store_package(package_id: str, location: PackageLocation):
    """Store package in warehouse location"""
    package = package_service.store_package(package_id, location.model_dump())
    if not package:
        raise HTTPException(
            status_code=404, detail=f"Package with ID {package_id} not found"
        )
    return package


@router.post("/{package_id}/pick", response_model=Package)
async def pick_package(
    package_id: str, notes: Optional[str] = Query(None, description="Pick notes")
):
    """Pick package for delivery preparation"""
    package = package_service.pick_package(package_id, notes)
    if not package:
        raise HTTPException(
            status_code=404, detail=f"Package with ID {package_id} not found"
        )
    return package


@router.post("/{package_id}/load", response_model=Package)
async def load_package(
    package_id: str,
    vehicle_id: str = Query(..., description="Vehicle ID"),
    driver_id: str = Query(..., description="Driver ID"),
    notes: Optional[str] = Query(None, description="Loading notes"),
):
    """Load package onto vehicle for delivery"""
    package = package_service.load_package(package_id, vehicle_id, driver_id, notes)
    if not package:
        raise HTTPException(
            status_code=404, detail=f"Package with ID {package_id} not found"
        )
    return package


@router.get("/status/{status}", response_model=List[Package])
async def get_packages_by_status(status: PackageStatus):
    """Get all packages with a specific status"""
    return package_service.get_packages_by_status(status)
