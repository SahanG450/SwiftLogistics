# Swift Logistics Mock Services - Enhanced for Business Requirements

## Overview

The mock services have been enhanced to align with Swift Logistics (Pvt) Ltd.'s business requirements as a last-mile delivery company serving e-commerce businesses in Sri Lanka.

## Business Context

**Swift Logistics** specializes in:
- Last-mile delivery for e-commerce businesses
- Serving clients from large online retailers to small independent sellers
- Replacing siloed, manual systems with integrated "SwiftTrack" platform
- Web-based portal for clients and mobile app for drivers

## Enhanced Mock Services

### 1. CMS Mock Service (Port 3001)
**Simulates**: Legacy on-premise Client Management System with SOAP-based XML API (REST simulation for development)

#### New Capabilities Added:

**A. Order Management** (`/api/orders`)
- ✅ **Order Intake**: Clients submit orders through portal
- ✅ **Order Tracking**: Real-time order status tracking
- ✅ **Priority Handling**: Support for urgent deliveries (Black Friday, Avurudu sales)
- ✅ **Proof of Delivery**: Digital signatures and photos
- ✅ **Failure Tracking**: Reasons for failed deliveries

**Order Statuses**:
- `pending` → `confirmed` → `processing` → `in_warehouse` → `ready_for_delivery` → `out_for_delivery` → `delivered`/`failed`

**Priority Levels**:
- `low`, `normal`, `high`, `urgent` (for promotional events)

**Endpoints**:
```
GET    /api/orders/                    # Get all orders (filterable)
GET    /api/orders/{id}                # Get specific order
POST   /api/orders/                    # Create order (intake)
PUT    /api/orders/{id}                # Update order
DELETE /api/orders/{id}                # Delete order
POST   /api/orders/{id}/assign-driver  # Assign to driver
POST   /api/orders/{id}/mark-delivered # Mark as delivered with proof
POST   /api/orders/{id}/mark-failed    # Mark as failed with reason
```

**B. Contract Management** (`/api/contracts`)
- ✅ **Client Contracts**: Manage delivery contracts with e-commerce clients
- ✅ **Pricing Tiers**: Different rates for different client types
- ✅ **Volume Discounts**: Automatic discounts for high-volume clients

**Contract Types**:
- `monthly`: Fixed monthly fee
- `per_delivery`: Pay per delivery
- `tiered`: Volume-based pricing

**Endpoints**:
```
GET    /api/contracts/            # Get all contracts
GET    /api/contracts/{id}        # Get specific contract
POST   /api/contracts/            # Create contract
PUT    /api/contracts/{id}        # Update contract
POST   /api/contracts/{id}/activate   # Activate contract
POST   /api/contracts/{id}/suspend    # Suspend contract
```

**C. Billing & Invoicing** (`/api/billing`)
- ✅ **Automated Billing**: Calculate billing based on contracts
- ✅ **Payment Tracking**: Track payments from clients
- ✅ **Delivery Metrics**: Successful vs. failed deliveries

**Endpoints**:
```
GET    /api/billing/                          # Get all invoices
GET    /api/billing/{id}                      # Get specific invoice
POST   /api/billing/                          # Create invoice
POST   /api/billing/{id}/record-payment       # Record payment
```

### 2. WMS Mock Service (Port 3002)
**Simulates**: Warehouse Management System with proprietary TCP/IP messaging (REST simulation)

#### New Capabilities Added:

**A. Package Tracking** (`/api/packages`)
- ✅ **Receipt Tracking**: Track packages from client arrival
- ✅ **Quality Inspection**: Inspect package condition
- ✅ **Warehouse Storage**: Assign warehouse locations
- ✅ **Loading Process**: Track loading onto vehicles
- ✅ **Event History**: Complete audit trail

**Package Journey**:
1. `received` - Package arrives from client
2. `inspected` - Quality check performed
3. `stored` - Placed in warehouse location
4. `picked` - Retrieved for delivery
5. `packed` - Prepared for loading
6. `loaded` - Loaded onto vehicle
7. `in_transit` → `delivered`

