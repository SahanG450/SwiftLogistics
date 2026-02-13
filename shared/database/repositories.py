"""
Repository implementations for SwiftLogistics entities
"""
from typing import Optional, List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from .base_repository import BaseRepository
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class OrderRepository(BaseRepository):
    """Repository for Order operations"""
    
    def __init__(self, database: AsyncIOMotorDatabase):
        super().__init__(database, "orders")
    
    async def find_by_order_id(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Find order by order_id"""
        return await self.find_one({"order_id": order_id})
    
    async def find_by_client(self, client_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Find all orders for a specific client"""
        return await self.find_many(
            {"client_id": client_id},
            skip=skip,
            limit=limit,
            sort=[("created_at", -1)]
        )
    
    async def find_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Find orders by status"""
        return await self.find_many(
            {"status": status},
            skip=skip,
            limit=limit,
            sort=[("created_at", -1)]
        )
    
    async def update_status(self, order_id: str, new_status: str) -> bool:
        """Update order status"""
        return await self.update_one(
            {"order_id": order_id},
            {"status": new_status, "status_updated_at": datetime.utcnow()}
        )


class DriverRepository(BaseRepository):
    """Repository for Driver operations"""
    
    def __init__(self, database: AsyncIOMotorDatabase):
        super().__init__(database, "drivers")
    
    async def find_by_driver_id(self, driver_id: str) -> Optional[Dict[str, Any]]:
        """Find driver by driver_id"""
        return await self.find_one({"driver_id": driver_id})
    
    async def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Find driver by email"""
        return await self.find_one({"email": email})
    
    async def find_available_drivers(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Find all available drivers"""
        return await self.find_many(
            {"status": "available"},
            limit=limit
        )
    
    async def update_status(self, driver_id: str, status: str) -> bool:
        """Update driver status"""
        return await self.update_one(
            {"driver_id": driver_id},
            {"status": status}
        )


class ClientRepository(BaseRepository):
    """Repository for Client operations"""
    
    def __init__(self, database: AsyncIOMotorDatabase):
        super().__init__(database, "clients")
    
    async def find_by_client_id(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Find client by client_id"""
        return await self.find_one({"client_id": client_id})
    
    async def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Find client by email"""
        return await self.find_one({"email": email})
    
    async def find_active_clients(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Find all active clients"""
        return await self.find_many(
            {"status": "active"},
            skip=skip,
            limit=limit
        )


class ShipmentRepository(BaseRepository):
    """Repository for Shipment operations"""
    
    def __init__(self, database: AsyncIOMotorDatabase):
        super().__init__(database, "shipments")
    
    async def find_by_shipment_id(self, shipment_id: str) -> Optional[Dict[str, Any]]:
        """Find shipment by shipment_id"""
        return await self.find_one({"shipment_id": shipment_id})
    
    async def find_by_order(self, order_id: str) -> List[Dict[str, Any]]:
        """Find all shipments for an order"""
        return await self.find_many({"order_id": order_id})
    
    async def find_by_driver(self, driver_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Find all shipments for a driver"""
        return await self.find_many(
            {"driver_id": driver_id},
            skip=skip,
            limit=limit,
            sort=[("created_at", -1)]
        )
    
    async def update_location(self, shipment_id: str, location: Dict[str, float]) -> bool:
        """Update shipment location"""
        return await self.update_one(
            {"shipment_id": shipment_id},
            {
                "current_location": location,
                "location_updated_at": datetime.utcnow()
            }
        )
    
    async def update_status(self, shipment_id: str, status: str) -> bool:
        """Update shipment status"""
        return await self.update_one(
            {"shipment_id": shipment_id},
            {"status": status, "status_updated_at": datetime.utcnow()}
        )


class ContractRepository(BaseRepository):
    """Repository for Contract operations"""
    
    def __init__(self, database: AsyncIOMotorDatabase):
        super().__init__(database, "contracts")
    
    async def find_by_contract_id(self, contract_id: str) -> Optional[Dict[str, Any]]:
        """Find contract by contract_id"""
        return await self.find_one({"contract_id": contract_id})
    
    async def find_by_client(self, client_id: str) -> List[Dict[str, Any]]:
        """Find all contracts for a client"""
        return await self.find_many(
            {"client_id": client_id},
            sort=[("created_at", -1)]
        )
    
    async def find_active_contracts(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Find all active contracts"""
        return await self.find_many(
            {"status": "active"},
            skip=skip,
            limit=limit
        )


class InvoiceRepository(BaseRepository):
    """Repository for Invoice operations"""
    
    def __init__(self, database: AsyncIOMotorDatabase):
        super().__init__(database, "invoices")
    
    async def find_by_invoice_id(self, invoice_id: str) -> Optional[Dict[str, Any]]:
        """Find invoice by invoice_id"""
        return await self.find_one({"invoice_id": invoice_id})
    
    async def find_by_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Find invoice for an order"""
        return await self.find_one({"order_id": order_id})
    
    async def find_by_client(self, client_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Find all invoices for a client"""
        return await self.find_many(
            {"client_id": client_id},
            skip=skip,
            limit=limit,
            sort=[("created_at", -1)]
        )
    
    async def find_unpaid_invoices(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Find all unpaid invoices"""
        return await self.find_many(
            {"payment_status": "unpaid"},
            skip=skip,
            limit=limit,
            sort=[("created_at", -1)]
        )
    
    async def update_payment_status(self, invoice_id: str, payment_status: str) -> bool:
        """Update invoice payment status"""
        return await self.update_one(
            {"invoice_id": invoice_id},
            {"payment_status": payment_status, "payment_updated_at": datetime.utcnow()}
        )


class AdminRepository(BaseRepository):
    """Repository for Admin/User operations"""
    
    def __init__(self, database: AsyncIOMotorDatabase):
        super().__init__(database, "admins")
    
    async def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Find admin by email"""
        return await self.find_one({"email": email})
    
    async def find_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Find admin by username"""
        return await self.find_one({"username": username})
