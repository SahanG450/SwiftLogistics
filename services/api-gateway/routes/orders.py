"""Order management routes."""

from fastapi import APIRouter, Depends, HTTPException, status
import httpx
import os
import sys

sys.path.append('/app')
from common.models import OrderCreateRequest, OrderResponse
from common.auth import get_current_user
from loguru import logger

router = APIRouter()

ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://orchestrator:3001")

@router.post("", response_model=OrderResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_order(
    order: OrderCreateRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new order.
    
    Requires authentication.
    """
    try:
        # Add user info to order
        order_data = order.dict()
        order_data["customerId"] = current_user["userId"]
        
        # Forward to orchestrator
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ORCHESTRATOR_URL}/api/orders",
                json=order_data,
                timeout=30.0
            )
            
            if response.status_code in [200, 202]:
                result = response.json()
                logger.info(f"Order created: {result['orderId']} by user {current_user['email']}")
                return OrderResponse(**result)
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to create order"
                )
    
    except httpx.TimeoutException:
        logger.error("Orchestrator service timeout")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Order service temporarily unavailable"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Order creation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order"
        )

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get order details by ID."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{ORCHESTRATOR_URL}/api/orders/{order_id}",
                timeout=10.0
            )
            
            if response.status_code == 200:
                return OrderResponse(**response.json())
            elif response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to retrieve order"
                )
    
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve order"
        )
