# WMS Mock Service - Complete Documentation

## Service Overview

**WMS (Warehouse Management System) Mock Service** simulates a warehouse management system that tracks packages from the moment they are received from clients until they are loaded onto vehicles for delivery. This service uses a proprietary messaging protocol over TCP/IP (REST simulation for development).

### Service Information
- **Service Name**: WMS Mock Service
- **Port**: 3002
- **Version**: 2.0.0
- **Technology**: Python 3.11 + FastAPI
- **API Style**: REST (simulating proprietary TCP/IP messaging protocol)
- **Data Storage**: File-based JSON persistence

### Core Capabilities
1. **Package Receiving** - Track packages arriving from e-commerce clients
2. **Quality Inspection** - Inspect package condition upon receipt
3. **Warehouse Storage** - Assign and track warehouse locations
4. **Package Tracking** - Real-time tracking with unique tracking numbers (SL format)
5. **Vehicle Loading** - Track packages loaded onto delivery vehicles

---

## Architecture & File Structure

```
services/mocks/wms-mock/
├── app.py                          # Main FastAPI application
├── Dockerfile                      # Container configuration
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── data/                           # JSON file storage
│   ├── inventory.json
│   └── packages.json
└── src/
    ├── config/
    │   └── settings.py             # Configuration management
    ├── models/
    │   └── schemas.py              # Pydantic data models
    ├── routes/
    │   ├── wms_routes.py           # Inventory endpoints
    │   └── package_routes.py       # Package tracking endpoints
    ├── handlers/
    │   └── wms_handlers.py         # TCP/IP protocol simulation
    └── utils/
        └── file_storage.py         # JSON file persistence utility
```

---

## API Endpoints Reference

### Health & Status Endpoints

#### GET /
**Service Information**
```bash
curl http://localhost:3002/
```
**Response:**
```json
{
  "service": "WMS Mock Service",
  "description": "Warehouse Management System - Package tracking from receipt to loading",
  "status": "running",
  "version": "2.0.0",
  "capabilities": [
    "Package Receiving",
    "Quality Inspection",
    "Warehouse Storage",
    "Package Tracking",
    "Vehicle Loading"
  ]
}
```

#### GET /health
**Health Check with Package Count**
```bash
curl http://localhost:3002/health
```
**Response:**
```json
{
  "status": "healthy",
  "service": "WMS Mock Service",
  "version": "2.0.0",
  "package_count": 1250
}
```

---

### Package Management Endpoints

#### GET /api/packages/
**Get All Packages with Filtering**
```bash
# Get all packages
curl http://localhost:3002/api/packages/

# Filter by status
curl http://localhost:3002/api/packages/?status=stored

# Filter by client
curl http://localhost:3002/api/packages/?client_id=client-001

# Filter by order
curl http://localhost:3002/api/packages/?order_id=order-123
```

#### GET /api/packages/{package_id}
**Get Specific Package**
```bash
curl http://localhost:3002/api/packages/pkg-123
```

#### GET /api/packages/tracking/{tracking_number}
**Track Package by Tracking Number**
```bash
curl http://localhost:3002/api/packages/tracking/SL100001
```
**Response:**
```json
{
  "id": "pkg-123",
  "tracking_number": "SL100001",
  "order_id": "order-123",
  "client_id": "client-001",
  "description": "Samsung Galaxy S24 - Electronics",
  "status": "stored",
  "condition": "good",
  "weight": 0.5,
  "dimensions": {
    "length": 20,
    "width": 10,
    "height": 15,
    "unit": "cm"
  },
  "location": {
    "warehouse_id": "WH-MAIN-01",
    "zone": "A",
    "rack": "R5",
    "shelf": "S2"
  },
  "events": [
    {
      "event_type": "received",
      "timestamp": "2026-02-01T08:00:00Z",
      "notes": "Package received from client"
    },
    {
      "event_type": "inspected",
      "timestamp": "2026-02-01T08:15:00Z",
      "condition": "good",
      "notes": "Quality check passed"
    },
    {
      "event_type": "stored",
      "timestamp": "2026-02-01T08:30:00Z",
      "location": "WH-MAIN-01/A/R5/S2"
    }
  ],
  "created_at": "2026-02-01T08:00:00Z",
  "updated_at": "2026-02-01T08:30:00Z"
}
```

#### POST /api/packages/
**Create New Package (Receive from Client)**
```bash
curl -X POST http://localhost:3002/api/packages/ \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "order-123",
    "client_id": "client-001",
    "description": "Samsung Galaxy S24 - Electronics",
    "weight": 0.5,
    "dimensions": {
      "length": 20,
      "width": 10,
      "height": 15,
      "unit": "cm"
    },
    "special_handling": "fragile"
  }'
```
**Response:**
```json
{
  "id": "pkg-123",
  "tracking_number": "SL100001",
  "status": "received",
  ...
}
```

