from datetime import datetime
from typing import Dict, List, Optional
import uuid
import os
from ..models.schemas import Route, RouteCreate, RouteUpdate, RouteStatus
from ..utils.helpers import calculate_distance, calculate_duration
from ..utils.file_storage import FileStorage


class ROSService:
    """Route Optimization Service - File-based storage"""

    def __init__(self):
        # Initialize file storage
        data_dir = os.path.join(os.path.dirname(__file__), "../../data")
        self.storage = FileStorage(data_dir, "routes")
        self._initialize_mock_data()

    def _initialize_mock_data(self):
        """Initialize with some mock routes if file is empty"""
        # Only initialize if storage is empty
        if not self.storage.get_all():
            mock_routes = [
                {
                    "origin": "New York, NY",
                    "destination": "Boston, MA",
                    "vehicle_id": "VEH-001",
                    "driver_id": "DRV-001",
                    "stops": [
                        {
                            "location": "Hartford, CT",
                            "estimated_arrival": "2026-01-30T14:00:00",
                        }
                    ],
                    "status": RouteStatus.IN_PROGRESS,
                },
                {
                    "origin": "Los Angeles, CA",
                    "destination": "San Francisco, CA",
                    "vehicle_id": "VEH-002",
                    "driver_id": "DRV-002",
                    "stops": [],
                    "status": RouteStatus.PLANNED,
                },
            ]

            initial_data = {}
            for route_data in mock_routes:
                route_id = str(uuid.uuid4())
                now = datetime.now().isoformat()

                # Calculate distance and duration
                distance = calculate_distance(
                    route_data["origin"], route_data["destination"]
                )
                estimated_duration = calculate_duration(distance)

                initial_data[route_id] = {
                    "id": route_id,
                    **route_data,
                    "distance": distance,
                    "estimated_duration": estimated_duration,
                    "actual_duration": None,
                    "created_at": now,
                    "updated_at": now,
                }

            self.storage.initialize_with_data(initial_data)

    def get_all_routes(self) -> List[Route]:
        """Get all routes"""
        routes = self.storage.get_all()
        return [Route(**route) for route in routes.values()]

    def get_route(self, route_id: str) -> Optional[Route]:
        """Get route by ID"""
        route = self.storage.get(route_id)
        return Route(**route) if route else None

    def create_route(self, route_data: RouteCreate) -> Route:
        """Create new route with optimization"""
        route_id = str(uuid.uuid4())
        now = datetime.now().isoformat()

        # Calculate distance and duration
        distance = calculate_distance(route_data.origin, route_data.destination)
        estimated_duration = route_data.estimated_duration or calculate_duration(
            distance
        )

        route = {
            "id": route_id,
            **route_data.model_dump(),
            "status": RouteStatus.PLANNED,
            "distance": distance,
            "estimated_duration": estimated_duration,
            "actual_duration": None,
            "created_at": now,
            "updated_at": now,
        }

        self.storage.create(route_id, route)
        return Route(**route)

    def update_route(self, route_id: str, route_data: RouteUpdate) -> Optional[Route]:
        """Update existing route"""
        route = self.storage.get(route_id)
        if not route:
            return None

        update_data = route_data.model_dump(exclude_unset=True)
        route.update(update_data)
        route["updated_at"] = datetime.now().isoformat()

        self.storage.update(route_id, route)
        return Route(**route)

    def delete_route(self, route_id: str) -> bool:
        """Delete route"""
        return self.storage.delete(route_id)

    def optimize_route(self, route_id: str) -> Optional[Route]:
        """Optimize route (mock optimization)"""
        route = self.storage.get(route_id)
        if not route:
            return None

        # Mock optimization - reduce duration by 10%
        current_duration = route.get("estimated_duration", 0)
        optimized_duration = int(current_duration * 0.9)

        route["estimated_duration"] = optimized_duration
        route["updated_at"] = datetime.now().isoformat()

        self.storage.update(route_id, route)
        return Route(**route)


# Singleton instance
ros_service = ROSService()
