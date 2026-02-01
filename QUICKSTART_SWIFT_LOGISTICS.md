# Swift Logistics Mock Services - Quick Start Guide

## 🚀 Quick Start

### Start All Services

```bash
./scripts/start-swift-logistics.sh
```

### Stop All Services

```bash
./scripts/stop-swift-logistics.sh
```

### Test All Services

```bash
./scripts/test-swift-logistics.sh
```

## 📋 Service Ports

| Service  | Port | Description                                       |
| -------- | ---- | ------------------------------------------------- |
| CMS Mock | 3001 | Client Management System (Legacy SOAP simulation) |
| WMS Mock | 3002 | Warehouse Management System                       |
| ROS Mock | 3003 | Route Optimization System                         |

## 🔗 API Documentation

- **CMS**: http://localhost:3001/docs
- **WMS**: http://localhost:3002/docs
- **ROS**: http://localhost:3003/docs

## 📦 Key Features by Service

### CMS Mock (Port 3001)

**Order Management**

- `POST /api/orders/` - Submit new order (Order Intake)
- `GET /api/orders/` - List all orders
- `GET /api/orders/{id}` - Get order details
- `POST /api/orders/{id}/assign-driver` - Assign to driver
- `POST /api/orders/{id}/mark-delivered` - Mark delivered with proof
- `POST /api/orders/{id}/mark-failed` - Mark failed with reason

**Contract Management**

- `POST /api/contracts/` - Create client contract
- `GET /api/contracts/` - List all contracts
- `POST /api/contracts/{id}/activate` - Activate contract

**Billing & Invoicing**

- `POST /api/billing/` - Create invoice
- `GET /api/billing/` - List invoices
- `POST /api/billing/{id}/record-payment` - Record payment

### WMS Mock (Port 3002)

**Package Tracking**

- `POST /api/packages/` - Receive package from client
- `GET /api/packages/tracking/{number}` - Track by tracking number
- `POST /api/packages/{id}/inspect` - Quality inspection
- `POST /api/packages/{id}/store` - Store in warehouse
- `POST /api/packages/{id}/pick` - Pick for delivery
- `POST /api/packages/{id}/load` - Load onto vehicle

### ROS Mock (Port 3003)

**Delivery Manifests**

- `POST /api/manifests/` - Create delivery manifest
- `GET /api/manifests/?driver_id={id}` - Get driver's manifest
- `POST /api/manifests/{id}/start` - Driver starts route
- `PUT /api/manifests/{id}/deliveries/{oid}` - Update delivery status
- `POST /api/manifests/{id}/complete` - Complete manifest

## 🔄 Typical Workflow

### 1. Client Submits Order

```bash
curl -X POST http://localhost:3001/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "client-001",
    "delivery_address": {
      "street": "No. 45, Galle Road",
      "city": "Colombo",
      "province": "Western",
      "country": "Sri Lanka",
      "contact_name": "Nimal Perera",
      "contact_phone": "+94771234567"
    },
    "items": [
      {
        "sku": "PHONE-001",
        "description": "Samsung Galaxy S24",
        "quantity": 1,
        "weight": 0.5,
        "value": 185000.0
      }
    ],
    "priority": "normal"
  }'
```

### 2. Warehouse Receives Package

```bash
curl -X POST http://localhost:3002/api/packages/ \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "order-001",
    "client_id": "client-001",
    "description": "Samsung Galaxy S24 - Electronics",
    "weight": 0.5,
    "special_handling": "Fragile"
  }'
# Returns: {"tracking_number": "SL100003", ...}
```

### 3. Inspect and Store Package

```bash
# Inspect
curl -X POST "http://localhost:3002/api/packages/{id}/inspect?condition=good&notes=Quality+check+passed"

# Store in warehouse
curl -X POST http://localhost:3002/api/packages/{id}/store \
  -H "Content-Type: application/json" \
  -d '{
    "warehouse_id": "WH-MAIN-01",
    "zone": "A",
    "rack": "R5",
    "shelf": "S3"
  }'
```

