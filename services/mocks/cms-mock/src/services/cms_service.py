from datetime import datetime
from typing import Dict, List, Optional
import uuid
import os
from ..models.schemas import Customer, CustomerCreate, CustomerUpdate, CustomerStatus
from ..utils.file_storage import FileStorage


class CMSService:
    """Customer Management Service - File-based storage"""

    def __init__(self):
        # Initialize file storage
        data_dir = os.path.join(os.path.dirname(__file__), "../../data")
        self.storage = FileStorage(data_dir, "customers")
        self._initialize_mock_data()

    def _initialize_mock_data(self):
        """Initialize with some mock customers if file is empty"""
        # Only initialize if storage is empty
        if not self.storage.get_all():
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

            initial_data = {}
            for customer_data in mock_customers:
                customer_id = str(uuid.uuid4())
                now = datetime.now().isoformat()
                initial_data[customer_id] = {
                    "id": customer_id,
                    **customer_data,
                    "status": CustomerStatus.ACTIVE,
                    "created_at": now,
                    "updated_at": now,
                }

            self.storage.initialize_with_data(initial_data)

    def get_all_customers(self) -> List[Customer]:
        """Get all customers"""
        customers = self.storage.get_all()
        return [Customer(**customer) for customer in customers.values()]

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID"""
        customer = self.storage.get(customer_id)
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

        self.storage.create(customer_id, customer)
        return Customer(**customer)

    def update_customer(
        self, customer_id: str, customer_data: CustomerUpdate
    ) -> Optional[Customer]:
        """Update existing customer"""
        customer = self.storage.get(customer_id)
        if not customer:
            return None

        update_data = customer_data.model_dump(exclude_unset=True)
        customer.update(update_data)
        customer["updated_at"] = datetime.now().isoformat()

        self.storage.update(customer_id, customer)
        return Customer(**customer)

    def delete_customer(self, customer_id: str) -> bool:
        """Delete customer"""
        return self.storage.delete(customer_id)


# Singleton instance
cms_service = CMSService()
