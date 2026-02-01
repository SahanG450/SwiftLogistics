# ROS Mock Service - Complete Documentation

## Service Overview

**ROS (Route Optimization System) Mock Service** simulates a modern, cloud-based third-party service that generates optimized delivery routes. This service takes delivery addresses and vehicle availability to create the most efficient routes for drivers, supporting Swift Logistics' delivery operations.

### Service Information
- **Service Name**: ROS Mock Service
- **Port**: 3003
- **Version**: 2.0.0
- **Technology**: Python 3.11 + FastAPI
- **API Style**: RESTful API (modern cloud-based service)
- **Data Storage**: File-based JSON persistence

### Core Capabilities
1. **Route Planning & Optimization** - Generate efficient delivery sequences
2. **Delivery Manifests** - Daily delivery lists for driver mobile app
3. **Real-time Route Updates** - Dynamic route changes and priority deliveries
4. **Driver Assignment** - Assign routes to specific drivers and vehicles
5. **Efficient Delivery Sequencing** - Optimize delivery order based on location and priority

---

## Architecture & File Structure

```
services/mocks/ros-mock/
├── app.py                          # Main FastAPI application
├── Dockerfile                      # Container configuration
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── data/                           # JSON file storage
│   ├── routes.json
│   └── manifests.json
└── src/
    ├── config/
    │   └── settings.py             # Configuration management
    ├── models/
    │   └── schemas.py              # Pydantic data models
    ├── routes/
    │   ├── ros_routes.py           # Route optimization endpoints
    │   └── manifest_routes.py      # Delivery manifest endpoints
    ├── services/
    │   ├── ros_service.py          # Route optimization logic
    │   └── manifest_service.py     # Manifest management logic
    └── utils/
        ├── file_storage.py         # JSON file persistence
        └── helpers.py              # Utility functions
```

---

## API Endpoints Reference

### Health & Status Endpoints

#### GET /
**Service Information**
```bash
curl http://localhost:3003/
```
**Response:**
```json
{
  "service": "ROS Mock Service",
  "description": "Route Optimization System - Modern cloud-based third-party service",
  "status": "running",
  "version": "2.0.0",
  "capabilities": [
    "Route Planning & Optimization",
    "Delivery Manifests",
    "Real-time Route Updates",
    "Driver Assignment",
    "Efficient Delivery Sequencing"
  ]
}
```

#### GET /health
**Health Check with Manifest Count**
```bash
curl http://localhost:3003/health
```
**Response:**
```json
{
  "status": "healthy",
  "service": "ROS Mock Service",
  "version": "2.0.0",
  "manifest_count": 45
}
```

---

### Delivery Manifest Endpoints

#### GET /api/manifests/
**Get All Manifests with Filtering**
```bash
# Get all manifests
curl http://localhost:3003/api/manifests/

# Filter by driver (Driver Mobile App)
curl http://localhost:3003/api/manifests/?driver_id=driver-001

# Filter by status
curl http://localhost:3003/api/manifests/?status=in_progress

# Filter by date
curl "http://localhost:3003/api/manifests/?delivery_date=2026-02-01"
```

#### GET /api/manifests/{manifest_id}
**Get Specific Manifest**
```bash
curl http://localhost:3003/api/manifests/manifest-123
```
**Response:**
```json
{
  "id": "manifest-123",
  "manifest_number": "MAN-2026-2001",
  "driver_id": "driver-001",
  "driver_name": "Sunil Silva",
  "vehicle_id": "VEH-101",
  "route_id": "route-456",
  "delivery_date": "2026-02-01",
  "status": "in_progress",
  "deliveries": [
    {
      "order_id": "order-001",
      "package_id": "pkg-001",
      "tracking_number": "SL100001",
      "recipient_name": "Nimal Perera",
      "delivery_address": "No. 45, Galle Road, Colombo 03",
      "contact_phone": "+94771234567",
      "coordinates": {
        "latitude": 6.9271,
        "longitude": 79.8612
      },
      "priority": "normal",
      "special_instructions": "Call before delivery",
      "estimated_delivery_time": "2026-02-01T10:30:00Z",
      "status": "pending",
      "sequence": 1
    },
    {
      "order_id": "order-002",
      "package_id": "pkg-002",
      "tracking_number": "SL100002",
      "recipient_name": "Kamala Fernando",
      "delivery_address": "138, Dutugemunu Street, Dehiwala",
      "contact_phone": "+94777654321",
      "coordinates": {
        "latitude": 6.8532,
        "longitude": 79.8638
      },
      "priority": "high",
      "special_instructions": null,
      "estimated_delivery_time": "2026-02-01T11:00:00Z",
      "status": "pending",
      "sequence": 2
    }
  ],
  "total_deliveries": 2,
  "completed_deliveries": 0,
  "failed_deliveries": 0,
  "started_at": "2026-02-01T09:00:00Z",
  "completed_at": null,
  "notes": null,
  "created_at": "2026-01-31T18:00:00Z",
  "updated_at": "2026-02-01T09:00:00Z"
}
```

