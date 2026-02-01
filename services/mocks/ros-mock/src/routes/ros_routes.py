from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models.schemas import Route, RouteCreate, RouteUpdate, ErrorResponse
from ..services.ros_service import ros_service

router = APIRouter(prefix="/api/routes", tags=["routes"])


@router.get("/", response_model=List[Route])
async def get_all_routes():
    """Get all routes"""
    return ros_service.get_all_routes()


@router.get(
    "/{route_id}", response_model=Route, responses={404: {"model": ErrorResponse}}
)
async def get_route(route_id: str):
    """Get route by ID"""
    route = ros_service.get_route(route_id)
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Route with ID {route_id} not found",
        )
    return route


@router.post("/", response_model=Route, status_code=status.HTTP_201_CREATED)
async def create_route(route: RouteCreate):
    """Create new route"""
    return ros_service.create_route(route)


@router.put(
    "/{route_id}", response_model=Route, responses={404: {"model": ErrorResponse}}
)
async def update_route(route_id: str, route: RouteUpdate):
    """Update existing route"""
    updated_route = ros_service.update_route(route_id, route)
    if not updated_route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Route with ID {route_id} not found",
        )
    return updated_route


@router.delete("/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route(route_id: str):
    """Delete route"""
    success = ros_service.delete_route(route_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Route with ID {route_id} not found",
        )
    return None


@router.post(
    "/{route_id}/optimize",
    response_model=Route,
    responses={404: {"model": ErrorResponse}},
)
async def optimize_route(route_id: str):
    """Optimize route for efficiency"""
    optimized_route = ros_service.optimize_route(route_id)
    if not optimized_route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Route with ID {route_id} not found",
        )
    return optimized_route


@router.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ROS Mock Service",
        "total_routes": len(ros_service.storage.get_all()),
    }
