"""Driver-related routes."""

from fastapi import APIRouter, Depends
import sys

sys.path.append('/app')
from common.auth import get_current_user

router = APIRouter()

@router.get("/location")
async def get_driver_location(current_user: dict = Depends(get_current_user)):
    """Get driver location (placeholder)."""
    return {
        "driverId": current_user["userId"],
        "location": {"lat": 6.9271, "lng": 79.8612},
        "status": "available"
    }

@router.get("/status")
async def get_driver_status(current_user: dict = Depends(get_current_user)):
    """Get driver status (placeholder)."""
    return {
        "driverId": current_user["userId"],
        "status": "active",
        "currentOrders": []
    }