#### POST /api/manifests/
**Create New Delivery Manifest**
```bash
curl -X POST http://localhost:3003/api/manifests/ \
  -H "Content-Type: application/json" \
  -d '{
    "driver_id": "driver-001",
    "vehicle_id": "VEH-101",
    "route_id": "route-456",
    "delivery_date": "2026-02-01",
    "deliveries": [
      {
        "order_id": "order-001",
        "package_id": "pkg-001",
        "tracking_number": "SL100001",
        "recipient_name": "Nimal Perera",
        "delivery_address": "No. 45, Galle Road, Colombo 03",
        "contact_phone": "+94771234567",
        "coordinates": {
          "latitude": 6.9271,
          "longitude": 79.8612
        },
        "priority": "normal"
      },
      {
        "order_id": "order-002",
        "package_id": "pkg-002",
        "tracking_number": "SL100002",
        "recipient_name": "Kamala Fernando",
        "delivery_address": "138, Dutugemunu Street, Dehiwala",
        "contact_phone": "+94777654321",
        "coordinates": {
          "latitude": 6.8532,
          "longitude": 79.8638
        },
        "priority": "high"
      }
    ]
  }'
```

#### PUT /api/manifests/{manifest_id}
**Update Manifest**
```bash
curl -X PUT http://localhost:3003/api/manifests/manifest-123 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed", "notes": "All deliveries completed successfully"}'
```

#### DELETE /api/manifests/{manifest_id}
**Delete Manifest**
```bash
curl -X DELETE http://localhost:3003/api/manifests/manifest-123
```

---

### Manifest Workflow Endpoints

#### POST /api/manifests/{manifest_id}/assign
**Assign Manifest to Driver**
```bash
curl -X POST http://localhost:3003/api/manifests/manifest-123/assign
```
Moves manifest from `draft` to `assigned` status.

#### POST /api/manifests/{manifest_id}/start
**Driver Starts Delivery Route**
```bash
curl -X POST http://localhost:3003/api/manifests/manifest-123/start
```
Marks manifest as `in_progress` and records start time. Used by Driver Mobile App.

#### POST /api/manifests/{manifest_id}/complete
**Complete Delivery Route**
```bash
curl -X POST http://localhost:3003/api/manifests/manifest-123/complete
```
Marks manifest as `completed` and records completion time.

#### PUT /api/manifests/{manifest_id}/deliveries/{order_id}
**Update Individual Delivery Status**
```bash
curl -X PUT "http://localhost:3003/api/manifests/manifest-123/deliveries/order-001?status=delivered"
```

**Delivery Status Values:**
- `pending` - Not yet attempted
- `out_for_delivery` - Driver en route
- `delivered` - Successfully delivered
- `failed` - Delivery failed

---

## Route Optimization Endpoints

#### GET /api/routes/
**Get All Routes**
```bash
curl http://localhost:3003/api/routes/
```

#### POST /api/routes/optimize
**Optimize Delivery Route**
```bash
curl -X POST http://localhost:3003/api/routes/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "delivery_addresses": [
      {
        "order_id": "order-001",
        "address": "No. 45, Galle Road, Colombo 03",
        "coordinates": {"latitude": 6.9271, "longitude": 79.8612},
        "priority": "normal"
      },
      {
        "order_id": "order-002",
        "address": "138, Dutugemunu Street, Dehiwala",
        "coordinates": {"latitude": 6.8532, "longitude": 79.8638},
        "priority": "high"
      },
      {
        "order_id": "order-003",
        "address": "25, Baseline Road, Colombo 09",
        "coordinates": {"latitude": 6.8944, "longitude": 79.8607},
        "priority": "urgent"
      }
    ],
    "vehicle_capacity": 50,
    "max_route_duration": 480,
    "start_location": {"latitude": 6.9497, "longitude": 79.9211},
    "priority_deliveries": ["order-003"]
  }'
```