**Endpoints**:
```
GET    /api/packages/                     # Get all packages
GET    /api/packages/{id}                 # Get specific package
GET    /api/packages/tracking/{number}    # Track by tracking number
POST   /api/packages/                     # Receive package
POST   /api/packages/{id}/inspect         # Inspect package
POST   /api/packages/{id}/store           # Store in warehouse
POST   /api/packages/{id}/pick            # Pick for delivery
POST   /api/packages/{id}/load            # Load onto vehicle
```

**Tracking Numbers**: `SLNNNNNN` format (e.g., SL100001)

### 3. ROS Mock Service (Port 3003)
**Simulates**: Modern cloud-based Route Optimization System with RESTful API

#### New Capabilities Added:

**A. Delivery Manifests** (`/api/manifests`)
- ✅ **Driver Manifests**: Daily delivery lists for drivers
- ✅ **Optimized Routes**: Sequenced delivery stops
- ✅ **Real-time Updates**: Route changes and priority deliveries
- ✅ **Delivery Tracking**: Track each delivery in manifest

**Manifest Features**:
- Delivery sequence optimization
- Estimated delivery times
- GPS coordinates for each stop
- Priority delivery handling
- Real-time status updates

**Endpoints**:
```
GET    /api/manifests/                        # Get all manifests
GET    /api/manifests/{id}                    # Get specific manifest
POST   /api/manifests/                        # Create manifest
POST   /api/manifests/{id}/assign             # Assign to driver
POST   /api/manifests/{id}/start              # Driver starts route
POST   /api/manifests/{id}/complete           # Complete route
PUT    /api/manifests/{id}/deliveries/{oid}   # Update delivery status
```

**Manifest Number Format**: `MAN-YYYY-NNNN` (e.g., MAN-2026-2001)

## SwiftTrack Platform Features Support

### Client Portal Capabilities
✅ **Order Submission**: POST `/api/orders/`
✅ **Order Status**: GET `/api/orders/{id}`
✅ **Real-time Tracking**: GET `/api/packages/tracking/{number}`
✅ **Delivery History**: GET `/api/orders?client_id=...`
✅ **Billing Information**: GET `/api/billing?client_id=...`

### Driver Mobile App Capabilities
✅ **View Manifest**: GET `/api/manifests?driver_id=...`
✅ **Optimized Route**: Manifest includes sequenced deliveries
✅ **Start Route**: POST `/api/manifests/{id}/start`
✅ **Mark Delivered**: POST `/api/orders/{id}/mark-delivered` (with signature/photo)
✅ **Mark Failed**: POST `/api/orders/{id}/mark-failed` (with reason)
✅ **Real-time Updates**: PUT `/api/manifests/{id}/deliveries/{oid}`

### High-Volume Event Handling
✅ **Priority Orders**: `urgent` priority level
✅ **Bulk Order Intake**: Multiple orders can be submitted
✅ **Order Queue Management**: Status tracking ensures no lost orders
✅ **Scalable Storage**: File-based persistence survives service restarts

## Data Models

### Order Model
```json
{
  "id": "uuid",
  "order_number": "ORD-2026-1001",
  "client_id": "client-001",
  "delivery_address": {
    "street": "No. 45, Galle Road",
    "city": "Colombo",
    "province": "Western",
    "country": "Sri Lanka",
    "contact_name": "Nimal Perera",
    "contact_phone": "+94771234567"
  },
  "items": [...],
  "status": "ready_for_delivery",
  "priority": "normal",
  "assigned_driver_id": null,
  "proof_of_delivery": null
}
```

### Package Model
```json
{
  "id": "uuid",
  "tracking_number": "SL100001",
  "order_id": "order-001",
  "status": "stored",
  "condition": "good",
  "location": {
    "warehouse_id": "WH-MAIN-01",
    "zone": "A",
    "rack": "R5"
  },
  "events": [
    {"event_type": "received", "timestamp": "..."},
    {"event_type": "inspected", "timestamp": "..."}
  ]
}
```

### Delivery Manifest Model
```json
{
  "id": "uuid",
  "manifest_number": "MAN-2026-2001",
  "driver_id": "driver-001",
  "vehicle_id": "VEH-101",
  "deliveries": [
    {
      "order_id": "order-001",
      "tracking_number": "SL100001",
      "recipient_name": "Nimal Perera",
      "delivery_address": "...",
      "coordinates": {"latitude": 6.9271, "longitude": 79.8612},
      "priority": "normal",
      "status": "pending"
    }
  ],
  "total_deliveries": 2,
  "completed_deliveries": 0
}
```

