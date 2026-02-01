# CMS Mock Service - API Endpoints Reference

Complete API documentation for all entity types in the CMS Mock Service.

---

## Customer Endpoints

### 1. Get All Customers

**GET** `/customers/`

```bash
curl http://localhost:3001/customers/
```

**Response (200 OK):**
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
    "created_at": "2024-01-15T10:00:00",
    "updated_at": "2024-01-15T10:00:00"
  }
]
```

### 2. Get Customer by ID

**GET** `/customers/{id}`

```bash
curl http://localhost:3001/customers/e20a1b70-67c9-4fb4-9f6d-56ba97a87c14
```

### 3. Create Customer

**POST** `/customers/`

```bash
curl -X POST http://localhost:3001/customers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "phone": "+1-555-0200",
    "address": "789 Oak St, Boston, MA 02101",
    "company": "Manufacturing Co"
  }'
```

### 4. Update Customer

**PUT** `/customers/{id}`

```bash
curl -X PUT http://localhost:3001/customers/{id} \
  -H "Content-Type: application/json" \
  -d '{"status": "inactive"}'
```

### 5. Delete Customer

**DELETE** `/customers/{id}`

```bash
curl -X DELETE http://localhost:3001/customers/{id}
```

---

## Driver Endpoints

### 1. Get All Drivers

**GET** `/drivers/` or `/drivers/?status=available`

```bash
# Get all drivers
curl http://localhost:3001/drivers/

# Filter by status
curl "http://localhost:3001/drivers/?status=available"
curl "http://localhost:3001/drivers/?status=on_duty"
curl "http://localhost:3001/drivers/?status=off_duty"
```

**Response (200 OK):**
```json
[
  {
    "id": "23ed1992-52a6-4def-9e00-53b21c155a5b",
    "name": "Mike Wilson",
    "email": "mike.wilson@swiftlogistics.com",
    "phone": "+1-555-0201",
    "license_number": "DL123456789",
    "vehicle_id": "VH-001",
    "status": "available",
    "created_at": "2024-01-15T10:00:00",
    "updated_at": "2024-01-15T10:00:00"
  }
]
```

### 2. Get Driver by ID

**GET** `/drivers/{id}`

```bash
curl http://localhost:3001/drivers/23ed1992-52a6-4def-9e00-53b21c155a5b
```

### 3. Create Driver

**POST** `/drivers/`

```bash
curl -X POST http://localhost:3001/drivers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Driver",
    "email": "john.driver@swiftlogistics.com",
    "phone": "+1-555-0301",
    "license_number": "DL987654321",
    "vehicle_id": "VH-003"
  }'
```

**Response (201 Created):**
```json
{
  "id": "generated-uuid",
  "name": "John Driver",
  "email": "john.driver@swiftlogistics.com",
  "phone": "+1-555-0301",
  "license_number": "DL987654321",
  "vehicle_id": "VH-003",
  "status": "available",
  "created_at": "2024-02-01T15:30:00",
  "updated_at": "2024-02-01T15:30:00"
}
```

### 4. Update Driver

**PUT** `/drivers/{id}`

```bash
curl -X PUT http://localhost:3001/drivers/{id} \
  -H "Content-Type: application/json" \
  -d '{
    "status": "on_duty",
    "vehicle_id": "VH-005"
  }'
```

### 5. Delete Driver

**DELETE** `/drivers/{id}`

```bash
curl -X DELETE http://localhost:3001/drivers/{id}
```

---

## Client Endpoints

### 1. Get All Clients

**GET** `/clients/` or `/clients/?membership_level=gold`

```bash
# Get all clients
curl http://localhost:3001/clients/

