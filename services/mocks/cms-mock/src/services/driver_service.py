import uuid
from datetime import datetime
from typing import Dict, Optional, List
from pathlib import Path

from ..models.schemas import Driver, DriverCreate, DriverUpdate, DriverStatus
from ..utils.file_storage import FileStorage


class DriverService:
    def __init__(self, data_dir: str = "data"):
        self.storage = FileStorage(data_dir, "drivers")
    
    def get_all_drivers(self) -> List[Driver]:
        """Get all drivers"""
        drivers_data = self.storage.get_all()
        return [Driver(**driver) for driver in drivers_data.values()]
    
    def get_driver_by_id(self, driver_id: str) -> Optional[Driver]:
        """Get driver by ID"""
        driver_data = self.storage.get(driver_id)
        if driver_data:
            return Driver(**driver_data)
        return None
    
    def create_driver(self, driver_data: DriverCreate) -> Driver:
        """Create a new driver"""
        driver_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        driver = {
            "id": driver_id,
            **driver_data.model_dump(),
            "status": DriverStatus.AVAILABLE.value,
            "created_at": now,
            "updated_at": now
        }
        
        self.storage.create(driver_id, driver)
        return Driver(**driver)
    
    def update_driver(self, driver_id: str, driver_data: DriverUpdate) -> Optional[Driver]:
        """Update a driver"""
        existing_driver = self.storage.get(driver_id)
        if not existing_driver:
            return None
        
        update_data = driver_data.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow().isoformat()
        
        # Convert enum to value if present
        if "status" in update_data and update_data["status"]:
            update_data["status"] = update_data["status"].value
        
        updated_driver = {**existing_driver, **update_data}
        self.storage.update(driver_id, updated_driver)
        
        return Driver(**updated_driver)
    
    def delete_driver(self, driver_id: str) -> bool:
        """Delete a driver"""
        return self.storage.delete(driver_id)
    
    def get_drivers_by_status(self, status: DriverStatus) -> List[Driver]:
        """Get drivers by status"""
        all_drivers = self.get_all_drivers()
        return [driver for driver in all_drivers if driver.status == status]
    
    def get_driver_count(self) -> int:
        """Get total number of drivers"""
        return len(self.storage.get_all())
