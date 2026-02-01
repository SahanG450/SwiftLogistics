from typing import List, Optional
from datetime import datetime
import uuid

from ..utils.file_storage import FileStorage
from ..models.schemas import (
    Package,
    PackageCreate,
    PackageUpdate,
    PackageStatus,
    PackageCondition,
    PackageEvent,
)


class PackageService:
    def __init__(self):
        self.storage = FileStorage(data_dir="data", filename="packages")
        self._init_mock_data()
        self.tracking_counter = self._get_next_tracking_number()

    def _get_next_tracking_number(self) -> int:
        """Get the next tracking number"""
        packages = self.storage.get_all()
        if not packages:
            return 100001

        max_num = 100001
        for package in packages.values():
            try:
                tracking = package.get("tracking_number", "")
                if tracking.startswith("SL"):
                    num = int(tracking.replace("SL", ""))
                    max_num = max(max_num, num)
            except (ValueError, IndexError):
                pass
        return max_num + 1

    def _generate_tracking_number(self) -> str:
        """Generate tracking number: SLNNNNNN"""
        tracking_num = f"SL{self.tracking_counter:06d}"
        self.tracking_counter += 1
        return tracking_num

    def _add_event(
        self, events: List[dict], event_type: str, notes: Optional[str] = None
    ) -> List[dict]:
        """Add an event to package history"""
        event = {
            "event_type": event_type,
            "timestamp": datetime.now().isoformat(),
            "location": None,
            "performed_by": "system",
            "notes": notes,
        }
        events.append(event)
        return events

    def _init_mock_data(self):
        """Initialize with sample packages"""
        if not self.storage.get_all():
            # Package 1 - Ready for delivery
            pkg1_id = str(uuid.uuid4())
            pkg1 = {
                "id": pkg1_id,
                "tracking_number": "SL100001",
                "order_id": "order-001",
                "client_id": "client-001",
                "description": "Samsung Galaxy S24 - Fragile Electronics",
                "status": "stored",
                "condition": "good",
                "location": {
                    "warehouse_id": "WH-MAIN-01",
                    "zone": "A",
                    "aisle": "12",
                    "rack": "R5",
                    "shelf": "S3",
                    "bin": "B02",
                },
                "weight": 0.5,
                "dimensions": "15x8x2 cm",
                "special_handling": "Fragile - Handle with care",
                "assigned_vehicle_id": None,
                "assigned_driver_id": None,
                "received_at": "2026-02-01T08:30:00.000000",
                "loaded_at": None,
                "delivered_at": None,
                "events": [
                    {
                        "event_type": "received",
                        "timestamp": "2026-02-01T08:30:00.000000",
                        "location": "Receiving Dock A",
                        "performed_by": "WH-STAFF-01",
                        "notes": "Package received from Daraz Lanka",
                    },
                    {
                        "event_type": "inspected",
                        "timestamp": "2026-02-01T08:45:00.000000",
                        "location": "Inspection Area",
                        "performed_by": "QC-STAFF-02",
                        "notes": "Quality check passed - good condition",
                    },
                    {
                        "event_type": "stored",
                        "timestamp": "2026-02-01T09:15:00.000000",
                        "location": "ZONE-A-R5-S3-B02",
                        "performed_by": "WH-STAFF-03",
                        "notes": "Stored in warehouse location",
                    },
                ],
                "notes": None,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }

            # Package 2 - Just received
            pkg2_id = str(uuid.uuid4())
            pkg2 = {
                "id": pkg2_id,
                "tracking_number": "SL100002",
                "order_id": "order-002",
                "client_id": "client-002",
                "description": "Avurudu Gift Basket x2",
                "status": "received",
                "condition": "good",
                "location": None,
                "weight": 3.5,
                "dimensions": "40x30x25 cm",
                "special_handling": "Contains perishable items",
                "assigned_vehicle_id": None,
                "assigned_driver_id": None,
                "received_at": "2026-02-01T10:00:00.000000",
                "loaded_at": None,
                "delivered_at": None,
                "events": [
                    {
                        "event_type": "received",
                        "timestamp": "2026-02-01T10:00:00.000000",
                        "location": "Receiving Dock B",
                        "performed_by": "WH-STAFF-04",
                        "notes": "Package received from Kapruka.com",
                    }
                ],
                "notes": "Priority delivery for Avurudu",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }

            self.storage.create(pkg1_id, pkg1)
            self.storage.create(pkg2_id, pkg2)

    def create_package(self, package_data: PackageCreate) -> Package:
        """Create a new package (receive from client)"""
        package_id = str(uuid.uuid4())
        tracking_number = (
            package_data.tracking_number or self._generate_tracking_number()
        )

        now = datetime.now().isoformat()

        # Initial event
        events = [
            {
                "event_type": "received",
                "timestamp": now,
                "location": "Receiving Dock",
                "performed_by": "system",
                "notes": f"Package received from client {package_data.client_id}",
            }
        ]

        package_dict = {
            "id": package_id,
            "tracking_number": tracking_number,
            **package_data.model_dump(exclude={"tracking_number"}),
            "status": PackageStatus.RECEIVED,
            "condition": PackageCondition.GOOD,
            "location": None,
            "assigned_vehicle_id": None,
            "assigned_driver_id": None,
            "received_at": now,
            "loaded_at": None,
            "delivered_at": None,
            "events": events,
            "notes": None,
            "created_at": now,
            "updated_at": now,
        }

        self.storage.create(package_id, package_dict)
        return Package(**package_dict)

    def get_package(self, package_id: str) -> Optional[Package]:
        """Get a specific package by ID"""
        package_data = self.storage.get(package_id)
        if package_data:
            return Package(**package_data)
        return None

    def get_package_by_tracking(self, tracking_number: str) -> Optional[Package]:
        """Get a package by tracking number"""
        packages = self.storage.get_all()
        for package in packages.values():
            if package.get("tracking_number") == tracking_number:
                return Package(**package)
        return None

    def get_all_packages(
        self,
        status: Optional[PackageStatus] = None,
        client_id: Optional[str] = None,
        order_id: Optional[str] = None,
    ) -> List[Package]:
        """Get all packages with optional filtering"""
        packages = self.storage.get_all()
        package_list = [Package(**pkg) for pkg in packages.values()]

        if status:
            package_list = [p for p in package_list if p.status == status]
        if client_id:
            package_list = [p for p in package_list if p.client_id == client_id]
        if order_id:
            package_list = [p for p in package_list if p.order_id == order_id]

        return package_list

    def update_package(
        self, package_id: str, package_update: PackageUpdate
    ) -> Optional[Package]:
        """Update a package"""
        existing_package = self.storage.get(package_id)
        if not existing_package:
            return None

        update_data = package_update.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.now().isoformat()

        # Add event if status changed
        if "status" in update_data:
            events = existing_package.get("events", [])
            events = self._add_event(
                events, update_data["status"], update_data.get("notes")
            )
            update_data["events"] = events

        updated_package = {**existing_package, **update_data}
        self.storage.update(package_id, updated_package)

        return Package(**updated_package)

    def delete_package(self, package_id: str) -> bool:
        """Delete a package"""
        return self.storage.delete(package_id)

    def inspect_package(
        self, package_id: str, condition: PackageCondition, notes: Optional[str] = None
    ) -> Optional[Package]:
        """Mark package as inspected"""
        update = PackageUpdate(
            status=PackageStatus.INSPECTED, condition=condition, notes=notes
        )
        return self.update_package(package_id, update)

    def store_package(
        self, package_id: str, location: dict, notes: Optional[str] = None
    ) -> Optional[Package]:
        """Store package in warehouse location"""
        update = PackageUpdate(
            status=PackageStatus.STORED, location=location, notes=notes
        )
        return self.update_package(package_id, update)

    def pick_package(
        self, package_id: str, notes: Optional[str] = None
    ) -> Optional[Package]:
        """Pick package for delivery preparation"""
        update = PackageUpdate(status=PackageStatus.PICKED, notes=notes)
        return self.update_package(package_id, update)

    def load_package(
        self,
        package_id: str,
        vehicle_id: str,
        driver_id: str,
        notes: Optional[str] = None,
    ) -> Optional[Package]:
        """Load package onto vehicle"""
        now = datetime.now().isoformat()

        existing = self.storage.get(package_id)
        if not existing:
            return None

        existing["status"] = PackageStatus.LOADED
        existing["assigned_vehicle_id"] = vehicle_id
        existing["assigned_driver_id"] = driver_id
        existing["loaded_at"] = now
        existing["updated_at"] = now

        # Add event
        events = existing.get("events", [])
        events = self._add_event(
            events, "loaded", notes or f"Loaded to vehicle {vehicle_id}"
        )
        existing["events"] = events

        self.storage.update(package_id, existing)
        return Package(**existing)

    def get_packages_by_status(self, status: PackageStatus) -> List[Package]:
        """Get packages by status"""
        return self.get_all_packages(status=status)
