from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from ..models.schemas import Inventory, InventoryCreate, InventoryUpdate, ErrorResponse
from ..handlers.wms_handlers import wms_handler

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


@router.get("/", response_model=List[Inventory])
async def get_all_inventory():
    """Get all inventory items"""
    return wms_handler.get_all_inventory()


@router.get(
    "/{item_id}", response_model=Inventory, responses={404: {"model": ErrorResponse}}
)
async def get_inventory_item(item_id: str):
    """Get inventory item by ID"""
    item = wms_handler.get_inventory_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory item with ID {item_id} not found",
        )
    return item


@router.get(
    "/sku/{sku}", response_model=Inventory, responses={404: {"model": ErrorResponse}}
)
async def get_inventory_by_sku(sku: str):
    """Get inventory item by SKU"""
    item = wms_handler.get_inventory_by_sku(sku)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory item with SKU {sku} not found",
        )
    return item


@router.post("/", response_model=Inventory, status_code=status.HTTP_201_CREATED)
async def create_inventory_item(item: InventoryCreate):
    """Create new inventory item"""
    return wms_handler.create_inventory_item(item)


@router.put(
    "/{item_id}", response_model=Inventory, responses={404: {"model": ErrorResponse}}
)
async def update_inventory_item(item_id: str, item: InventoryUpdate):
    """Update existing inventory item"""
    updated_item = wms_handler.update_inventory_item(item_id, item)
    if not updated_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory item with ID {item_id} not found",
        )
    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory_item(item_id: str):
    """Delete inventory item"""
    success = wms_handler.delete_inventory_item(item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory item with ID {item_id} not found",
        )
    return None


@router.get("/check-stock/{sku}")
async def check_stock_level(sku: str):
    """Check stock level and reorder status"""
    result = wms_handler.check_stock_level(sku)
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=result["error"]
        )
    return result


@router.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "WMS Mock Service",
        "total_items": len(wms_handler.inventory),
    }
