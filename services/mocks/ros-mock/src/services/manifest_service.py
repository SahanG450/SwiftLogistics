from typing import List, Optional
from datetime import datetime
import uuid

from ..utils.file_storage import FileStorage
from ..models.schemas import (
    DeliveryManifest,
    ManifestCreate,
    ManifestUpdate,
    ManifestStatus,
)


class ManifestService:
    def __init__(self):
        self.storage = FileStorage(data_dir="data", filename="manifests")
        self._init_mock_data()
        self.manifest_counter = self._get_next_manifest_number()

    def _get_next_manifest_number(self) -> int:
        """Get the next manifest number"""
        manifests = self.storage.get_all()
        if not manifests:
            return 2001

        max_num = 2001
        for manifest in manifests.values():
            try:
                parts = manifest.get("manifest_number", "").split("-")
                if len(parts) == 3:
                    num = int(parts[2])
                    max_num = max(max_num, num)
            except (ValueError, IndexError):
                pass
        return max_num + 1

    def _generate_manifest_number(self) -> str:
        """Generate manifest number: MAN-YYYY-NNNN"""
        year = datetime.now().year
        manifest_num = f"MAN-{year}-{self.manifest_counter:04d}"
        self.manifest_counter += 1
        return manifest_num

    def _init_mock_data(self):
        """Initialize with sample delivery manifests"""
        if not self.storage.get_all():
            # Manifest 1 - Today's deliveries
            manifest1_id = str(uuid.uuid4())
            manifest1 = {
                "id": manifest1_id,
                "manifest_number": "MAN-2026-2001",
                "driver_id": "driver-001",
                "driver_name": "Samantha Perera",
                "vehicle_id": "VEH-101",
                "route_id": "route-001",
                "deliveries": [
                    {
                        "order_id": "order-001",
                        "package_id": "pkg-001",
                        "tracking_number": "SL100001",
                        "recipient_name": "Nimal Perera",
                        "delivery_address": "No. 45, Galle Road, Colombo 03",
                        "contact_phone": "+94771234567",
                        "coordinates": {"latitude": 6.9271, "longitude": 79.8612},
                        "priority": "normal",
                        "special_instructions": "Fragile - Handle with care",
                        "estimated_delivery_time": "2026-02-02T10:30:00",
                        "status": "pending"
                    },
                    {
                        "order_id": "order-003",
                        "package_id": "pkg-003",
                        "tracking_number": "SL100003",
                        "recipient_name": "Kamala Silva",
                        "delivery_address": "78, Duplication Road, Colombo 04",
                        "contact_phone": "+94772345678",
                        "coordinates": {"latitude": 6.8935, "longitude": 79.8564},
                        "priority": "high",
                        "special_instructions": None,
                        "estimated_delivery_time": "2026-02-02T11:15:00",
                        "status": "pending"
                    }
                ],
                "delivery_date": "2026-02-02",
                "status": "assigned",
                "total_deliveries": 2,
                "completed_deliveries": 0,
                "failed_deliveries": 0,
                "started_at": None,
                "completed_at": None,
                "notes": "Colombo zone - Morning shift",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }

            self.storage.create(manifest1_id, manifest1)

    def create_manifest(self, manifest_data: ManifestCreate) -> DeliveryManifest:
        """Create a new delivery manifest"""
        manifest_id = str(uuid.uuid4())
        manifest_number = self._generate_manifest_number()

        now = datetime.now().isoformat()
        manifest_dict = {
            "id": manifest_id,
            "manifest_number": manifest_number,
            **manifest_data.model_dump(),
            "status": ManifestStatus.DRAFT,
            "total_deliveries": len(manifest_data.deliveries),
            "completed_deliveries": 0,
            "failed_deliveries": 0,
            "started_at": None,
            "completed_at": None,
            "notes": None,
            "created_at": now,
            "updated_at": now,
        }

        self.storage.create(manifest_id, manifest_dict)
        return DeliveryManifest(**manifest_dict)

    def get_manifest(self, manifest_id: str) -> Optional[DeliveryManifest]:
        """Get a specific manifest by ID"""
        manifest_data = self.storage.get(manifest_id)
        if manifest_data:
            return DeliveryManifest(**manifest_data)
        return None

    def get_all_manifests(
        self,
        driver_id: Optional[str] = None,
        status: Optional[ManifestStatus] = None,
        delivery_date: Optional[str] = None,
    ) -> List[DeliveryManifest]:
        """Get all manifests with optional filtering"""
        manifests = self.storage.get_all()
        manifest_list = [DeliveryManifest(**m) for m in manifests.values()]

        if driver_id:
            manifest_list = [m for m in manifest_list if m.driver_id == driver_id]
        if status:
            manifest_list = [m for m in manifest_list if m.status == status]
        if delivery_date:
            manifest_list = [m for m in manifest_list if m.delivery_date == delivery_date]

        return manifest_list

    def update_manifest(
        self, manifest_id: str, manifest_update: ManifestUpdate
    ) -> Optional[DeliveryManifest]:
        """Update a manifest"""
        existing_manifest = self.storage.get(manifest_id)
        if not existing_manifest:
            return None

        update_data = manifest_update.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.now().isoformat()

        updated_manifest = {**existing_manifest, **update_data}
        self.storage.update(manifest_id, updated_manifest)

        return DeliveryManifest(**updated_manifest)

    def delete_manifest(self, manifest_id: str) -> bool:
        """Delete a manifest"""
        return self.storage.delete(manifest_id)

    def assign_manifest(self, manifest_id: str) -> Optional[DeliveryManifest]:
        """Assign manifest to driver"""
        update = ManifestUpdate(status=ManifestStatus.ASSIGNED)
        return self.update_manifest(manifest_id, update)

    def start_manifest(self, manifest_id: str) -> Optional[DeliveryManifest]:
        """Start manifest delivery"""
        update = ManifestUpdate(
            status=ManifestStatus.IN_PROGRESS,
            started_at=datetime.now().isoformat()
        )
        return self.update_manifest(manifest_id, update)

    def complete_manifest(self, manifest_id: str) -> Optional[DeliveryManifest]:
        """Complete manifest"""
        update = ManifestUpdate(
            status=ManifestStatus.COMPLETED,
            completed_at=datetime.now().isoformat()
        )
        return self.update_manifest(manifest_id, update)

    def update_delivery_status(
        self, manifest_id: str, order_id: str, delivery_status: str
    ) -> Optional[DeliveryManifest]:
        """Update status of a specific delivery in the manifest"""
        manifest = self.storage.get(manifest_id)
        if not manifest:
            return None

        deliveries = manifest.get("deliveries", [])
        for delivery in deliveries:
            if delivery.get("order_id") == order_id:
                delivery["status"] = delivery_status

        # Update counters
        completed = sum(1 for d in deliveries if d.get("status") == "delivered")
        failed = sum(1 for d in deliveries if d.get("status") == "failed")

        manifest["deliveries"] = deliveries
        manifest["completed_deliveries"] = completed
        manifest["failed_deliveries"] = failed
        manifest["updated_at"] = datetime.now().isoformat()

        self.storage.update(manifest_id, manifest)
        return DeliveryManifest(**manifest)
