from datetime import datetime
from typing import Dict, List, Optional
import uuid
from ..models.schemas import (
    Inventory,
    InventoryCreate,
    InventoryUpdate,
    InventoryStatus,
    WarehouseLocation,
)


class WMSHandler:
    """Warehouse Management Service Handler - In-memory database"""

    def __init__(self):
        self.inventory: Dict[str, dict] = {}
        self._initialize_mock_data()

    def _initialize_mock_data(self):
        """Initialize with some mock inventory"""
        mock_items = [
            {
                "sku": "PROD-001",
                "name": "Laptop Computer",
                "quantity": 50,
                "location": {
                    "warehouse_id": "WH-001",
                    "zone": "A",
                    "aisle": "12",
                    "rack": "3",
                    "bin": "B",
                },
                "unit_price": 999.99,
                "reorder_level": 10,
            },
            {
                "sku": "PROD-002",
                "name": "Wireless Mouse",
                "quantity": 200,
                "location": {
                    "warehouse_id": "WH-001",
                    "zone": "B",
                    "aisle": "5",
                    "rack": "1",
                    "bin": "A",
                },
                "unit_price": 29.99,
                "reorder_level": 50,
            },
            {
                "sku": "PROD-003",
                "name": "USB Cable",
                "quantity": 5,
                "location": {
                    "warehouse_id": "WH-002",
                    "zone": "C",
                    "aisle": "8",
                    "rack": "2",
                    "bin": "C",
                },
                "unit_price": 9.99,
                "reorder_level": 100,
            },
        ]

        for item_data in mock_items:
            item_id = str(uuid.uuid4())
            now = datetime.now().isoformat()

            # Determine status based on quantity and reorder level
            quantity = item_data["quantity"]
            reorder_level = item_data["reorder_level"]
            status = (
                InventoryStatus.OUT_OF_STOCK
                if quantity == 0
                else (
                    InventoryStatus.AVAILABLE
                    if quantity > reorder_level
                    else InventoryStatus.RESERVED
                )
            )

            self.inventory[item_id] = {
                "id": item_id,
                **item_data,
                "status": status,
                "created_at": now,
                "updated_at": now,
            }

    def get_all_inventory(self) -> List[Inventory]:
        """Get all inventory items"""
        return [Inventory(**item) for item in self.inventory.values()]

    def get_inventory_item(self, item_id: str) -> Optional[Inventory]:
        """Get inventory item by ID"""
        item = self.inventory.get(item_id)
        return Inventory(**item) if item else None

    def get_inventory_by_sku(self, sku: str) -> Optional[Inventory]:
        """Get inventory item by SKU"""
        for item in self.inventory.values():
            if item["sku"] == sku:
                return Inventory(**item)
        return None

    def create_inventory_item(self, item_data: InventoryCreate) -> Inventory:
        """Create new inventory item"""
        item_id = str(uuid.uuid4())
        now = datetime.now().isoformat()

        # Determine initial status
        status = (
            InventoryStatus.OUT_OF_STOCK
            if item_data.quantity == 0
            else InventoryStatus.AVAILABLE
        )

        item = {
            "id": item_id,
            **item_data.model_dump(),
            "status": status,
            "created_at": now,
            "updated_at": now,
        }

        self.inventory[item_id] = item
        return Inventory(**item)

    def update_inventory_item(
        self, item_id: str, item_data: InventoryUpdate
    ) -> Optional[Inventory]:
        """Update existing inventory item"""
        if item_id not in self.inventory:
            return None

        update_data = item_data.model_dump(exclude_unset=True)
        self.inventory[item_id].update(update_data)
        self.inventory[item_id]["updated_at"] = datetime.now().isoformat()

        # Auto-update status based on quantity if quantity was updated
        if "quantity" in update_data:
            quantity = self.inventory[item_id]["quantity"]
            if quantity == 0:
                self.inventory[item_id]["status"] = InventoryStatus.OUT_OF_STOCK
            elif "status" not in update_data:
                self.inventory[item_id]["status"] = InventoryStatus.AVAILABLE

        return Inventory(**self.inventory[item_id])

    def delete_inventory_item(self, item_id: str) -> bool:
        """Delete inventory item"""
        if item_id in self.inventory:
            del self.inventory[item_id]
            return True
        return False

    def check_stock_level(self, sku: str) -> dict:
        """Check if item needs reordering"""
        item = self.get_inventory_by_sku(sku)
        if not item:
            return {"error": "Item not found"}

        needs_reorder = item.quantity <= (item.reorder_level or 0)
        return {
            "sku": sku,
            "quantity": item.quantity,
            "reorder_level": item.reorder_level,
            "needs_reorder": needs_reorder,
            "status": item.status,
        }


# Singleton instance
wms_handler = WMSHandler()
