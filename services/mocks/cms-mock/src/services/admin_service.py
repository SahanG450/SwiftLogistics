import uuid
from datetime import datetime
from typing import Dict, Optional, List
from pathlib import Path

from ..models.schemas import Admin, AdminCreate, AdminUpdate, AdminRole
from ..utils.file_storage import FileStorage


class AdminService:
    def __init__(self, data_dir: str = "data"):
        self.storage = FileStorage(data_dir, "admins")
    
    def get_all_admins(self) -> List[Admin]:
        """Get all admins"""
        admins_data = self.storage.get_all()
        return [Admin(**admin) for admin in admins_data.values()]
    
    def get_admin_by_id(self, admin_id: str) -> Optional[Admin]:
        """Get admin by ID"""
        admin_data = self.storage.get(admin_id)
        if admin_data:
            return Admin(**admin_data)
        return None
    
    def create_admin(self, admin_data: AdminCreate) -> Admin:
        """Create a new admin"""
        admin_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        admin = {
            "id": admin_id,
            **admin_data.model_dump(),
            "created_at": now,
            "updated_at": now
        }
        
        # Convert enum to value if present
        if "role" in admin and admin["role"]:
            admin["role"] = admin["role"].value
        
        self.storage.create(admin_id, admin)
        return Admin(**admin)
    
    def update_admin(self, admin_id: str, admin_data: AdminUpdate) -> Optional[Admin]:
        """Update an admin"""
        existing_admin = self.storage.get(admin_id)
        if not existing_admin:
            return None
        
        update_data = admin_data.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow().isoformat()
        
        # Convert enum to value if present
        if "role" in update_data and update_data["role"]:
            update_data["role"] = update_data["role"].value
        
        updated_admin = {**existing_admin, **update_data}
        self.storage.update(admin_id, updated_admin)
        
        return Admin(**updated_admin)
    
    def delete_admin(self, admin_id: str) -> bool:
        """Delete an admin"""
        return self.storage.delete(admin_id)
    
    def get_admins_by_role(self, role: AdminRole) -> List[Admin]:
        """Get admins by role"""
        all_admins = self.get_all_admins()
        return [admin for admin in all_admins if admin.role == role]
    
    def get_admin_count(self) -> int:
        """Get total number of admins"""
        return len(self.storage.get_all())