**Response:**
```json
{
  "route_id": "route-789",
  "optimized_sequence": [2, 0, 1],
  "total_distance": 15.3,
  "estimated_duration": 95,
  "waypoints": [
    {
      "order_id": "order-003",
      "sequence": 1,
      "address": "25, Baseline Road, Colombo 09",
      "estimated_arrival": "2026-02-01T09:30:00Z",
      "distance_from_previous": 5.2
    },
    {
      "order_id": "order-001",
      "sequence": 2,
      "address": "No. 45, Galle Road, Colombo 03",
      "estimated_arrival": "2026-02-01T10:00:00Z",
      "distance_from_previous": 4.8
    },
    {
      "order_id": "order-002",
      "sequence": 3,
      "address": "138, Dutugemunu Street, Dehiwala",
      "estimated_arrival": "2026-02-01T10:30:00Z",
      "distance_from_previous": 5.3
    }
  ],
  "created_at": "2026-02-01T08:00:00Z"
}
```

---

## Manifest Number Format

**Format**: `MAN-YYYY-NNNN`
- `MAN` - Manifest identifier
- `YYYY` - Year (4 digits)
- `NNNN` - Sequential number (4 digits)

**Examples:**
- `MAN-2026-2001` - First manifest of 2026
- `MAN-2026-2002` - Second manifest of 2026
- `MAN-2026-9999` - Maximum for year

---

## Data Models & Schemas

### Delivery Manifest Schema
```python
{
  "id": "uuid",
  "manifest_number": "MAN-2026-2001",
  "driver_id": "driver-001",
  "driver_name": "Sunil Silva",
  "vehicle_id": "VEH-101",
  "route_id": "route-456",
  "delivery_date": "2026-02-01",
  "status": "in_progress",
  "deliveries": [
    {
      "order_id": "order-001",
      "package_id": "pkg-001",
      "tracking_number": "SL100001",
      "recipient_name": "Nimal Perera",
      "delivery_address": "No. 45, Galle Road, Colombo 03",
      "contact_phone": "+94771234567",
      "coordinates": {
        "latitude": 6.9271,
        "longitude": 79.8612
      },
      "priority": "normal",
      "special_instructions": "Call before delivery",
      "estimated_delivery_time": "2026-02-01T10:30:00Z",
      "status": "pending",
      "sequence": 1
    }
  ],
  "total_deliveries": 15,
  "completed_deliveries": 3,
  "failed_deliveries": 1,
  "started_at": "2026-02-01T09:00:00Z",
  "completed_at": null,
  "notes": null,
  "created_at": "2026-01-31T18:00:00Z",
  "updated_at": "2026-02-01T11:30:00Z"
}
```

### Manifest Status Flow
```
draft → assigned → in_progress → completed/cancelled
```

### Delivery Priority Levels
- `low` - Standard delivery (3-5 days)
- `normal` - Regular delivery (1-2 days)
- `high` - Priority delivery (same day)
- `urgent` - Express delivery (Black Friday, Avurudu sales)

---

## Setup & Installation

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- Docker (optional)

### Local Development Setup

1. **Navigate to service directory:**
```bash
cd services/mocks/ros-mock
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
```

5. **Run the service:**
```bash
python app.py
```

The service will start on `http://localhost:3003`

### Docker Deployment

```bash
docker build -t ros-mock-service .
docker run -p 3003:3003 -v $(pwd)/data:/app/data ros-mock-service
```

### Using Docker Compose

From project root:
```bash
docker-compose up ros-mock
```

---

## Configuration

### Environment Variables
```bash
# Service Configuration
APP_NAME="ROS Mock Service"
HOST=0.0.0.0
PORT=3003
DEBUG=true

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Data Storage
DATA_DIR=/app/data

# Manifest Configuration
MANIFEST_PREFIX=MAN
MANIFEST_YEAR_RESET=true
```

---

## Business Context & Integration

### Swift Logistics Driver Mobile App Integration

The ROS Mock Service directly supports the **SwiftTrack Driver Mobile App** with:

1. **Daily Manifest Viewing**: Drivers retrieve their assigned manifest
2. **Optimized Route Display**: Deliveries shown in optimal sequence
3. **Real-time Updates**: Route changes and priority deliveries pushed to app
4. **Delivery Status Updates**: Drivers mark deliveries as completed/failed
5. **Proof of Delivery**: Integration with CMS for signature/photo upload

### Driver Mobile App Workflow

```bash
# 1. Driver logs in and retrieves manifest for the day
curl "http://localhost:3003/api/manifests/?driver_id=driver-001&delivery_date=2026-02-01"

# 2. Driver starts the route
curl -X POST http://localhost:3003/api/manifests/manifest-123/start

# 3. Driver completes each delivery
curl -X PUT "http://localhost:3003/api/manifests/manifest-123/deliveries/order-001?status=delivered"

# 4. Driver marks delivery as failed (recipient not available)
curl -X PUT "http://localhost:3003/api/manifests/manifest-123/deliveries/order-002?status=failed"

# 5. Driver completes the route
curl -X POST http://localhost:3003/api/manifests/manifest-123/complete
```

