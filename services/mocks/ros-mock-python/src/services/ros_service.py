from datetime import datetime
from typing import Dict, List, Optional
import uuid
from ..models.schemas import Route, RouteCreate, RouteUpdate, RouteStatus
from ..utils.helpers import calculate_distance, calculate_duration


class ROSService:
    """Route Optimization Service - In-memory database"""

    def __init__(self):
        self.routes: Dict[str, dict] = {}
        self._initialize_mock_data()

    def _initialize_mock_data(self):
        """Initialize with some mock routes"""
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

        for route_data in mock_routes:
            route_id = str(uuid.uuid4())
            now = datetime.now().isoformat()

            # Calculate distance and duration
            distance = calculate_distance(
                route_data["origin"], route_data["destination"]
            )
            estimated_duration = calculate_duration(distance)

            self.routes[route_id] = {
                "id": route_id,
                **route_data,
                "distance": distance,
                "estimated_duration": estimated_duration,
                "actual_duration": None,
                "created_at": now,
                "updated_at": now,
            }

    def get_all_routes(self) -> List[Route]:
        """Get all routes"""
        return [Route(**route) for route in self.routes.values()]

    def get_route(self, route_id: str) -> Optional[Route]:
        """Get route by ID"""
        route = self.routes.get(route_id)
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

        self.routes[route_id] = route
        return Route(**route)

    def update_route(self, route_id: str, route_data: RouteUpdate) -> Optional[Route]:
        """Update existing route"""
        if route_id not in self.routes:
            return None

        update_data = route_data.model_dump(exclude_unset=True)
        self.routes[route_id].update(update_data)
        self.routes[route_id]["updated_at"] = datetime.now().isoformat()

        return Route(**self.routes[route_id])

    def delete_route(self, route_id: str) -> bool:
        """Delete route"""
        if route_id in self.routes:
            del self.routes[route_id]
            return True
        return False

    def optimize_route(self, route_id: str) -> Optional[Route]:
        """Optimize route (mock optimization)"""
        if route_id not in self.routes:
            return None

        # Mock optimization - reduce duration by 10%
        current_duration = self.routes[route_id].get("estimated_duration", 0)
        optimized_duration = int(current_duration * 0.9)

        self.routes[route_id]["estimated_duration"] = optimized_duration
        self.routes[route_id]["updated_at"] = datetime.now().isoformat()

        return Route(**self.routes[route_id])


# Singleton instance
ros_service = ROSService()
