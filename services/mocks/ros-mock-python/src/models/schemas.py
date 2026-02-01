from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class RouteStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Coordinates(BaseModel):
    latitude: float
    longitude: float


class RouteStop(BaseModel):
    location: str
    coordinates: Optional[Coordinates] = None
    estimated_arrival: Optional[str] = None
    actual_arrival: Optional[str] = None


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