### Integration Points

- **CMS Mock**: Order intake and delivery proof recording
- **WMS Mock**: Package loading and tracking information
- **ROS Adapter**: Route data transformation for internal systems
- **Orchestrator**: Workflow coordination
- **Driver Mobile App**: Real-time manifest and route display

### High-Priority Delivery Handling

During promotional events (Black Friday, Avurudu):
- **Urgent priority** deliveries are automatically sequenced first
- Real-time route recalculation for new high-priority orders
- Driver receives push notifications for route changes
- Optimized to minimize total delivery time while prioritizing urgent orders

---

## Route Optimization Algorithm

### Optimization Factors
1. **Distance**: Minimize total route distance
2. **Priority**: Urgent deliveries first, then high, normal, low
3. **Delivery Windows**: Respect time constraints
4. **Vehicle Capacity**: Ensure vehicle can carry all packages
5. **Traffic Patterns**: Time-of-day traffic considerations (future)

### Current Implementation
- Simple greedy algorithm with priority weighting
- Distance calculation using Haversine formula
- Priority deliveries moved to front of sequence
- Nearest-neighbor heuristic for remaining deliveries

---

## Interactive API Documentation

Access interactive API docs when service is running:

- **Swagger UI**: http://localhost:3003/docs
- **Service Info**: http://localhost:3003/
- **Health Check**: http://localhost:3003/health

---

## Testing the Service

### Complete Manifest Workflow Test
```bash
# 1. Health check
curl http://localhost:3003/health

# 2. Create a delivery manifest
MANIFEST_ID=$(curl -X POST http://localhost:3003/api/manifests/ \
  -H "Content-Type: application/json" \
  -d '{
    "driver_id": "driver-001",
    "vehicle_id": "VEH-101",
    "route_id": "route-456",
    "delivery_date": "2026-02-01",
    "deliveries": [
      {
        "order_id": "order-001",
        "package_id": "pkg-001",
        "tracking_number": "SL100001",
        "recipient_name": "Nimal Perera",
        "delivery_address": "No. 45, Galle Road, Colombo 03",
        "contact_phone": "+94771234567",
        "coordinates": {"latitude": 6.9271, "longitude": 79.8612},
        "priority": "normal"
      }
    ]
  }' | jq -r '.id')

# 3. Assign to driver
curl -X POST http://localhost:3003/api/manifests/$MANIFEST_ID/assign

# 4. Driver starts route
curl -X POST http://localhost:3003/api/manifests/$MANIFEST_ID/start

# 5. Update delivery status
curl -X PUT "http://localhost:3003/api/manifests/$MANIFEST_ID/deliveries/order-001?status=delivered"

# 6. Complete manifest
curl -X POST http://localhost:3003/api/manifests/$MANIFEST_ID/complete

# 7. View completed manifest
curl http://localhost:3003/api/manifests/$MANIFEST_ID | jq
```

---

## Troubleshooting

### Service won't start
```bash
# Check port availability
lsof -i :3003

# View logs
docker logs ros-mock
```

### Manifest numbers not generating
- Check `MANIFEST_PREFIX` in `.env`
- Verify year-based numbering config
- Check data directory permissions

### Route optimization slow
- Reduce number of delivery addresses
- Check coordinate data validity
- Monitor CPU usage during optimization

---

## Development Notes

### Cloud-Based Third-Party Service
- This simulates a modern SaaS route optimization service
- Real-world equivalents: Google Route Optimization API, MapBox, HERE Technologies
- RESTful API design for easy integration
- JSON request/response format

### Extending Optimization Algorithm
To implement more sophisticated routing:
1. Install optimization library: `pip install ortools`
2. Update `src/utils/helpers.py` with vehicle routing solver
3. Add constraints for delivery windows, vehicle capacity
4. Implement multi-vehicle routing support

---

## Version History

**Version 2.0.0** (Current)
- ✅ Delivery manifest management
- ✅ Driver mobile app support
- ✅ Real-time delivery status updates
- ✅ Route optimization with priority handling
- ✅ Manifest number generation
- ✅ Complete workflow support

**Version 1.0.0**
- Basic route planning
- Simple waypoint sequencing

---

## Support & Documentation

- **API Documentation**: http://localhost:3003/docs
- **Service Port**: 3003
- **Protocol**: HTTP/REST (modern cloud-based API)
- **Data Format**: JSON

---

**Last Updated**: February 1, 2026  
**Maintainer**: Swift Logistics Development Team  
**Status**: Production Ready
