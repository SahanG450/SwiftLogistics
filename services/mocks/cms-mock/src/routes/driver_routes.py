from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional

from ..models.schemas import Driver, DriverCreate, DriverUpdate, DriverStatus, ErrorResponse
from ..services.driver_service import DriverService

router = APIRouter(prefix="/drivers", tags=["drivers"])
driver_service = DriverService()


@router.get("/", response_model=List[Driver])
async def get_all_drivers(
    status: Optional[DriverStatus] = Query(None, description="Filter drivers by status")
):
    """Get all drivers, optionally filtered by status"""
    if status:
        return driver_service.get_drivers_by_status(status)
    return driver_service.get_all_drivers()


@router.get("/{driver_id}", response_model=Driver, responses={404: {"model": ErrorResponse}})
async def get_driver(driver_id: str):
    """Get a specific driver by ID"""
    driver = driver_service.get_driver_by_id(driver_id)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver with id {driver_id} not found"
        )
    return driver


@router.post("/", response_model=Driver, status_code=status.HTTP_201_CREATED)
async def create_driver(driver: DriverCreate):
    """Create a new driver"""
    return driver_service.create_driver(driver)


@router.put("/{driver_id}", response_model=Driver, responses={404: {"model": ErrorResponse}})
async def update_driver(driver_id: str, driver: DriverUpdate):
    """Update a driver"""
    updated_driver = driver_service.update_driver(driver_id, driver)
    if not updated_driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver with id {driver_id} not found"
        )
    return updated_driver


@router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_driver(driver_id: str):
    """Delete a driver"""
    deleted = driver_service.delete_driver(driver_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver with id {driver_id} not found"
        )
    return None