#### PUT /api/packages/{package_id}
**Update Package**
```bash
curl -X PUT http://localhost:3002/api/packages/pkg-123 \
  -H "Content-Type: application/json" \
  -d '{"status": "picked"}'
```

#### DELETE /api/packages/{package_id}
**Delete Package**
```bash
curl -X DELETE http://localhost:3002/api/packages/pkg-123
```

---

### Package Workflow Endpoints

#### POST /api/packages/{package_id}/inspect
**Inspect Package (Quality Check)**
```bash
curl -X POST "http://localhost:3002/api/packages/pkg-123/inspect?condition=good&notes=No+damage+detected"
```

**Package Conditions:**
- `good` - Package in perfect condition
- `fair` - Minor cosmetic damage
- `damaged` - Significant damage detected
- `critical` - Severe damage, requires attention

#### POST /api/packages/{package_id}/store
**Store Package in Warehouse Location**
```bash
curl -X POST http://localhost:3002/api/packages/pkg-123/store \
  -H "Content-Type: application/json" \
  -d '{
    "warehouse_id": "WH-MAIN-01",
    "zone": "A",
    "rack": "R5",
    "shelf": "S2"
  }'
```

#### POST /api/packages/{package_id}/pick
**Pick Package for Delivery**
```bash
curl -X POST "http://localhost:3002/api/packages/pkg-123/pick?notes=Picked+for+route+RT-001"
```

#### POST /api/packages/{package_id}/load
**Load Package onto Vehicle**
```bash
curl -X POST "http://localhost:3002/api/packages/pkg-123/load?vehicle_id=VEH-101&driver_id=driver-001&notes=Loaded+on+truck"
```

#### GET /api/packages/status/{status}
**Get Packages by Status**
```bash
curl http://localhost:3002/api/packages/status/stored
```

---

## Package Journey & Status Flow

### Package Lifecycle
```
1. received      → Package arrives from client
2. inspected     → Quality check performed
3. stored        → Placed in warehouse location
4. picked        → Retrieved for delivery
5. packed        → Prepared for loading
6. loaded        → Loaded onto vehicle
7. in_transit    → Out for delivery
8. delivered     → Successfully delivered
```

### Event History Tracking

Every package maintains a complete audit trail of all events:

```json
"events": [
  {
    "event_type": "received",
    "timestamp": "2026-02-01T08:00:00Z",
    "notes": "Package received from Daraz Lanka"
  },
  {
    "event_type": "inspected",
    "timestamp": "2026-02-01T08:15:00Z",
    "condition": "good",
    "notes": "Electronics - handled with care"
  },
  {
    "event_type": "stored",
    "timestamp": "2026-02-01T08:30:00Z",
    "location": "WH-MAIN-01/A/R5/S2",
    "notes": "Fragile zone"
  },
  {
    "event_type": "picked",
    "timestamp": "2026-02-01T13:00:00Z",
    "notes": "Picked for route RT-001"
  },
  {
    "event_type": "loaded",
    "timestamp": "2026-02-01T13:30:00Z",
    "vehicle_id": "VEH-101",
    "driver_id": "driver-001"
  }
]
```

---

## Tracking Number Format

**Format**: `SLNNNNNN`
- `SL` - Sri Lanka country code
- `NNNNNN` - 6-digit sequential number

**Examples:**
- `SL100001` - First package
- `SL100002` - Second package
- `SL999999` - Maximum capacity (resets after)

---

## Data Models & Schemas

### Package Schema
```python
{
  "id": "uuid",
  "tracking_number": "SL100001",
  "order_id": "order-123",
  "client_id": "client-001",
  "description": "Samsung Galaxy S24 - Electronics",
  "status": "stored",
  "condition": "good",
  "weight": 0.5,
  "dimensions": {
    "length": 20.0,
    "width": 10.0,
    "height": 15.0,
    "unit": "cm"
  },
  "location": {
    "warehouse_id": "WH-MAIN-01",
    "zone": "A",
    "rack": "R5",
    "shelf": "S2"
  },
  "vehicle_id": null,
  "driver_id": null,
  "special_handling": "fragile",
  "events": [...],
  "created_at": "2026-02-01T08:00:00Z",
  "updated_at": "2026-02-01T13:30:00Z"
}
```

### Package Status Values
- `received` - Package received at warehouse
- `inspected` - Quality inspection completed
- `stored` - Placed in warehouse location
- `picked` - Retrieved for delivery
- `packed` - Packed for loading
- `loaded` - Loaded on delivery vehicle
- `in_transit` - Out for delivery
- `delivered` - Successfully delivered

### Package Condition Values
- `good` - Perfect condition
- `fair` - Minor issues
- `damaged` - Significant damage
- `critical` - Severe damage

---

## Setup & Installation

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- Docker (optional)

### Local Development Setup

