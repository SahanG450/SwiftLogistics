# ROS Mock Service - Complete Documentation

**Route Optimization System Mock Service**  
Port: **3002**  
Technology: **Python FastAPI**  
Storage: **File-based JSON**

---

## 📋 Table of Contents

- [Overview](#overview)
- [What It Can Do](#what-it-can-do)
- [How It Works](#how-it-works)
- [API Endpoints](#api-endpoints)
- [Data Model](#data-model)
- [Route Optimization](#route-optimization)
- [File Storage](#file-storage)
- [Examples](#examples)
- [Error Handling](#error-handling)

---

## Overview

The ROS Mock Service provides route optimization and management capabilities for Swift Logistics. It simulates route planning, optimization algorithms, and route tracking with file-based persistence.

### Key Features

- ✅ Route CRUD operations
- ✅ Route optimization algorithm
- ✅ Multi-stop route support
- ✅ Distance and duration calculations
- ✅ Route status tracking
- ✅ Vehicle and driver assignment
- ✅ Thread-safe file operations
- ✅ Auto-generated API documentation

---

## What It Can Do

### 1. Route Management

- **Create** new delivery routes
- **Read** all routes or specific route by ID
- **Update** route information and status
- **Delete** routes
- **Track** route progress (planned, in_progress, completed, cancelled)
- **Assign** vehicles and drivers
- **Manage** multiple stops per route

### 2. Route Optimization

- **Calculate** optimal routes between origin and destination
- **Support** multiple waypoints
- **Estimate** travel time and distance
- **Consider** vehicle type constraints
- **Apply** distance and duration limits
- **Generate** optimized stop sequences

### 3. Route Tracking

- **Monitor** route status in real-time
- **Track** estimated vs actual arrival times
- **Record** actual duration
- **Update** stop completion status
- **Calculate** performance metrics

### 4. Route Analysis

- **Filter** routes by status
- **Count** routes by criteria
- **Calculate** total distances
- **Analyze** delivery performance

---

## How It Works

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     ROS Mock Service                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐      ┌──────────────┐    ┌─────────────┐ │
│  │   FastAPI   │ ───► │ ROS Service  │───►│ FileStorage │ │
│  │  (Router)   │      │  (Business)  │    │   (Data)    │ │
│  └─────────────┘      └──────────────┘    └─────────────┘ │
│         │                      │                   │        │
│         │                      │                   │        │
│         ▼                      ▼                   ▼        │
│  ┌─────────────┐      ┌──────────────┐    ┌─────────────┐ │
│  │  Pydantic   │      │ Optimization │    │ JSON File   │ │
│  │ Validation  │      │   Engine     │    │ (Persist)   │ │
│  └─────────────┘      └──────────────┘    └─────────────┘ │
│                              │                              │
│                              ▼                              │
│                      ┌──────────────┐                      │
│                      │   Helpers    │                      │
│                      │ (Distance)   │                      │
│                      └──────────────┘                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Optimization Algorithm

The service uses a simple but effective optimization approach:

1. **Input Validation** - Verify origin, destination, waypoints
2. **Distance Calculation** - Estimate distances using simplified model
3. **Duration Estimation** - Calculate travel time based on distance
4. **Stop Sequencing** - Optimize waypoint order
5. **Constraint Checking** - Verify against max distance/duration
6. **Route Generation** - Create optimized route with stops

**Distance Calculation Formula:**

```python
# Simplified Haversine-like formula
distance = random.uniform(50, 1000)  # km (mock implementation)
duration = distance / 80 * 60        # minutes at 80 km/h average
```

### Route Status Lifecycle

```
planned ──► in_progress ──► completed
   │                            │
   └──────────► cancelled ◄─────┘
```

---

## API Endpoints

### Base URL

```
http://localhost:3002
```

### Endpoints Summary

| Method | Endpoint                      | Description          | Auth Required |
| ------ | ----------------------------- | -------------------- | ------------- |
| GET    | `/api/routes/`                | Get all routes       | No            |
| GET    | `/api/routes/{id}`            | Get route by ID      | No            |
| POST   | `/api/routes/`                | Create new route     | No            |
| PUT    | `/api/routes/{id}`            | Update route         | No            |
| DELETE | `/api/routes/{id}`            | Delete route         | No            |
| POST   | `/api/routes/optimize`        | Optimize route       | No            |
| GET    | `/api/routes/status/{status}` | Get routes by status | No            |
| GET    | `/health`                     | Service health check | No            |
| GET    | `/`                           | Service info         | No            |
| GET    | `/docs`                       | API documentation    | No            |

---

### 1. Get All Routes

**Endpoint:** `GET /api/routes/`

**Description:** Retrieve all route records.

**Request:**

```bash
curl http://localhost:3002/api/routes/
```

**Response:** `200 OK`

```json
[
  {
    "id": "27f07d93-60d7-4932-8ad8-ccffbaf8af2c",
    "origin": "New York, NY",
    "destination": "Boston, MA",
    "vehicle_id": "VEH-001",
    "driver_id": "DRV-001",
    "stops": [
      {
        "location": "Hartford, CT",
        "coordinates": null,
        "estimated_arrival": "2026-01-30T14:00:00",
        "actual_arrival": null
      }
    ],
    "status": "in_progress",
    "estimated_duration": 240,
    "actual_duration": null,
    "distance": 215.0,
    "created_at": "2026-02-01T08:00:00.000000",
    "updated_at": "2026-02-01T08:00:00.000000"
  }
]
```

---

### 2. Get Route by ID

**Endpoint:** `GET /api/routes/{route_id}`

**Description:** Retrieve a specific route by UUID.

**Request:**

```bash
curl http://localhost:3002/api/routes/27f07d93-60d7-4932-8ad8-ccffbaf8af2c
```

**Response:** `200 OK`

```json
{
  "id": "27f07d93-60d7-4932-8ad8-ccffbaf8af2c",
  "origin": "New York, NY",
  "destination": "Boston, MA",
  "vehicle_id": "VEH-001",
  "driver_id": "DRV-001",
  "stops": [
    {
      "location": "Hartford, CT",
      "coordinates": null,
      "estimated_arrival": "2026-01-30T14:00:00",
      "actual_arrival": null
    }
  ],
  "status": "in_progress",
  "estimated_duration": 240,
  "actual_duration": null,
  "distance": 215.0,
  "created_at": "2026-02-01T08:00:00.000000",
  "updated_at": "2026-02-01T08:00:00.000000"
}
```

**Error Response:** `404 Not Found`

```json
{
  "detail": "Route with ID {id} not found"
}
```

---

### 3. Create Route

**Endpoint:** `POST /api/routes/`

**Description:** Create a new delivery route.

**Request Body:**

```json
{
  "origin": "Chicago, IL",
  "destination": "Detroit, MI",
  "vehicle_id": "VEH-003",
  "driver_id": "DRV-003",
  "distance": 280.0,
  "status": "planned",
  "stops": [
    {
      "location": "Gary, IN",
      "coordinates": null,
      "estimated_arrival": "2026-02-02T10:00:00"
    }
  ]
}
```

**Request Example:**

```bash
curl -X POST http://localhost:3002/api/routes/ \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Chicago, IL",
    "destination": "Detroit, MI",
    "vehicle_id": "VEH-003",
    "driver_id": "DRV-003",
    "distance": 280.0,
    "status": "planned"
  }'
```

**Response:** `201 Created`

```json
{
  "id": "b1c2d3e4-f5g6-h7i8-j9k0-l1m2n3o4p5q6",
  "origin": "Chicago, IL",
  "destination": "Detroit, MI",
  "vehicle_id": "VEH-003",
  "driver_id": "DRV-003",
  "stops": [],
  "status": "planned",
  "estimated_duration": 210,
  "actual_duration": null,
  "distance": 280.0,
  "created_at": "2026-02-01T12:00:00.123456",
  "updated_at": "2026-02-01T12:00:00.123456"
}
```

---

### 4. Update Route

**Endpoint:** `PUT /api/routes/{route_id}`

**Description:** Update route information. Only provided fields are updated.

**Request Body:** (All fields optional)

```json
{
  "status": "completed",
  "actual_duration": 235
}
```

**Request Example:**

```bash
curl -X PUT http://localhost:3002/api/routes/b1c2d3e4-f5g6-h7i8-j9k0-l1m2n3o4p5q6 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "actual_duration": 235
  }'
```

**Response:** `200 OK`

```json
{
  "id": "b1c2d3e4-f5g6-h7i8-j9k0-l1m2n3o4p5q6",
  "origin": "Chicago, IL",
  "destination": "Detroit, MI",
  "vehicle_id": "VEH-003",
  "driver_id": "DRV-003",
  "stops": [],
  "status": "completed",
  "estimated_duration": 210,
  "actual_duration": 235,
  "distance": 280.0,
  "created_at": "2026-02-01T12:00:00.123456",
  "updated_at": "2026-02-01T15:55:00.789012"
}
```

---

### 5. Delete Route

**Endpoint:** `DELETE /api/routes/{route_id}`

**Description:** Delete a route record permanently.

**Request:**

```bash
curl -X DELETE http://localhost:3002/api/routes/b1c2d3e4-f5g6-h7i8-j9k0-l1m2n3o4p5q6
```

**Response:** `204 No Content`

---

### 6. Optimize Route ⭐

**Endpoint:** `POST /api/routes/optimize`

**Description:** Calculate optimal route with distance and duration estimates.

**Request Body:**

```json
{
  "origin": "Los Angeles, CA",
  "destination": "San Francisco, CA",
  "waypoints": ["Bakersfield, CA", "Fresno, CA"],
  "vehicle_type": "truck",
  "constraints": {
    "max_distance": 1000,
    "max_duration": 720
  }
}
```

**Request Example:**

```bash
curl -X POST http://localhost:3002/api/routes/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Los Angeles, CA",
    "destination": "San Francisco, CA",
    "waypoints": ["Bakersfield, CA", "Fresno, CA"],
    "vehicle_type": "truck",
    "constraints": {
      "max_distance": 1000,
      "max_duration": 720
    }
  }'
```

**Response:** `200 OK`

```json
{
  "route_id": "opt-c4d5e6f7-g8h9-i0j1-k2l3-m4n5o6p7q8r9",
  "origin": "Los Angeles, CA",
  "destination": "San Francisco, CA",
  "waypoints": ["Bakersfield, CA", "Fresno, CA"],
  "optimized_sequence": [
    "Los Angeles, CA",
    "Bakersfield, CA",
    "Fresno, CA",
    "San Francisco, CA"
  ],
  "total_distance": 615.3,
  "estimated_duration": 462,
  "vehicle_type": "truck",
  "stops": [
    {
      "location": "Bakersfield, CA",
      "coordinates": null,
      "estimated_arrival": "2026-02-02T12:30:00",
      "sequence_number": 1
    },
    {
      "location": "Fresno, CA",
      "coordinates": null,
      "estimated_arrival": "2026-02-02T15:15:00",
      "sequence_number": 2
    }
  ],
  "metadata": {
    "algorithm": "mock_optimizer_v1",
    "optimization_time_ms": 45,
    "constraints_met": true
  }
}
```

**Constraint Violation:** `400 Bad Request`

```json
{
  "detail": "Route exceeds maximum distance constraint"
}
```

---

### 7. Get Routes by Status

**Endpoint:** `GET /api/routes/status/{status}`

**Description:** Filter routes by their current status.

**Status Values:** `planned`, `in_progress`, `completed`, `cancelled`

**Request:**

```bash
curl http://localhost:3002/api/routes/status/in_progress
```

**Response:** `200 OK`

```json
[
  {
    "id": "27f07d93-60d7-4932-8ad8-ccffbaf8af2c",
    "origin": "New York, NY",
    "destination": "Boston, MA",
    "status": "in_progress",
    ...
  }
]
```

---

### 8. Health Check

**Endpoint:** `GET /health`

**Description:** Check service health and get statistics.

**Request:**

```bash
curl http://localhost:3002/health
```

**Response:** `200 OK`

```json
{
  "status": "healthy",
  "service": "ROS Mock Service",
  "total_routes": 5,
  "routes_in_progress": 2
}
```

---

## Data Model

### Route Schema

```python
class Route(BaseModel):
    id: str                          # UUID v4
    origin: str                      # Starting location
    destination: str                 # End location
    vehicle_id: str                  # Assigned vehicle
    driver_id: str                   # Assigned driver
    stops: List[Stop]                # Intermediate stops
    status: str                      # Route status
    estimated_duration: Optional[int]  # Minutes
    actual_duration: Optional[int]     # Minutes
    distance: float                  # Kilometers
    created_at: datetime             # Creation timestamp
    updated_at: datetime             # Last update timestamp
```

### Stop Schema

```python
class Stop(BaseModel):
    location: str                    # Stop address
    coordinates: Optional[dict]      # GPS coordinates
    estimated_arrival: Optional[datetime]
    actual_arrival: Optional[datetime]
    sequence_number: Optional[int]   # Stop order
```

### Optimization Request Schema

```python
class OptimizeRequest(BaseModel):
    origin: str                      # Start point
    destination: str                 # End point
    waypoints: List[str]             # Intermediate stops
    vehicle_type: str                # Vehicle category
    constraints: Optional[dict]      # Distance/time limits
```

### Field Constraints

| Field                | Type    | Required | Validation                              | Example          |
| -------------------- | ------- | -------- | --------------------------------------- | ---------------- |
| `id`                 | UUID    | Auto     | UUID v4                                 | `"27f07d93-..."` |
| `origin`             | String  | Yes      | Min 1 char                              | `"New York, NY"` |
| `destination`        | String  | Yes      | Min 1 char                              | `"Boston, MA"`   |
| `vehicle_id`         | String  | Yes      | Min 1 char                              | `"VEH-001"`      |
| `driver_id`          | String  | Yes      | Min 1 char                              | `"DRV-001"`      |
| `stops`              | Array   | No       | Valid Stop objects                      | `[...]`          |
| `status`             | Enum    | Yes      | planned/in_progress/completed/cancelled | `"planned"`      |
| `distance`           | Float   | Yes      | > 0                                     | `215.5`          |
| `estimated_duration` | Integer | No       | > 0                                     | `240`            |
| `actual_duration`    | Integer | No       | > 0                                     | `235`            |

### Status Values

- `planned` - Route created but not started
- `in_progress` - Currently being executed
- `completed` - Successfully finished
- `cancelled` - Cancelled before/during execution

---

## Route Optimization

### Optimization Algorithm

The service uses a mock optimization algorithm that:

1. **Validates Input**

   - Ensures origin and destination are provided
   - Checks waypoints are valid
   - Validates vehicle type

2. **Calculates Distances**

   ```python
   # Mock distance calculation
   base_distance = random.uniform(50, 500)
   per_waypoint = random.uniform(20, 100)
   total_distance = base_distance + (len(waypoints) * per_waypoint)
   ```

3. **Estimates Duration**

   ```python
   # Average speed: 80 km/h for trucks, 100 km/h for vans
   avg_speed = 80 if vehicle_type == "truck" else 100
   duration_minutes = (total_distance / avg_speed) * 60
   ```

4. **Optimizes Sequence**

   - Orders waypoints for minimum distance
   - Considers constraints
   - Generates stop times

5. **Applies Constraints**
   ```python
   if constraints:
       if total_distance > constraints.get('max_distance'):
           raise Exception("Distance constraint exceeded")
       if duration > constraints.get('max_duration'):
           raise Exception("Duration constraint exceeded")
   ```

### Optimization Example

**Input:**

```json
{
  "origin": "New York",
  "destination": "Boston",
  "waypoints": ["Hartford", "Providence"],
  "vehicle_type": "truck",
  "constraints": {
    "max_distance": 500,
    "max_duration": 360
  }
}
```

**Output:**

```json
{
  "optimized_sequence": ["New York", "Hartford", "Providence", "Boston"],
  "total_distance": 245.8,
  "estimated_duration": 185,
  "constraints_met": true
}
```

### Supported Vehicle Types

- `truck` - Large delivery trucks (avg 80 km/h)
- `van` - Delivery vans (avg 100 km/h)
- `car` - Passenger cars (avg 110 km/h)

---

## File Storage

### Storage Location

```
services/mocks/ros-mock/data/routes.json
```

### File Format

```json
{
  "route_uuid_1": {
    "id": "route_uuid_1",
    "origin": "New York, NY",
    "destination": "Boston, MA",
    "stops": [...],
    ...
  }
}
```

### Storage Operations

```python
# All operations are thread-safe
storage.get_all()        # Get all routes
storage.get(route_id)    # Get one route
storage.create(id, data) # Create route
storage.update(id, data) # Update route
storage.delete(route_id) # Delete route
```

### Viewing Data

```bash
# Pretty print routes
cat data/routes.json | jq

# Count routes
cat data/routes.json | jq 'length'

# Get in-progress routes
cat data/routes.json | jq '.[] | select(.status=="in_progress")'

# Calculate total distance
cat data/routes.json | jq '[.[] | .distance] | add'
```

---

## Examples

### Complete Workflow

```bash
# 1. Create a new route
curl -X POST http://localhost:3002/api/routes/ \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Miami, FL",
    "destination": "Orlando, FL",
    "vehicle_id": "VEH-005",
    "driver_id": "DRV-005",
    "distance": 235.0,
    "status": "planned"
  }'

# 2. Optimize a route before creation
curl -X POST http://localhost:3002/api/routes/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Seattle, WA",
    "destination": "Portland, OR",
    "waypoints": ["Tacoma, WA"],
    "vehicle_type": "van"
  }'

# 3. Start the route
ROUTE_ID="<returned-uuid>"
curl -X PUT http://localhost:3002/api/routes/$ROUTE_ID \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'

# 4. Complete the route
curl -X PUT http://localhost:3002/api/routes/$ROUTE_ID \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "actual_duration": 240
  }'

# 5. Get all in-progress routes
curl http://localhost:3002/api/routes/status/in_progress
```

### Python Client

```python
import requests

BASE_URL = "http://localhost:3002"

# Optimize route
optimize_req = {
    "origin": "Dallas, TX",
    "destination": "Houston, TX",
    "waypoints": ["Austin, TX"],
    "vehicle_type": "truck",
    "constraints": {
        "max_distance": 500,
        "max_duration": 300
    }
}

response = requests.post(
    f"{BASE_URL}/api/routes/optimize",
    json=optimize_req
)

optimized = response.json()
print(f"Distance: {optimized['total_distance']} km")
print(f"Duration: {optimized['estimated_duration']} min")
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning               | When It Occurs                       |
| ---- | --------------------- | ------------------------------------ |
| 200  | OK                    | Successful GET, PUT, POST (optimize) |
| 201  | Created               | Successful POST (create route)       |
| 204  | No Content            | Successful DELETE                    |
| 400  | Bad Request           | Constraint violation, invalid input  |
| 404  | Not Found             | Route ID doesn't exist               |
| 422  | Unprocessable Entity  | Validation error                     |
| 500  | Internal Server Error | Server-side error                    |

### Common Errors

**1. Route Not Found**

```json
{
  "detail": "Route with ID abc123 not found"
}
```

**2. Constraint Violation**

```json
{
  "detail": "Route exceeds maximum distance constraint (650km > 500km)"
}
```

**3. Invalid Status**

```json
{
  "detail": [
    {
      "loc": ["body", "status"],
      "msg": "value is not a valid enumeration member"
    }
  ]
}
```

---

## Performance

### Benchmarks

- **Request Latency:** < 15ms
- **Optimization Time:** < 50ms
- **Throughput:** ~800 requests/second
- **Max Routes:** 5,000+ efficient

---

## Support & Documentation

- **API Docs:** http://localhost:3002/docs
- **Health Check:** http://localhost:3002/health
- **Source Code:** `services/mocks/ros-mock/`

---

**Last Updated:** February 1, 2026  
**Version:** 1.0.0  
**Status:** Production Ready (Development Use Only)
