"""Order routes."""

from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import sys

sys.path.append('/app')
from common.models import OrderCreateRequest, OrderResponse
from models.order import Order
from services.order_manager import create_order_id
from services.message_queue import message_queue
from loguru import logger

router = APIRouter()

@router.post("", response_model=OrderResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_order(order_request: OrderCreateRequest):
    """Create a new order."""
    try:
        # Generate order ID
        order_id = create_order_id()
        
        # Create order document
        order = Order(
            orderId=order_id,
            customerId=order_request.dict().get("customerId", "unknown"),
            pickupLocation=order_request.pickupLocation.dict(),
            deliveryAddress=order_request.deliveryAddress.dict(),
            packageDetails=order_request.packageDetails.dict(),
            scheduledPickupTime=order_request.scheduledPickupTime,
            specialInstructions=order_request.specialInstructions,
            status="RECEIVED",
            createdAt=datetime.utcnow()
        )
        
        # Save to database
        await order.insert()
        
        logger.info(f"Order created: {order_id}")
        
        # Publish to RabbitMQ
        message_queue.publish(
            exchange_name='order_exchange',
            message={
                "orderId": order_id,
                "customerId": order.customerId,
                "pickupLocation": order.pickupLocation,
                "deliveryAddress": order.deliveryAddress,
                "packageDetails": order.packageDetails,
                "timestamp": order.createdAt.isoformat()
            }
        )
        
        logger.info(f"Order published to queue: {order_id}")
        
        # Publish event
        message_queue.publish(
            exchange_name='events_exchange',
            message={
                "type": "ORDER_CREATED",
                "data": {
                    "orderId": order_id,
                    "status": "RECEIVED",
                    "message": "Order received and being processed"
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        return OrderResponse(
            orderId=order_id,
            status="RECEIVED",
            message="Order received and being processed",
            customerId=order.customerId,
            createdAt=order.createdAt
        )
    
    except Exception as e:
        logger.error(f"Failed to create order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order"
        )

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    """Get order by ID."""
    order = await Order.find_one(Order.orderId == order_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return OrderResponse(
        orderId=order.orderId,
        status=order.status,
        customerId=order.customerId,
        createdAt=order.createdAt
    )