1. **Navigate to service directory:**
```bash
cd services/mocks/wms-mock
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

The service will start on `http://localhost:3002`

### Docker Deployment

```bash
docker build -t wms-mock-service .
docker run -p 3002:3002 -v $(pwd)/data:/app/data wms-mock-service
```

### Using Docker Compose

From project root:
```bash
docker-compose up wms-mock
```

---

## Configuration

### Environment Variables
```bash
# Service Configuration
APP_NAME="WMS Mock Service"
HOST=0.0.0.0
PORT=3002
DEBUG=true

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Data Storage
DATA_DIR=/app/data

# Tracking Number Configuration
TRACKING_PREFIX=SL
TRACKING_START=100001
```

---

## Business Context & Integration

### Swift Logistics Warehouse Operations

1. **Package Receipt**: E-commerce clients deliver packages to Swift Logistics warehouse
2. **Quality Control**: All packages inspected for damage before acceptance
3. **Storage Management**: Smart warehouse location assignment for efficient picking
4. **Delivery Preparation**: Packages picked and loaded based on route optimization
5. **Real-time Tracking**: Clients track packages via tracking number in SwiftTrack portal

### Integration Points

- **CMS Mock**: Order metadata and client information
- **ROS Mock**: Route optimization and delivery manifest creation
- **WMS Adapter**: Protocol translation (TCP/IP simulation to internal format)
- **Orchestrator**: Workflow coordination between systems
- **Client Portal**: Real-time package tracking display

### High-Volume Event Handling

During promotional events (Black Friday, Avurudu sales):
- Bulk package intake support
- Batch processing capabilities
- Status tracking ensures no lost packages
- Event history provides complete audit trail

---

## Interactive API Documentation

Access interactive API docs when service is running:

- **Swagger UI**: http://localhost:3002/docs
- **Service Info**: http://localhost:3002/
- **Health Check**: http://localhost:3002/health

---

## Testing the Service

### Complete Workflow Test
```bash
# 1. Health check
curl http://localhost:3002/health

# 2. Create a package
PKG_ID=$(curl -X POST http://localhost:3002/api/packages/ \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "order-123",
    "client_id": "daraz-lanka",
    "description": "Samsung Galaxy S24",
    "weight": 0.5,
    "special_handling": "fragile"
  }' | jq -r '.id')

TRACKING=$(curl http://localhost:3002/api/packages/$PKG_ID | jq -r '.tracking_number')
echo "Tracking Number: $TRACKING"

# 3. Inspect package
curl -X POST "http://localhost:3002/api/packages/$PKG_ID/inspect?condition=good"

# 4. Store in warehouse
curl -X POST http://localhost:3002/api/packages/$PKG_ID/store \
  -H "Content-Type: application/json" \
  -d '{"warehouse_id": "WH-MAIN-01", "zone": "A", "rack": "R5", "shelf": "S2"}'

# 5. Pick for delivery
curl -X POST "http://localhost:3002/api/packages/$PKG_ID/pick"

# 6. Load onto vehicle
curl -X POST "http://localhost:3002/api/packages/$PKG_ID/load?vehicle_id=VEH-101&driver_id=driver-001"

# 7. Track package
curl http://localhost:3002/api/packages/tracking/$TRACKING | jq
```

---

## Troubleshooting

### Service won't start
```bash
# Check port availability
lsof -i :3002

# View logs
docker logs wms-mock
```

### Tracking numbers not generating
- Check `TRACKING_START` in `.env`
- Verify data directory has write permissions
- Check package creation logic in logs

### Package events not recording
- Ensure proper status transitions
- Check event logging in service code
- Verify JSON file integrity

---

## Development Notes

### TCP/IP Protocol Simulation
This is a REST simulation of a proprietary TCP/IP messaging protocol:
- Real WMS uses binary protocol over TCP port 5000
- This mock provides HTTP/REST interface for easier integration
- Message format mimics real-time event streaming

### Adding Custom Warehouse Zones
Edit package location schema in `src/models/schemas.py`:
```python
class PackageLocation(BaseModel):
    warehouse_id: str
    zone: str  # A, B, C, D (customizable)
    rack: str
    shelf: str
```

---

## Version History

**Version 2.0.0** (Current)
- ✅ Complete package lifecycle tracking
- ✅ Event history audit trail
- ✅ Tracking number generation (SL format)
- ✅ Warehouse location management
- ✅ Quality inspection workflow
- ✅ Vehicle loading tracking

**Version 1.0.0**
- Basic inventory management
- Simple storage tracking

---

## Support & Documentation

- **API Documentation**: http://localhost:3002/docs
- **Service Port**: 3002
- **Protocol**: HTTP/REST (simulating TCP/IP proprietary protocol)
- **Data Format**: JSON

---

**Last Updated**: February 1, 2026  
**Maintainer**: Swift Logistics Development Team  
**Status**: Production Ready
