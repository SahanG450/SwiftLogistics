from typing import List, Optional
from datetime import datetime
import uuid

from ..utils.file_storage import FileStorage
from ..models.schemas import Order, OrderCreate, OrderUpdate, OrderStatus


class OrderService:
    def __init__(self):
        self.storage = FileStorage(data_dir="data", filename="orders")
        self._init_mock_data()
        self.order_counter = self._get_next_order_number()

    def _get_next_order_number(self) -> int:
        """Get the next order number based on existing orders"""
        orders = self.storage.get_all()
        if not orders:
            return 1000

        # Extract numbers from existing order numbers (format: ORD-YYYY-NNNN)
        max_num = 1000
        for order in orders.values():
            try:
                parts = order.get("order_number", "").split("-")
                if len(parts) == 3:
                    num = int(parts[2])
                    max_num = max(max_num, num)
            except (ValueError, IndexError):
                pass
        return max_num + 1

    def _generate_order_number(self) -> str:
        """Generate a human-readable order number: ORD-YYYY-NNNN"""
        year = datetime.now().year
        order_num = f"ORD-{year}-{self.order_counter:04d}"
        self.order_counter += 1
        return order_num

    def _init_mock_data(self):
        """Initialize with sample orders if storage is empty"""
        if not self.storage.get_all():
            # Sample order 1
            order1_id = str(uuid.uuid4())
            order1 = {
                "id": order1_id,
                "order_number": "ORD-2026-1001",
                "client_id": "client-001",
                "client_name": "Daraz Lanka",
                "delivery_address": {
                    "street": "No. 45, Galle Road",
                    "city": "Colombo",
                    "postal_code": "00300",
                    "province": "Western",
                    "country": "Sri Lanka",
                    "contact_name": "Nimal Perera",
                    "contact_phone": "+94771234567",
                },
                "items": [
                    {
                        "sku": "PHONE-001",
                        "description": "Samsung Galaxy S24",
                        "quantity": 1,
                        "weight": 0.5,
                        "value": 185000.0,
                    }
                ],
                "status": "ready_for_delivery",
                "priority": "normal",
                "assigned_driver_id": None,
                "assigned_route_id": None,
                "warehouse_location": "ZONE-A-RACK-12",
                "scheduled_date": "2026-02-02",
                "special_instructions": "Fragile - Handle with care",
                "failure_reason": None,
                "failure_notes": None,
                "proof_of_delivery": None,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }

            # Sample order 2
            order2_id = str(uuid.uuid4())
            order2 = {
                "id": order2_id,
                "order_number": "ORD-2026-1002",
                "client_id": "client-002",
                "client_name": "Kapruka.com",
                "delivery_address": {
                    "street": "123, Main Street, Kandy",
                    "city": "Kandy",
                    "postal_code": "20000",
                    "province": "Central",
                    "country": "Sri Lanka",
                    "contact_name": "Sunil Fernando",
                    "contact_phone": "+94712345678",
                },
                "items": [
                    {
                        "sku": "GIFT-BASKET-01",
                        "description": "Avurudu Gift Basket",
                        "quantity": 2,
                        "weight": 3.5,
                        "value": 8500.0,
                    }
                ],
                "status": "pending",
                "priority": "high",
                "assigned_driver_id": None,
                "assigned_route_id": None,
                "warehouse_location": None,
                "scheduled_date": "2026-04-13",
                "special_instructions": "Avurudu special delivery - Must arrive before April 13",
                "failure_reason": None,
                "failure_notes": None,
                "proof_of_delivery": None,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }

            self.storage.create(order1_id, order1)
            self.storage.create(order2_id, order2)

    def create_order(self, order_data: OrderCreate) -> Order:
        """Create a new order"""
        order_id = str(uuid.uuid4())
        order_number = self._generate_order_number()

        now = datetime.now().isoformat()
        order_dict = {
            "id": order_id,
            "order_number": order_number,
            **order_data.model_dump(),
            "status": OrderStatus.PENDING,
            "assigned_driver_id": None,
            "assigned_route_id": None,
            "warehouse_location": None,
            "failure_reason": None,
            "failure_notes": None,
            "proof_of_delivery": None,
            "created_at": now,
            "updated_at": now,
        }

        self.storage.create(order_id, order_dict)
        return Order(**order_dict)

    def get_order(self, order_id: str) -> Optional[Order]:
        """Get a specific order by ID"""
        order_data = self.storage.get(order_id)
        if order_data:
            return Order(**order_data)
        return None

    def get_all_orders(
        self,
        status: Optional[OrderStatus] = None,
        client_id: Optional[str] = None,
        priority: Optional[str] = None,
        driver_id: Optional[str] = None,
    ) -> List[Order]:
        """Get all orders with optional filtering"""
        orders = self.storage.get_all()
        order_list = [Order(**order) for order in orders.values()]

        # Apply filters
        if status:
            order_list = [o for o in order_list if o.status == status]
        if client_id:
            order_list = [o for o in order_list if o.client_id == client_id]
        if priority:
            order_list = [o for o in order_list if o.priority == priority]
        if driver_id:
            order_list = [o for o in order_list if o.assigned_driver_id == driver_id]

        return order_list

    def update_order(self, order_id: str, order_update: OrderUpdate) -> Optional[Order]:
        """Update an existing order"""
        existing_order = self.storage.get(order_id)
        if not existing_order:
            return None

        update_data = order_update.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.now().isoformat()

        updated_order = {**existing_order, **update_data}
        self.storage.update(order_id, updated_order)

        return Order(**updated_order)

    def delete_order(self, order_id: str) -> bool:
        """Delete an order"""
        return self.storage.delete(order_id)

    def get_orders_by_status(self, status: OrderStatus) -> List[Order]:
        """Get orders by status - helper method"""
        return self.get_all_orders(status=status)

    def mark_as_delivered(
        self, order_id: str, proof_of_delivery: dict
    ) -> Optional[Order]:
        """Mark order as delivered with proof"""
        update = OrderUpdate(
            status=OrderStatus.DELIVERED, proof_of_delivery=proof_of_delivery
        )
        return self.update_order(order_id, update)

    def mark_as_failed(
        self, order_id: str, failure_reason: str, failure_notes: Optional[str] = None
    ) -> Optional[Order]:
        """Mark order as failed with reason"""
        update = OrderUpdate(
            status=OrderStatus.FAILED,
            failure_reason=failure_reason,
            failure_notes=failure_notes,
        )
        return self.update_order(order_id, update)

    def assign_to_driver(
        self, order_id: str, driver_id: str, route_id: Optional[str] = None
    ) -> Optional[Order]:
        """Assign order to a driver and optionally a route"""
        update = OrderUpdate(
            assigned_driver_id=driver_id,
            assigned_route_id=route_id,
            status=OrderStatus.OUT_FOR_DELIVERY,
        )
        return self.update_order(order_id, update)