# Filter by membership level
curl "http://localhost:3001/clients/?membership_level=basic"
curl "http://localhost:3001/clients/?membership_level=silver"
curl "http://localhost:3001/clients/?membership_level=gold"
curl "http://localhost:3001/clients/?membership_level=platinum"
```

**Response (200 OK):**
```json
[
  {
    "id": "c1a2b3c4-1234-5678-90ab-cdef12345678",
    "name": "Tech Startup Inc",
    "email": "contact@techstartup.com",
    "phone": "+1-555-0301",
    "address": "100 Innovation Drive, San Francisco, CA 94105",
    "membership_level": "gold",
    "created_at": "2024-01-10T09:00:00",
    "updated_at": "2024-01-10T09:00:00"
  }
]
```

### 2. Get Client by ID

**GET** `/clients/{id}`

```bash
curl http://localhost:3001/clients/c1a2b3c4-1234-5678-90ab-cdef12345678
```

### 3. Create Client

**POST** `/clients/`

```bash
curl -X POST http://localhost:3001/clients/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Enterprise Co",
    "email": "contact@newenterprise.com",
    "phone": "+1-555-0401",
    "address": "200 Business Park, Austin, TX 78701",
    "membership_level": "silver"
  }'
```

**Response (201 Created):**
```json
{
  "id": "generated-uuid",
  "name": "New Enterprise Co",
  "email": "contact@newenterprise.com",
  "phone": "+1-555-0401",
  "address": "200 Business Park, Austin, TX 78701",
  "membership_level": "silver",
  "created_at": "2024-02-01T16:00:00",
  "updated_at": "2024-02-01T16:00:00"
}
```

### 4. Update Client

**PUT** `/clients/{id}`

```bash
curl -X PUT http://localhost:3001/clients/{id} \
  -H "Content-Type: application/json" \
  -d '{"membership_level": "platinum"}'
```

### 5. Delete Client

**DELETE** `/clients/{id}`

```bash
curl -X DELETE http://localhost:3001/clients/{id}
```

---

## Admin Endpoints

### 1. Get All Admins

**GET** `/admins/` or `/admins/?role=super_admin`

```bash
# Get all admins
curl http://localhost:3001/admins/

# Filter by role
curl "http://localhost:3001/admins/?role=super_admin"
curl "http://localhost:3001/admins/?role=admin"
curl "http://localhost:3001/admins/?role=moderator"
curl "http://localhost:3001/admins/?role=support"
```

**Response (200 OK):**
```json
[
  {
    "id": "337dfd9a-1d3a-40ef-97ae-b21d8f0a8446",
    "name": "Admin User",
    "email": "admin@swiftlogistics.com",
    "phone": "+1-555-0001",
    "role": "super_admin",
    "permissions": ["*"],
    "created_at": "2024-01-01T08:00:00",
    "updated_at": "2024-01-01T08:00:00"
  }
]
```

### 2. Get Admin by ID

**GET** `/admins/{id}`

```bash
curl http://localhost:3001/admins/337dfd9a-1d3a-40ef-97ae-b21d8f0a8446
```

### 3. Create Admin

**POST** `/admins/`

```bash
curl -X POST http://localhost:3001/admins/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Moderator",
    "email": "moderator@swiftlogistics.com",
    "phone": "+1-555-0501",
    "role": "moderator",
    "permissions": ["users.read", "content.moderate"]
  }'
```

**Response (201 Created):**
```json
{
  "id": "generated-uuid",
  "name": "New Moderator",
  "email": "moderator@swiftlogistics.com",
  "phone": "+1-555-0501",
  "role": "moderator",
  "permissions": ["users.read", "content.moderate"],
  "created_at": "2024-02-01T17:00:00",
  "updated_at": "2024-02-01T17:00:00"
}
```

### 4. Update Admin

**PUT** `/admins/{id}`

```bash
curl -X PUT http://localhost:3001/admins/{id} \
  -H "Content-Type: application/json" \
  -d '{
    "role": "admin",
    "permissions": ["users.read", "users.write", "orders.read"]
  }'
```

### 5. Delete Admin

**DELETE** `/admins/{id}`

```bash
curl -X DELETE http://localhost:3001/admins/{id}
```

---

## Health & Info Endpoints

### Health Check

**GET** `/health`

```bash
curl http://localhost:3001/health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "CMS Mock Service",
  "entities": {
    "customers": 3,
    "drivers": 3,
    "clients": 4,
    "admins": 3
  }
}
```

### Service Info

**GET** `/`

```bash
curl http://localhost:3001/
```

**Response (200 OK):**
```json
{
  "service": "CMS Mock Service",
  "status": "running",
  "version": "1.0.0"
}
```

### API Documentation

**GET** `/docs`

Opens interactive Swagger UI documentation in browser:
```
http://localhost:3001/docs
```

