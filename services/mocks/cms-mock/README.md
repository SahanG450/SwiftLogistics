# CMS Mock Service - Complete Documentation

## Service Overview

**CMS (Client Management System) Mock Service** simulates a legacy on-premise Client Management System with SOAP-based XML API (REST simulation for development). This service is the heart of Swift Logistics' client interactions, handling order intake, contract management, and billing operations.

### Service Information
- **Service Name**: CMS Mock Service
- **Port**: 3001
- **Version**: 2.0.0
- **Technology**: Python 3.11 + FastAPI
- **API Style**: REST (simulating legacy SOAP-based system)
- **Data Storage**: File-based JSON persistence

### Core Capabilities
1. **Order Intake & Management** - Client portal order submissions
2. **Client Contracts** - Service agreements and pricing tiers
3. **Billing & Invoicing** - Automated billing and payment tracking
4. **Customer Management** - End customer data management
5. **Driver Management** - Driver profiles and assignments

---

## Architecture & File Structure

```
services/mocks/cms-mock/
├── app.py                          # Main FastAPI application
├── Dockerfile                      # Container configuration
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── data/                           # JSON file storage
│   ├── customers.json
│   ├── drivers.json
│   ├── clients.json
│   ├── admins.json
│   ├── orders.json
│   ├── contracts.json
│   └── billing.json
└── src/
    ├── config/
    │   └── settings.py             # Configuration management
    ├── models/
    │   └── schemas.py              # Pydantic data models
    ├── routes/
    │   ├── cms_routes.py           # Customer endpoints
    │   ├── driver_routes.py        # Driver endpoints
    │   ├── client_routes.py        # Client endpoints
    │   ├── admin_routes.py         # Admin endpoints
    │   ├── order_routes.py         # Order management
    │   ├── contract_routes.py      # Contract management
    │   └── billing_routes.py       # Billing & invoicing
    ├── services/
    │   ├── cms_service.py          # Customer business logic
    │   ├── driver_service.py       # Driver business logic
    │   ├── client_service.py       # Client business logic
    │   ├── admin_service.py        # Admin business logic
    │   ├── order_service.py        # Order business logic
    │   ├── contract_service.py     # Contract business logic
    │   └── billing_service.py      # Billing business logic
    └── utils/
        └── file_storage.py         # JSON file persistence utility
```

---

## API Endpoints Reference

### Health & Status Endpoints

#### GET /
**Service Information**
```bash
curl http://localhost:3001/
```
**Response:**
```json
{
  "service": "CMS Mock Service",
  "description": "Client Management System (Legacy SOAP-based - REST simulation)",
  "status": "running",
  "version": "2.0.0",
  "capabilities": [
    "Order Intake & Management",
    "Client Contracts",
    "Billing & Invoicing",
    "Customer Management",
    "Driver Management"
  ]
}
```

#### GET /health
**Health Check with Entity Counts**
```bash
curl http://localhost:3001/health
```
**Response:**
```json
{
  "status": "healthy",
  "service": "CMS Mock Service",
  "version": "2.0.0",
  "entity_counts": {
    "customers": 5,
    "drivers": 3,
    "clients": 10,
    "admins": 2,
    "orders": 150,
    "contracts": 10,
    "invoices": 25
  }
}
```

---

### Order Management Endpoints

#### GET /api/orders/
**Get All Orders with Filtering**
```bash
# Get all orders
curl http://localhost:3001/api/orders/

# Filter by status
curl http://localhost:3001/api/orders/?status=pending

# Filter by client
curl http://localhost:3001/api/orders/?client_id=client-001

# Filter by priority
curl http://localhost:3001/api/orders/?priority=urgent

# Filter by driver
curl http://localhost:3001/api/orders/?driver_id=driver-001
```

#### GET /api/orders/{order_id}
**Get Specific Order**
```bash
curl http://localhost:3001/api/orders/order-123
```

#### POST /api/orders/
**Create New Order (Order Intake)**
```bash
curl -X POST http://localhost:3001/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "client-001",
    "delivery_address": {
      "street": "No. 45, Galle Road",
      "city": "Colombo",
      "province": "Western",
      "postal_code": "00300",
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
        "value": 150000.00
      }
    ],
    "priority": "normal",
    "special_instructions": "Handle with care - fragile electronics"
  }'
```

#### PUT /api/orders/{order_id}
**Update Order**
```bash
curl -X PUT http://localhost:3001/api/orders/order-123 \
  -H "Content-Type: application/json" \
  -d '{"status": "confirmed", "priority": "high"}'
```

#### DELETE /api/orders/{order_id}
**Delete Order**
```bash
curl -X DELETE http://localhost:3001/api/orders/order-123
```

#### POST /api/orders/{order_id}/assign-driver
**Assign Order to Driver**
```bash
curl -X POST "http://localhost:3001/api/orders/order-123/assign-driver?driver_id=driver-001&route_id=route-456"
```