## File Storage

All data persists to JSON files:
```
services/mocks/cms-mock/data/
  ├── customers.json
  ├── drivers.json
  ├── clients.json
  ├── admins.json
  ├── orders.json         # NEW
  ├── contracts.json      # NEW
  └── billing.json        # NEW

services/mocks/wms-mock/data/
  ├── inventory.json
  └── packages.json       # NEW

services/mocks/ros-mock/data/
  ├── routes.json
  └── manifests.json      # NEW
```

## Typical Workflow

### 1. Client Submits Order
```bash
POST /api/orders/
{
  "client_id": "daraz-lanka",
  "delivery_address": {...},
  "items": [...],
  "priority": "normal"
}
```

### 2. Warehouse Receives Package
```bash
POST /api/packages/
{
  "order_id": "order-001",
  "client_id": "daraz-lanka",
  "description": "Samsung Galaxy S24"
}
# Returns: tracking_number = "SL100001"
```

### 3. Package Processed
```bash
POST /api/packages/{id}/inspect  # Quality check
POST /api/packages/{id}/store    # Store in warehouse
```

### 4. Route Optimization
```bash
POST /api/manifests/
{
  "driver_id": "driver-001",
  "vehicle_id": "VEH-101",
  "deliveries": [...]
}
```

### 5. Driver Delivers
```bash
POST /api/manifests/{id}/start          # Driver starts
POST /api/orders/{id}/mark-delivered    # Mark delivered with proof
```

### 6. Billing
```bash
POST /api/billing/
{
  "client_id": "daraz-lanka",
  "total_deliveries": 1450,
  "successful_deliveries": 1398
}
```

## Testing the Services

### Start all services:
```bash
cd services/mocks

# Start CMS
cd cms-mock && python app.py &

# Start WMS
cd ../wms-mock && python app.py &

# Start ROS
cd ../ros-mock && python app.py &
```

### Test endpoints:
```bash
# Check health
curl http://localhost:3001/health  # CMS
curl http://localhost:3002/health  # WMS
curl http://localhost:3003/health  # ROS

# Create an order
curl -X POST http://localhost:3001/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "client-001",
    "delivery_address": {
      "street": "123 Main St",
      "city": "Colombo",
      "province": "Western",
      "country": "Sri Lanka"
    },
    "items": [
      {"sku": "PHONE-001", "description": "Phone", "quantity": 1}
    ]
  }'

# Track a package
curl http://localhost:3002/api/packages/tracking/SL100001

# View driver manifest
curl "http://localhost:3003/api/manifests?driver_id=driver-001"
```

## API Documentation

Interactive API docs available at:
- **CMS**: http://localhost:3001/docs
- **WMS**: http://localhost:3002/docs
- **ROS**: http://localhost:3003/docs

## Summary of Changes

### Files Created:
1. **CMS Mock**:
   - `src/services/order_service.py`
   - `src/services/contract_service.py`
   - `src/services/billing_service.py`
   - `src/routes/order_routes.py`
   - `src/routes/contract_routes.py`
   - `src/routes/billing_routes.py`

2. **WMS Mock**:
   - `src/services/package_service.py`
   - `src/routes/package_routes.py`

3. **ROS Mock**:
   - `src/services/manifest_service.py`
   - `src/routes/manifest_routes.py`

### Files Modified:
1. **CMS Mock**:
   - `src/models/schemas.py` - Added order, contract, billing schemas
   - `app.py` - Included new routers

2. **WMS Mock**:
   - `src/models/schemas.py` - Added package tracking schemas
   - `app.py` - Included package router

3. **ROS Mock**:
   - `src/models/schemas.py` - Added manifest schemas
   - `app.py` - Included manifest router

## Next Steps

1. **Integration Testing**: Test complete order flow across all three services
2. **Middleware Development**: Build adapters to integrate these mock services
3. **Real-time Updates**: Add WebSocket support for driver app updates
4. **Message Queue**: Implement reliable order processing with queue system
5. **Authentication**: Add proper auth for production deployment

---

**Version**: 2.0.0  
**Last Updated**: February 1, 2026  
**Status**: Enhanced for Swift Logistics Business Requirements
