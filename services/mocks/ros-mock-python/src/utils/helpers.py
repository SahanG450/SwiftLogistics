import random
from typing import Optional


def calculate_distance(origin: str, destination: str) -> float:
    """Calculate mock distance between two locations in kilometers"""
    # Simple hash-based distance calculation for consistency
    hash_value = hash(f"{origin}{destination}")
    return abs(hash_value % 1000) + 10.0


def calculate_duration(distance: float, avg_speed: float = 60.0) -> int:
    """Calculate estimated duration in minutes based on distance"""
    # avg_speed in km/h
    hours = distance / avg_speed
    minutes = int(hours * 60)
    # Add some random traffic delay
    traffic_delay = random.randint(0, 30)
    return minutes + traffic_delay


def generate_route_coordinates(origin: str, destination: str, num_stops: int = 0):
    """Generate mock GPS coordinates for route visualization"""
    # This is a simplified mock - in real system would use mapping API
    base_lat = 40.7128  # NY latitude as base
    base_lon = -74.0060  # NY longitude as base

    coordinates = []
    for i in range(num_stops + 2):  # origin + stops + destination
        lat = base_lat + random.uniform(-5, 5)
        lon = base_lon + random.uniform(-5, 5)
        coordinates.append({"latitude": lat, "longitude": lon})

    return coordinates
