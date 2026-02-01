import uuid
from datetime import datetime
from typing import Dict, Optional, List
from pathlib import Path

from ..models.schemas import Client, ClientCreate, ClientUpdate, MembershipLevel
from ..utils.file_storage import FileStorage


class ClientService:
    def __init__(self, data_dir: str = "data"):
        self.storage = FileStorage(data_dir, "clients")
    
    def get_all_clients(self) -> List[Client]:
        """Get all clients"""
        clients_data = self.storage.get_all()
        return [Client(**client) for client in clients_data.values()]
    
    def get_client_by_id(self, client_id: str) -> Optional[Client]:
        """Get client by ID"""
        client_data = self.storage.get(client_id)
        if client_data:
            return Client(**client_data)
        return None
    
    def create_client(self, client_data: ClientCreate) -> Client:
        """Create a new client"""
        client_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        client = {
            "id": client_id,
            **client_data.model_dump(),
            "created_at": now,
            "updated_at": now
        }
        
        # Convert enum to value if present
        if "membership_level" in client and client["membership_level"]:
            client["membership_level"] = client["membership_level"].value
        
        self.storage.create(client_id, client)
        return Client(**client)
    
    def update_client(self, client_id: str, client_data: ClientUpdate) -> Optional[Client]:
        """Update a client"""
        existing_client = self.storage.get(client_id)
        if not existing_client:
            return None
        
        update_data = client_data.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow().isoformat()
        
        # Convert enum to value if present
        if "membership_level" in update_data and update_data["membership_level"]:
            update_data["membership_level"] = update_data["membership_level"].value
        
        updated_client = {**existing_client, **update_data}
        self.storage.update(client_id, updated_client)
        
        return Client(**updated_client)
    
    def delete_client(self, client_id: str) -> bool:
        """Delete a client"""
        return self.storage.delete(client_id)
    
    def get_clients_by_membership(self, membership_level: MembershipLevel) -> List[Client]:
        """Get clients by membership level"""
        all_clients = self.get_all_clients()
        return [client for client in all_clients if client.membership_level == membership_level]
    
    def get_client_count(self) -> int:
        """Get total number of clients"""
        return len(self.storage.get_all())
