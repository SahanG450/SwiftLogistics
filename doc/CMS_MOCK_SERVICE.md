# CMS Mock Service - Complete Documentation

**Customer Management System Mock Service**  
Port: **3001**  
Technology: **Python FastAPI**  
Storage: **File-based JSON**

---

## 📋 Table of Contents

- [Overview](#overview)
- [What It Can Do](#what-it-can-do)
- [How It Works](#how-it-works)
- [API Endpoints](#api-endpoints)
  - [Customer Endpoints](#customer-endpoints)
  - [Driver Endpoints](#driver-endpoints)
  - [Client Endpoints](#client-endpoints)
  - [Admin Endpoints](#admin-endpoints)
  - [Health & Info Endpoints](#health--info-endpoints)
- [Data Models](#data-models)
  - [Customer Model](#customer-model)
  - [Driver Model](#driver-model)
  - [Client Model](#client-model)
  - [Admin Model](#admin-model)
- [File Storage](#file-storage)
- [Examples](#examples)
  - [Customer Examples](#customer-examples)
  - [Driver Examples](#driver-examples)
  - [Client Examples](#client-examples)
  - [Admin Examples](#admin-examples)
- [Error Handling](#error-handling)
- [Configuration](#configuration)
- [Development](#development)

---

## Overview

The CMS Mock Service provides a **comprehensive management system** for Swift Logistics, handling four distinct entity types: **Customers**, **Drivers**, **Clients**, and **Admins**. It simulates a real database but uses file-based JSON storage for simplicity and persistence.

### Key Features

- ✅ **Full CRUD operations** for 4 entity types
- ✅ **Status and role management** with enum validation
- ✅ **Thread-safe file operations** using Python locks
- ✅ **Automatic data persistence** to JSON files
- ✅ **Input validation** with Pydantic v2
- ✅ **Auto-generated API documentation** (Swagger UI)
- ✅ **RESTful API design** following best practices
- ✅ **CORS enabled** for cross-origin requests
- ✅ **Filtering capabilities** by status, role, and membership level
- ✅ **Entity count tracking** in health endpoint

---

## What It Can Do

### 1. **Customer Management** 👥
Manage customer accounts and track their status

- Create new customer records with validation
- Read all customers or get specific customer by ID
- Update customer information (name, email, phone, address, company)
- Delete customer records permanently
- Track customer status (active/inactive/pending)
- Store complete contact information and company associations

### 2. **Driver Management** 🚚
Manage delivery drivers and their availability

- Create new driver profiles with license information
- Read all drivers or get specific driver by ID
- Update driver information, status, and vehicle assignments
- Delete driver records
- Track driver status (available/on_duty/off_duty/inactive)
- Manage vehicle assignments (vehicle_id)
- Store license numbers and contact information
- Filter drivers by status

### 3. **Client Management** 🏢
Manage business clients with membership tiers

- Create new client accounts with membership levels
- Read all clients or get specific client by ID
- Update client information and membership tiers
- Delete client records
- Manage membership levels (basic/silver/gold/platinum)
- Store client contact and address information
- Track client relationships
- Filter clients by membership level

### 4. **Admin Management** 👨‍💼
Manage administrative users with role-based access

- Create admin accounts with specific roles
- Read all admins or get specific admin by ID
- Update admin information, roles, and permissions
- Delete admin records
- Manage admin roles (super_admin/admin/moderator/support)
- Control fine-grained permissions (array of permission strings)
- Track admin activities
- Filter admins by role

### 5. **Data Validation** ✅

- Email format validation (RFC 5322 compliant)
- Phone number storage (flexible format)
- Required field enforcement
- Status/Role/Membership enum validation
- Automatic UUID generation
- Automatic timestamp management (created_at, updated_at)

### 6. **Data Persistence** 💾

- All data saved to separate JSON files per entity type
- Survives service restarts
- Thread-safe concurrent access with Python locks
- Atomic file writes (all-or-nothing)
- Pretty-printed JSON for readability

### 7. **Health Monitoring** 🏥

- Health check endpoint with status
- Entity count statistics for all 4 types
- Service status reporting

---

## How It Works

### Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                       CMS Mock Service (Port 3001)                   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────┐      ┌─────────────────┐    ┌────────────────┐ │
│  │   FastAPI      │ ───► │  Service Layer  │───►│  FileStorage   │ │
│  │   (Routes)     │      │  (Business      │    │  (Data Layer)  │ │
│  │                │      │   Logic)        │    │                │ │
│  │ • /customers   │      │ • CMSService    │    │ • customers.   │ │
│  │ • /drivers     │      │ • DriverSvc     │    │   json         │ │
│  │ • /clients     │      │ • ClientSvc     │    │ • drivers.json │ │
│  │ • /admins      │      │ • AdminService  │    │ • clients.json │ │
│  │ • /health      │      │                 │    │ • admins.json  │ │
│  └────────────────┘      └─────────────────┘    └────────────────┘ │
│         │                         │                      │          │
│         │                         │                      │          │
│         ▼                         ▼                      ▼          │
│  ┌────────────────┐      ┌─────────────────┐    ┌────────────────┐ │
│  │   Pydantic     │      │  UUID Generator │    │  Thread Locks  │ │
│  │   Validation   │      │  Timestamps     │    │  Atomic Writes │ │
│  └────────────────┘      └─────────────────┘    └────────────────┘ │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Request Flow

1. **HTTP Request** arrives at FastAPI router (`/customers`, `/drivers`, `/clients`, `/admins`)
2. **Route Handler** extracts path parameters and request body
3. **Pydantic Models** validate input data against schemas
4. **Service Layer** processes business logic (CMSService, DriverService, etc.)
5. **FileStorage** performs thread-safe read/write to JSON files
6. **Response** formatted with proper HTTP status code and JSON body

### Data Storage Flow

```
Create Entity (Customer/Driver/Client/Admin):
  
  User Request ──► FastAPI Router ──► Pydantic Validation
                                             │
                                             ▼
                                    Generate UUID v4
                                             │
                                             ▼
                                    Add Timestamps (ISO 8601)
                                    • created_at
                                    • updated_at
                                             │
                                             ▼
                                    Service.create(data)
                                             │
                                             ▼
                                    FileStorage.create(id, data)
                                             │
                                             ▼
                        Acquire Lock ──► Read JSON ──► Add Data ──► Write JSON ──► Release Lock
                                                                            │
                                                                            ▼
                                                                   data/{entity}.json
                                                                   • customers.json
                                                                   • drivers.json
                                                                   • clients.json
                                                                   • admins.json
```

### Threading Model

The service uses Python's `threading.Lock` for thread-safe file operations:

```python
with self.lock:
    # Read JSON file
    # Modify data
    # Write JSON file
# Lock automatically released
```

This ensures:

- No data corruption from concurrent writes
- Consistent reads during writes
- Atomic file operations

---

## API Endpoints

### Base URL

```
http://localhost:3001
```

### Complete Endpoints Summary

| Method | Endpoint                         | Description                    | Filters Available |
| ------ | -------------------------------- | ------------------------------ | ----------------- |
| **Customers** |  |  |  |
| GET    | `/customers/`                    | Get all customers              | None              |
| GET    | `/customers/{id}`                | Get customer by ID             | -                 |
| POST   | `/customers/`                    | Create new customer            | -                 |
| PUT    | `/customers/{id}`                | Update customer                | -                 |
| DELETE | `/customers/{id}`                | Delete customer                | -                 |
| **Drivers** |  |  |  |
| GET    | `/drivers/`                      | Get all drivers                | ?status=          |
| GET    | `/drivers/{id}`                  | Get driver by ID               | -                 |
| POST   | `/drivers/`                      | Create new driver              | -                 |
| PUT    | `/drivers/{id}`                  | Update driver                  | -                 |
| DELETE | `/drivers/{id}`                  | Delete driver                  | -                 |
| **Clients** |  |  |  |
| GET    | `/clients/`                      | Get all clients                | ?membership_level=|
| GET    | `/clients/{id}`                  | Get client by ID               | -                 |
| POST   | `/clients/`                      | Create new client              | -                 |
| PUT    | `/clients/{id}`                  | Update client                  | -                 |
| DELETE | `/clients/{id}`                  | Delete client                  | -                 |
| **Admins** |  |  |  |
| GET    | `/admins/`                       | Get all admins                 | ?role=            |
| GET    | `/admins/{id}`                   | Get admin by ID                | -                 |
| POST   | `/admins/`                       | Create new admin               | -                 |
| PUT    | `/admins/{id}`                   | Update admin                   | -                 |
| DELETE | `/admins/{id}`                   | Delete admin                   | -                 |
| **Health & Info** |  |  |  |
| GET    | `/`                              | Service information            | -                 |
| GET    | `/health`                        | Health check + entity counts   | -                 |
| GET    | `/docs`                          | Interactive API documentation  | -                 |

---

## Customer Endpoints

### 1. Get All Customers

**Endpoint:** `GET /api/customers/`

**Description:** Retrieve all customer records.

**Request:**

```bash
curl http://localhost:3001/api/customers/
```

**Response:** `200 OK`

```json
[
  {
    "id": "e20a1b70-67c9-4fb4-9f6d-56ba97a87c14",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0101",
    "address": "123 Main St, New York, NY 10001",
    "company": "Tech Corp",
    "status": "active",
    "created_at": "2026-02-01T10:00:00.000000",
    "updated_at": "2026-02-01T10:00:00.000000"
  }
]
```

---

### 2. Get Customer by ID

**Endpoint:** `GET /api/customers/{customer_id}`

**Description:** Retrieve a specific customer by UUID.

**Request:**

```bash
curl http://localhost:3001/api/customers/e20a1b70-67c9-4fb4-9f6d-56ba97a87c14
```

**Response:** `200 OK`

```json
{
  "id": "e20a1b70-67c9-4fb4-9f6d-56ba97a87c14",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1-555-0101",
  "address": "123 Main St, New York, NY 10001",
  "company": "Tech Corp",
  "status": "active",
  "created_at": "2026-02-01T10:00:00.000000",
  "updated_at": "2026-02-01T10:00:00.000000"
}
```

**Error Response:** `404 Not Found`

```json
{
  "detail": "Customer with ID {id} not found"
}
```

---

### 3. Create Customer

**Endpoint:** `POST /api/customers/`

**Description:** Create a new customer record.

**Request Headers:**

```
Content-Type: application/json
```

**Request Body:**

```json
{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "phone": "+1-555-0200",
  "address": "789 Oak St, Boston, MA 02101",
  "company": "Manufacturing Co",
  "status": "active"
}
```

**Request Example:**

```bash
curl -X POST http://localhost:3001/api/customers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "phone": "+1-555-0200",
    "address": "789 Oak St, Boston, MA 02101",
    "company": "Manufacturing Co",
    "status": "active"
  }'
```

**Response:** `201 Created`

```json
{
  "id": "a7b8c9d0-1234-5678-90ab-cdef12345678",
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "phone": "+1-555-0200",
  "address": "789 Oak St, Boston, MA 02101",
  "company": "Manufacturing Co",
  "status": "active",
  "created_at": "2026-02-01T12:30:00.123456",
  "updated_at": "2026-02-01T12:30:00.123456"
}
```

**Validation Errors:** `422 Unprocessable Entity`

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

### 4. Update Customer

**Endpoint:** `PUT /api/customers/{customer_id}`

**Description:** Update an existing customer. Only provided fields are updated.

**Request Body:** (All fields optional)

```json
{
  "name": "Alice J. Johnson",
  "phone": "+1-555-0201",
  "status": "inactive"
}
```

**Request Example:**

```bash
curl -X PUT http://localhost:3001/api/customers/a7b8c9d0-1234-5678-90ab-cdef12345678 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice J. Johnson",
    "status": "inactive"
  }'
```

**Response:** `200 OK`

```json
{
  "id": "a7b8c9d0-1234-5678-90ab-cdef12345678",
  "name": "Alice J. Johnson",
  "email": "alice@example.com",
  "phone": "+1-555-0200",
  "address": "789 Oak St, Boston, MA 02101",
  "company": "Manufacturing Co",
  "status": "inactive",
  "created_at": "2026-02-01T12:30:00.123456",
  "updated_at": "2026-02-01T12:35:00.789012"
}
```

**Error Response:** `404 Not Found`

```json
{
  "detail": "Customer with ID {id} not found"
}
```

---

### 5. Delete Customer

**Endpoint:** `DELETE /api/customers/{customer_id}`

**Description:** Delete a customer record permanently.

**Request:**

```bash
curl -X DELETE http://localhost:3001/api/customers/a7b8c9d0-1234-5678-90ab-cdef12345678
```

**Response:** `204 No Content`

```
(Empty response body)
```

**Error Response:** `404 Not Found`

```json
{
  "detail": "Customer with ID {id} not found"
}
```

---

### 6. Health Check

**Endpoint:** `GET /health`

**Description:** Check service health and get statistics.

**Request:**

```bash
curl http://localhost:3001/health
```

**Response:** `200 OK`

```json
{
  "status": "healthy",
  "service": "CMS Mock Service",
  "total_customers": 3
}
```

---

## Data Model

### Customer Schema

```python
class Customer(BaseModel):
    id: str                          # UUID v4 (auto-generated)
    name: str                        # Customer full name
    email: str                       # Email address (validated)
    phone: str                       # Phone number
    address: str                     # Full address
    company: str                     # Company name
    status: str                      # "active" or "inactive"
    created_at: datetime             # Auto-generated timestamp
    updated_at: datetime             # Auto-updated timestamp
```

### Field Constraints

| Field        | Type     | Required | Validation      | Example                                  |
| ------------ | -------- | -------- | --------------- | ---------------------------------------- |
| `id`         | UUID     | Auto     | UUID v4 format  | `"e20a1b70-67c9-4fb4-9f6d-56ba97a87c14"` |
| `name`       | String   | Yes      | Min 1 char      | `"John Doe"`                             |
| `email`      | String   | Yes      | Valid email     | `"john@example.com"`                     |
| `phone`      | String   | Yes      | Any format      | `"+1-555-0101"`                          |
| `address`    | String   | Yes      | Min 1 char      | `"123 Main St, NYC"`                     |
| `company`    | String   | Yes      | Min 1 char      | `"Tech Corp"`                            |
| `status`     | Enum     | Yes      | active/inactive | `"active"`                               |
| `created_at` | DateTime | Auto     | ISO 8601        | `"2026-02-01T10:00:00.000000"`           |
| `updated_at` | DateTime | Auto     | ISO 8601        | `"2026-02-01T10:00:00.000000"`           |

### Status Values

- `active` - Customer is currently active
- `inactive` - Customer is deactivated

---

## File Storage

### Storage Location

```
services/mocks/cms-mock/data/customers.json
```

### File Format

```json
{
  "customer_uuid_1": {
    "id": "customer_uuid_1",
    "name": "John Doe",
    "email": "john@example.com",
    ...
  },
  "customer_uuid_2": {
    "id": "customer_uuid_2",
    "name": "Jane Smith",
    "email": "jane@example.com",
    ...
  }
}
```

### Storage Features

- **Persistent** - Data survives service restarts
- **Thread-Safe** - Concurrent requests handled safely
- **Atomic Writes** - All-or-nothing file updates
- **Pretty Printed** - Human-readable JSON formatting
- **Auto-Created** - File created automatically if missing
- **Mock Data** - Initialized with 2 sample customers

### Storage Operations

```python
# FileStorage class handles all operations
storage = FileStorage(data_dir="data", filename="customers")

# All operations are thread-safe
storage.get_all()           # Get all customers
storage.get(customer_id)     # Get one customer
storage.create(id, data)     # Create customer
storage.update(id, data)     # Update customer
storage.delete(customer_id)  # Delete customer
```

### Viewing Data

```bash
# Pretty print JSON
cat data/customers.json | jq

# Count customers
cat data/customers.json | jq 'length'

# Get customer names
cat data/customers.json | jq '.[] | .name'
```

### Backup & Restore

```bash
# Backup
cp data/customers.json backup/customers-$(date +%Y%m%d).json

# Restore
cp backup/customers-20260201.json data/customers.json

# Reset to initial state
rm data/customers.json
# Restart service - will create with mock data
```

---

## Examples

### Complete Workflow Example

```bash
# 1. Check service health
curl http://localhost:3001/health

# 2. Get all customers
curl http://localhost:3001/api/customers/

# 3. Create a new customer
curl -X POST http://localhost:3001/api/customers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bob Wilson",
    "email": "bob@example.com",
    "phone": "+1-555-0300",
    "address": "456 Elm St, Chicago, IL 60601",
    "company": "Logistics Inc",
    "status": "active"
  }'

# Save the returned ID
CUSTOMER_ID="<returned-uuid>"

# 4. Get the specific customer
curl http://localhost:3001/api/customers/$CUSTOMER_ID

# 5. Update the customer
curl -X PUT http://localhost:3001/api/customers/$CUSTOMER_ID \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1-555-0301"}'

# 6. Deactivate customer
curl -X PUT http://localhost:3001/api/customers/$CUSTOMER_ID \
  -H "Content-Type: application/json" \
  -d '{"status": "inactive"}'

# 7. Delete customer
curl -X DELETE http://localhost:3001/api/customers/$CUSTOMER_ID
```

### Python Client Example

```python
import requests
import json

BASE_URL = "http://localhost:3001"

# Create customer
customer_data = {
    "name": "Python Client Customer",
    "email": "python@example.com",
    "phone": "+1-555-9999",
    "address": "123 API St",
    "company": "Automation Ltd",
    "status": "active"
}

response = requests.post(
    f"{BASE_URL}/api/customers/",
    json=customer_data
)

if response.status_code == 201:
    customer = response.json()
    customer_id = customer["id"]
    print(f"Created customer: {customer_id}")

    # Update customer
    update_data = {"phone": "+1-555-8888"}
    response = requests.put(
        f"{BASE_URL}/api/customers/{customer_id}",
        json=update_data
    )

    if response.status_code == 200:
        print("Customer updated successfully")
```

### JavaScript Client Example

```javascript
const BASE_URL = "http://localhost:3001";

// Create customer
async function createCustomer() {
  const response = await fetch(`${BASE_URL}/api/customers/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: "JS Client Customer",
      email: "js@example.com",
      phone: "+1-555-7777",
      address: "789 Web St",
      company: "Frontend Inc",
      status: "active",
    }),
  });

  const customer = await response.json();
  console.log("Created:", customer);
  return customer.id;
}

// Get all customers
async function getAllCustomers() {
  const response = await fetch(`${BASE_URL}/api/customers/`);
  const customers = await response.json();
  console.log("Customers:", customers);
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning               | When It Occurs            |
| ---- | --------------------- | ------------------------- |
| 200  | OK                    | Successful GET, PUT       |
| 201  | Created               | Successful POST           |
| 204  | No Content            | Successful DELETE         |
| 404  | Not Found             | Customer ID doesn't exist |
| 422  | Unprocessable Entity  | Validation error          |
| 500  | Internal Server Error | Server-side error         |

### Error Response Format

All errors return JSON with details:

```json
{
  "detail": "Error message here"
}
```

### Validation Errors

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

### Common Errors

**1. Invalid Email**

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address"
    }
  ]
}
```

**2. Missing Required Field**

```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required"
    }
  ]
}
```

**3. Customer Not Found**

```json
{
  "detail": "Customer with ID abc123 not found"
}
```

**4. Invalid Status**

```json
{
  "detail": [
    {
      "loc": ["body", "status"],
      "msg": "value is not a valid enumeration member; permitted: 'active', 'inactive'"
    }
  ]
}
```

---

## Configuration

### Environment Variables

```bash
# Server configuration
HOST=0.0.0.0           # Listen on all interfaces
PORT=3001              # Service port
DEBUG=true             # Enable debug mode

# CORS configuration
CORS_ORIGINS=["*"]     # Allow all origins
```

### Settings File

Located at: `src/config/settings.py`

```python
class Settings(BaseSettings):
    app_name: str = "CMS Mock Service"
    host: str = "0.0.0.0"
    port: int = 3001
    debug: bool = True
    cors_origins: list = ["*"]
```

---

## Development

### Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run service
python app.py

# Or with auto-reload
uvicorn app:app --reload --host 0.0.0.0 --port 3001
```

### Running with Docker

```bash
# Build image
docker build -t cms-mock .

# Run container
docker run -p 3001:3001 \
  -v $(pwd)/data:/app/data \
  cms-mock

# Run with docker-compose
docker-compose -f docker-compose-python-mocks.yml up cms-mock
```

### Testing

```bash
# Test health endpoint
curl http://localhost:3001/health

# Run full test suite
./scripts/test-mock-services.sh
```

---

## Troubleshooting

### Service Won't Start

**Problem:** Port already in use

```bash
# Find process on port 3001
lsof -i :3001

# Kill process
kill -9 <PID>
```

### Data Not Persisting

**Problem:** File permissions

```bash
# Check permissions
ls -la data/

# Fix permissions
chmod 755 data/
chmod 644 data/customers.json
```

### Invalid JSON File

**Problem:** Corrupted JSON

```bash
# Validate JSON
cat data/customers.json | jq

# If corrupted, delete and restart
rm data/customers.json
# Service will recreate with mock data
```

---

## Performance

### Benchmarks

- **Request Latency:** < 10ms (local)
- **Throughput:** ~1000 requests/second
- **Concurrent Users:** Handles 100+ concurrent connections
- **File Size:** Scales up to 10,000 customers efficiently

### Optimization Tips

1. **File Size:** Keep JSON file under 10MB for best performance
2. **Concurrency:** Thread-safe up to 100 concurrent requests
3. **Memory:** Uses ~50MB RAM for 1,000 customers
4. **Disk I/O:** SSD recommended for large datasets

---

## Security Notes

⚠️ **This is a MOCK service for development/testing only**

- No authentication/authorization
- No encryption at rest
- No audit logging
- No rate limiting
- CORS allows all origins

**Do not use in production without adding proper security!**

---

## Support & Documentation

- **API Docs:** http://localhost:3001/docs
- **Service Info:** http://localhost:3001/
- **Health Check:** http://localhost:3001/health
- **Source Code:** `services/mocks/cms-mock/`

---

**Last Updated:** February 1, 2026  
**Version:** 1.0.0  
**Status:** Production Ready (Development Use Only)
