from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from ..models.schemas import Order, OrderCreate, OrderUpdate, OrderStatus, ProofOfDelivery, DeliveryFailureReason
from ..services.order_service import OrderService

router = APIRouter(prefix="/api/orders", tags=["Orders"])
order_service = OrderService()


@router.get("/", response_model=List[Order])
async def get_all_orders(
    status: Optional[OrderStatus] = Query(None, description="Filter by order status"),
    client_id: Optional[str] = Query(None, description="Filter by client ID"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    driver_id: Optional[str] = Query(None, description="Filter by assigned driver ID"),
):
    """Get all orders with optional filtering"""
    return order_service.get_all_orders(
        status=status, client_id=client_id, priority=priority, driver_id=driver_id
    )


@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: str):
    """Get a specific order by ID"""
    order = order_service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")
    return order


@router.post("/", response_model=Order, status_code=201)
async def create_order(order: OrderCreate):
    """Create a new order (Order Intake from Client Portal)"""
    return order_service.create_order(order)


@router.put("/{order_id}", response_model=Order)
async def update_order(order_id: str, order: OrderUpdate):
    """Update an existing order"""
    updated_order = order_service.update_order(order_id, order)
    if not updated_order:
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")
    return updated_order


@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: str):
    """Delete an order"""
    if not order_service.delete_order(order_id):
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")


@router.post("/{order_id}/assign-driver", response_model=Order)
async def assign_driver(
    order_id: str,
    driver_id: str = Query(..., description="Driver ID to assign"),
    route_id: Optional[str] = Query(None, description="Route ID (optional)"),
):
    """Assign an order to a driver (and optionally a route)"""
    order = order_service.assign_to_driver(order_id, driver_id, route_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")
    return order


@router.post("/{order_id}/mark-delivered", response_model=Order)
async def mark_delivered(order_id: str, proof: ProofOfDelivery):
    """Mark an order as delivered with proof of delivery"""
    order = order_service.mark_as_delivered(order_id, proof.model_dump())
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")
    return order


@router.post("/{order_id}/mark-failed", response_model=Order)
async def mark_failed(
    order_id: str,
    reason: DeliveryFailureReason = Query(..., description="Failure reason"),
    notes: Optional[str] = Query(None, description="Additional notes"),
):
    """Mark an order as failed with reason"""
    order = order_service.mark_as_failed(order_id, reason, notes)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")
    return order


@router.get("/status/{status}", response_model=List[Order])
async def get_orders_by_status(status: OrderStatus):
    """Get all orders with a specific status"""
    return order_service.get_orders_by_status(status)