### 4. Create Delivery Manifest

```bash
curl -X POST http://localhost:3003/api/manifests/ \
  -H "Content-Type: application/json" \
  -d '{
    "driver_id": "driver-001",
    "vehicle_id": "VEH-101",
    "route_id": "route-001",
    "delivery_date": "2026-02-02",
    "deliveries": [
      {
        "order_id": "order-001",
        "package_id": "pkg-001",
        "tracking_number": "SL100003",
        "recipient_name": "Nimal Perera",
        "delivery_address": "No. 45, Galle Road, Colombo 03",
        "contact_phone": "+94771234567",
        "priority": "normal"
      }
    ]
  }'
```

### 5. Driver Starts Delivery

```bash
# Driver starts manifest
curl -X POST http://localhost:3003/api/manifests/{id}/start

# Driver marks package as delivered
curl -X POST http://localhost:3001/api/orders/{order_id}/mark-delivered \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_name": "Nimal Perera",
    "delivered_at": "2026-02-02T10:30:00",
    "signature_url": "https://example.com/signature.png",
    "notes": "Delivered successfully"
  }'
```

### 6. Track Package

```bash
# By tracking number
curl http://localhost:3002/api/packages/tracking/SL100003

# By order ID
curl http://localhost:3001/api/orders/{order_id}
```

## 📊 Data Formats

### Order Numbers

- Format: `ORD-YYYY-NNNN`
- Example: `ORD-2026-1001`

### Tracking Numbers

- Format: `SLNNNNNN`
- Example: `SL100001`

### Manifest Numbers

- Format: `MAN-YYYY-NNNN`
- Example: `MAN-2026-2001`

### Contract Numbers

- Format: `CON-NNNN`
- Example: `CON-5001`

### Invoice Numbers

- Format: `INV-YYYY-NNNNN`
- Example: `INV-2026-10001`

## 🎯 SwiftTrack Platform Features

### Client Portal

✅ Submit orders
✅ Track deliveries in real-time
✅ View order history
✅ Check billing status

### Driver Mobile App

✅ View daily manifest
✅ See optimized route
✅ Mark deliveries as completed
✅ Upload proof of delivery
✅ Report delivery failures

## 🔍 Filter Examples

### Get Orders by Status

```bash
curl "http://localhost:3001/api/orders/?status=ready_for_delivery"
```

### Get Orders by Client

```bash
curl "http://localhost:3001/api/orders/?client_id=client-001"
```

### Get Driver's Manifest

```bash
curl "http://localhost:3003/api/manifests/?driver_id=driver-001"
```

### Get Packages by Status

```bash
curl "http://localhost:3002/api/packages/?status=stored"
```

## 🚨 Priority Levels

- `low` - Regular delivery
- `normal` - Standard delivery
- `high` - Important delivery
- `urgent` - Critical (promotional events like Black Friday, Avurudu)

## 📈 Order Status Flow

```
pending → confirmed → processing → in_warehouse →
ready_for_delivery → out_for_delivery → delivered/failed
```

## 📦 Package Status Flow

```
received → inspected → stored → picked →
packed → loaded → in_transit → delivered
```

## 🚛 Manifest Status Flow

```
draft → assigned → in_progress → completed
```

## 🔧 Troubleshooting

### Check Service Status

```bash
curl http://localhost:3001/health
curl http://localhost:3002/health
curl http://localhost:3003/health
```

### View Logs

```bash
tail -f /tmp/cms-mock.log
tail -f /tmp/wms-mock.log
tail -f /tmp/ros-mock.log
```

### Restart Services

```bash
./scripts/stop-swift-logistics.sh
./scripts/start-swift-logistics.sh
```

## 📚 Additional Documentation

- Full API Reference: `SWIFT_LOGISTICS_MOCK_SERVICES.md`
- CMS Details: `doc/CMS_MOCK_SERVICE.md`
- Architecture: `doc/ARCHITECTURE.md`

---

**Version**: 2.0.0  
**Last Updated**: February 1, 2026  
**Status**: Production Ready for Development