#### POST /api/orders/{order_id}/mark-delivered
**Mark Order as Delivered with Proof**
```bash
curl -X POST http://localhost:3001/api/orders/order-123/mark-delivered \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_name": "Nimal Perera",
    "signature": "data:image/png;base64,iVBORw0KG...",
    "photo": "data:image/jpeg;base64,/9j/4AAQSk...",
    "delivered_at": "2026-02-01T14:30:00Z",
    "notes": "Left at front door as requested"
  }'
```

#### POST /api/orders/{order_id}/mark-failed
**Mark Order as Failed**
```bash
curl -X POST "http://localhost:3001/api/orders/order-123/mark-failed?reason=recipient_unavailable&notes=Called+3+times,+no+answer"
```

#### GET /api/orders/status/{status}
**Get Orders by Status**
```bash
curl http://localhost:3001/api/orders/status/pending
```

---

### Contract Management Endpoints

#### GET /api/contracts/
**Get All Contracts**
```bash
curl http://localhost:3001/api/contracts/
```

#### GET /api/contracts/{contract_id}
**Get Specific Contract**
```bash
curl http://localhost:3001/api/contracts/contract-123
```

#### POST /api/contracts/
**Create New Contract**
```bash
curl -X POST http://localhost:3001/api/contracts/ \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "client-001",
    "contract_type": "tiered",
    "pricing": {
      "base_rate": 250.00,
      "per_delivery": 150.00,
      "tiers": [
        {"min_deliveries": 100, "rate": 140.00},
        {"min_deliveries": 500, "rate": 130.00},
        {"min_deliveries": 1000, "rate": 120.00}
      ]
    },
    "start_date": "2026-02-01",
    "end_date": "2027-02-01",
    "terms": "Monthly billing, 30-day payment terms"
  }'
```

#### PUT /api/contracts/{contract_id}
**Update Contract**
```bash
curl -X PUT http://localhost:3001/api/contracts/contract-123 \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'
```

#### POST /api/contracts/{contract_id}/activate
**Activate Contract**
```bash
curl -X POST http://localhost:3001/api/contracts/contract-123/activate
```

#### POST /api/contracts/{contract_id}/suspend
**Suspend Contract**
```bash
curl -X POST http://localhost:3001/api/contracts/contract-123/suspend
```

---

### Billing & Invoicing Endpoints

#### GET /api/billing/
**Get All Invoices**
```bash
# Get all invoices
curl http://localhost:3001/api/billing/

# Filter by client
curl "http://localhost:3001/api/billing/?client_id=client-001"
```

#### GET /api/billing/{invoice_id}
**Get Specific Invoice**
```bash
curl http://localhost:3001/api/billing/invoice-123
```

#### POST /api/billing/
**Create New Invoice**
```bash
curl -X POST http://localhost:3001/api/billing/ \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "client-001",
    "billing_period": "2026-01",
    "total_deliveries": 1450,
    "successful_deliveries": 1398,
    "failed_deliveries": 52,
    "amount": 185000.00,
    "due_date": "2026-02-28"
  }'
```

#### POST /api/billing/{invoice_id}/record-payment
**Record Payment**
```bash
curl -X POST http://localhost:3001/api/billing/invoice-123/record-payment \
  -H "Content-Type: application/json" \
  -d '{
    "payment_amount": 185000.00,
    "payment_method": "bank_transfer",
    "payment_reference": "TXN-2026-001234",
    "payment_date": "2026-02-15T10:30:00Z"
  }'
```

---

### Customer Management Endpoints

#### GET /api/customers/
**Get All Customers**
```bash
curl http://localhost:3001/api/customers/
```

#### POST /api/customers/
**Create Customer**
```bash
curl -X POST http://localhost:3001/api/customers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nimal Perera",
    "email": "nimal@example.com",
    "phone": "+94771234567",
    "address": "No. 45, Galle Road, Colombo",
    "company": "ABC Traders"
  }'
```

---

### Driver Management Endpoints

#### GET /api/drivers/
**Get All Drivers**
```bash
curl http://localhost:3001/api/drivers/
```

#### POST /api/drivers/
**Create Driver**
```bash
curl -X POST http://localhost:3001/api/drivers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sunil Silva",
    "email": "sunil@swiftlogistics.lk",
    "phone": "+94771234567",
    "license_number": "B1234567",
    "vehicle_id": "VEH-101"
  }'
```

---

## Data Models & Schemas

### Order Schema
```python
{
  "id": "uuid",
  "order_number": "ORD-2026-1001",
  "client_id": "client-001",
  "delivery_address": {
    "street": "No. 45, Galle Road",
    "city": "Colombo",
    "province": "Western",
    "postal_code": "00300",
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
      "value": 150000.00
    }
  ],
  "status": "pending",
  "priority": "normal",
  "assigned_driver_id": null,
  "assigned_route_id": null,
  "proof_of_delivery": null,
  "failure_reason": null,
  "special_instructions": null,
  "created_at": "2026-02-01T10:00:00Z",
  "updated_at": "2026-02-01T10:00:00Z"
}
```

