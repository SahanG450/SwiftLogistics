from datetime import datetime
from typing import Dict, List, Optional
import uuid
from ..models.schemas import Customer, CustomerCreate, CustomerUpdate, CustomerStatus


class CMSService:
    """Customer Management Service - In-memory database"""

    def __init__(self):
        self.customers: Dict[str, dict] = {}
        self._initialize_mock_data()

    def _initialize_mock_data(self):
        """Initialize with some mock customers"""
        mock_customers = [
            {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1-555-0101",
                "address": "123 Main St, New York, NY 10001",
                "company": "Tech Corp",
            },
            {
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "phone": "+1-555-0102",
                "address": "456 Oak Ave, Los Angeles, CA 90001",
                "company": "Retail Inc",
            },
        ]

        for customer_data in mock_customers:
            customer_id = str(uuid.uuid4())
            now = datetime.now().isoformat()
            self.customers[customer_id] = {
                "id": customer_id,
                **customer_data,
                "status": CustomerStatus.ACTIVE,
                "created_at": now,
                "updated_at": now,
            }

    def get_all_customers(self) -> List[Customer]:
        """Get all customers"""
        return [Customer(**customer) for customer in self.customers.values()]

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID"""
        customer = self.customers.get(customer_id)
        return Customer(**customer) if customer else None

    def create_customer(self, customer_data: CustomerCreate) -> Customer:
        """Create new customer"""
        customer_id = str(uuid.uuid4())
        now = datetime.now().isoformat()

        customer = {
            "id": customer_id,
            **customer_data.model_dump(),
            "status": CustomerStatus.ACTIVE,
            "created_at": now,
            "updated_at": now,
        }

        self.customers[customer_id] = customer
        return Customer(**customer)

    def update_customer(
        self, customer_id: str, customer_data: CustomerUpdate
    ) -> Optional[Customer]:
        """Update existing customer"""
        if customer_id not in self.customers:
            return None

        update_data = customer_data.model_dump(exclude_unset=True)
        self.customers[customer_id].update(update_data)
        self.customers[customer_id]["updated_at"] = datetime.now().isoformat()

        return Customer(**self.customers[customer_id])

    def delete_customer(self, customer_id: str) -> bool:
        """Delete customer"""
        if customer_id in self.customers:
            del self.customers[customer_id]
            return True
        return False


# Singleton instance
cms_service = CMSService()
