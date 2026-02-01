# CMS Mock Service - Quick Reference Card

**Port:** 3001 | **Swagger:** http://localhost:3001/docs

---

## 🚀 Quick Start

```bash
# Health check
curl http://localhost:3001/health

# View all endpoints
curl http://localhost:3001/docs
```

---

## 📋 API Endpoints

### Customers
```bash
GET    /customers/              # List all
GET    /customers/{id}          # Get by ID
POST   /customers/              # Create
PUT    /customers/{id}          # Update
DELETE /customers/{id}          # Delete
```

### Drivers
```bash
GET    /drivers/                # List all
GET    /drivers/?status={val}   # Filter by status
GET    /drivers/{id}            # Get by ID
POST   /drivers/                # Create
PUT    /drivers/{id}            # Update
DELETE /drivers/{id}            # Delete
```

### Clients
```bash
GET    /clients/                        # List all
GET    /clients/?membership_level={val} # Filter
GET    /clients/{id}                    # Get by ID
POST   /clients/                        # Create
PUT    /clients/{id}                    # Update
DELETE /clients/{id}                    # Delete
```

### Admins
```bash
GET    /admins/                 # List all
GET    /admins/?role={val}      # Filter by role
GET    /admins/{id}             # Get by ID
POST   /admins/                 # Create
PUT    /admins/{id}             # Update
DELETE /admins/{id}             # Delete
```

---

## 🎯 Common Examples

### Create a Driver
```bash
curl -X POST http://localhost:3001/drivers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "email": "john@example.com",
    "phone": "+1-555-0100",
    "license_number": "DL12345678"
  }'
```

### Get Available Drivers
```bash
curl "http://localhost:3001/drivers/?status=available"
```

### Update Driver Status
```bash
curl -X PUT http://localhost:3001/drivers/{id} \
  -H "Content-Type: application/json" \
  -d '{"status": "on_duty", "vehicle_id": "VH-123"}'
```

### Create a Client
```bash
curl -X POST http://localhost:3001/clients/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Corp",
    "email": "contact@techcorp.com",
    "membership_level": "gold"
  }'
```

### Get Platinum Clients
```bash
curl "http://localhost:3001/clients/?membership_level=platinum"
```

---

## 📊 Filter Values

| Entity | Filter | Values |
|--------|--------|--------|
| Drivers | status | `available`, `on_duty`, `off_duty`, `inactive` |
| Clients | membership_level | `basic`, `silver`, `gold`, `platinum` |
| Admins | role | `super_admin`, `admin`, `moderator`, `support` |

---

## 🗂️ Data Files

```
data/customers.json   # Customer records
data/drivers.json     # Driver records
data/clients.json     # Client records
data/admins.json      # Admin records
```

---

## 🧪 Testing

```bash
# Run comprehensive tests
./scripts/test-cms-extended.sh
```

---

## 📚 Full Documentation

- **Extended Guide:** `doc/CMS_EXTENDED_DOCUMENTATION.md`
- **Original Guide:** `doc/CMS_MOCK_SERVICE.md`
- **Completion Summary:** `CMS_EXTENSION_COMPLETE.md`