### Order Status Flow
```
pending → confirmed → processing → in_warehouse → 
ready_for_delivery → out_for_delivery → delivered/failed
```

### Priority Levels
- `low` - Standard delivery (3-5 days)
- `normal` - Regular delivery (1-2 days)
- `high` - Priority delivery (same day)
- `urgent` - Express delivery (promotional events like Black Friday, Avurudu)

### Delivery Failure Reasons
- `recipient_unavailable`
- `address_incorrect`
- `refused_delivery`
- `damaged_package`
- `access_denied`
- `other`

### Contract Types
- `monthly` - Fixed monthly fee
- `per_delivery` - Pay per delivery
- `tiered` - Volume-based pricing with discounts

---

## Setup & Installation

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- Docker (optional, for containerized deployment)

### Local Development Setup

1. **Navigate to service directory:**
```bash
cd services/mocks/cms-mock
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

4. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env as needed
```

5. **Run the service:**
```bash
python app.py
```

The service will start on `http://localhost:3001`

### Docker Deployment

1. **Build Docker image:**
```bash
docker build -t cms-mock-service .
```

2. **Run container:**
```bash
docker run -p 3001:3001 -v $(pwd)/data:/app/data cms-mock-service
```

### Using Docker Compose

From the project root:
```bash
docker-compose up cms-mock
```

---

## Configuration

### Environment Variables
```bash
# Service Configuration
APP_NAME="CMS Mock Service"
HOST=0.0.0.0
PORT=3001
DEBUG=true

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Data Storage
DATA_DIR=/app/data
```

---

## Interactive API Documentation

Once the service is running, access interactive API documentation:

- **Swagger UI**: http://localhost:3001/docs
- **Service Info**: http://localhost:3001/
- **Health Check**: http://localhost:3001/health

---

## Testing the Service

### Quick Test Script
```bash
# Health check
curl http://localhost:3001/health

# Create an order
ORDER_ID=$(curl -X POST http://localhost:3001/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "test-client",
    "delivery_address": {
      "street": "123 Test St",
      "city": "Colombo",
      "province": "Western",
      "country": "Sri Lanka"
    },
    "items": [{"sku": "TEST-001", "description": "Test Item", "quantity": 1}]
  }' | jq -r '.id')

# Get the order
curl http://localhost:3001/api/orders/$ORDER_ID

# Update order status
curl -X PUT http://localhost:3001/api/orders/$ORDER_ID \
  -H "Content-Type: application/json" \
  -d '{"status": "confirmed"}'
```

---

## Business Context

### Swift Logistics Use Cases

1. **E-commerce Order Intake**: Large retailers (Daraz, Kapruka) submit bulk orders
2. **Priority Handling**: Urgent deliveries during promotional events (Black Friday, Avurudu sales)
3. **Proof of Delivery**: Digital signatures and photos for accountability
4. **Contract Management**: Different pricing tiers for enterprise vs. SME clients
5. **Automated Billing**: Monthly invoicing based on delivery volumes

### Integration Points

- **API Gateway**: Primary access point for client portal
- **CMS Adapter**: Protocol translation (REST to internal message format)
- **Orchestrator**: Order workflow coordination
- **WMS Mock**: Package tracking linkage via order_id
- **ROS Mock**: Driver assignment and manifest creation

---

## Troubleshooting

### Service won't start
```bash
# Check if port 3001 is already in use
lsof -i :3001

# Check logs
docker logs cms-mock
```

### Data not persisting
- Ensure `/app/data` directory has write permissions
- Check volume mounts in docker-compose.yml
- Verify DATA_DIR environment variable

### CORS errors
- Update `CORS_ORIGINS` in `.env` to include your frontend URL
- Restart the service after changing environment variables

---

## Development Notes

### Adding New Endpoints
1. Create schema in `src/models/schemas.py`
2. Add business logic in `src/services/`
3. Create route in `src/routes/`
4. Register router in `app.py`

### File Storage
- All data is stored as JSON in `/app/data/`
- Each entity type has its own file (orders.json, contracts.json, etc.)
- Files are automatically created on first write
- Data persists across service restarts

---

## Version History

**Version 2.0.0** (Current)
- ✅ Enhanced order management with priority handling
- ✅ Contract management with tiered pricing
- ✅ Billing & invoicing automation
- ✅ Proof of delivery with digital signatures
- ✅ Delivery failure tracking
- ✅ Driver assignment capabilities

**Version 1.0.0**
- Basic customer and driver management
- Simple CRUD operations

---

## Support & Documentation

- **API Documentation**: http://localhost:3001/docs
- **Project Repository**: SwiftLogistics
- **Service Port**: 3001
- **Protocol**: HTTP/REST (simulating legacy SOAP)

---

**Last Updated**: February 1, 2026  
**Maintainer**: Swift Logistics Development Team  
**Status**: Production Ready
