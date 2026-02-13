# MongoDB Integration - Quick Start Guide

This guide will help you quickly set up and test MongoDB with your SwiftLogistics Python services.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

Run the setup script:

```bash
cd /home/snake/UCSC/UCSC/Year\ 2/sem\ 2/Middleware\ Architecture\ SCS2314/Assignment\ 4/SwiftLogistics
chmod +x scripts/setup_mongodb.sh
./scripts/setup_mongodb.sh
```

This script will:

- Start MongoDB Docker container
- Install Python dependencies
- Run connection tests
- Verify all repositories work

### Option 2: Manual Setup

#### Step 1: Start MongoDB

```bash
cd /home/snake/UCSC/UCSC/Year\ 2/sem\ 2/Middleware\ Architecture\ SCS2314/Assignment\ 4/SwiftLogistics
docker-compose up -d mongodb
```

#### Step 2: Wait for MongoDB to be ready

```bash
docker logs -f swiftlogistics-mongodb
# Wait for "Waiting for connections" message
```

#### Step 3: Install Python dependencies

```bash
cd shared/database
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Step 4: Test the connection

```bash
python test_mongodb.py
```

## ✅ Verification

After setup, you should see:

```
====================================
MONGODB INTEGRATION TEST SUITE
====================================
...
✓ CONNECTION: PASSED
✓ REPOSITORIES: PASSED
✓ INDEXES: PASSED
✓ AGGREGATION: PASSED

TOTAL: 4/4 tests passed
====================================
```

## 📝 Configuration

### Environment Variables

Create or update `.env` file:

```bash
# MongoDB Configuration
MONGODB_URI=mongodb://admin:admin123@mongodb:27017/swiftlogistics?authSource=admin
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=admin123
MONGO_INITDB_DATABASE=swiftlogistics
```

### Connection Strings

**From Docker containers:**

```
mongodb://admin:admin123@mongodb:27017/swiftlogistics?authSource=admin
```

**From localhost (host machine):**

```
mongodb://admin:admin123@localhost:27017/swiftlogistics?authSource=admin
```

## 🔧 Usage in Your Services

### 1. Update requirements.txt

Add to your service's `requirements.txt`:

```txt
motor==3.3.2
pymongo==4.6.1
```

### 2. Copy shared database module

The database utilities are in `shared/database/`. You can either:

**Option A:** Import directly (if using Docker volumes):

```python
import sys
sys.path.append('/app/shared')

from database import get_database
from database.repositories import OrderRepository
```

**Option B:** Copy to your service:

```bash
cp -r shared/database/ services/your-service/src/database/
```

### 3. Update your FastAPI app

```python
from fastapi import FastAPI
from database import get_database, close_database_connection
from database.repositories import OrderRepository

app = FastAPI()

@app.on_event("startup")
async def startup():
    await get_database()
    print("Connected to MongoDB")

@app.on_event("shutdown")
async def shutdown():
    await close_database_connection()

@app.get("/orders")
async def get_orders():
    db = await get_database()
    order_repo = OrderRepository(db)
    orders = await order_repo.find_many(limit=10)
    return {"orders": orders}
```

### 4. Update Dockerfile

Ensure your Dockerfile copies the shared directory:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy shared utilities first
COPY ../../shared /app/shared

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY . .

CMD ["python", "app.py"]
```

### 5. Update docker-compose.yml

Add MongoDB dependency and environment variables:

```yaml
your-service:
  build: ./services/your-service
  depends_on:
    mongodb:
      condition: service_healthy
  environment:
    MONGODB_URI: mongodb://admin:admin123@mongodb:27017/swiftlogistics?authSource=admin
  networks:
    - swiftlogistics-network
```

## 📚 Available Repositories

The following repositories are ready to use:

- `OrderRepository` - Order management
- `DriverRepository` - Driver data
- `ClientRepository` - Client information
- `ShipmentRepository` - Shipment tracking
- `ContractRepository` - Contracts
- `InvoiceRepository` - Billing
- `AdminRepository` - Admin users

### Example Usage

```python
from database import get_database
from database.repositories import OrderRepository

# Initialize
db = await get_database()
order_repo = OrderRepository(db)

# Create
order_id = await order_repo.create({
    "order_id": "ORD-001",
    "client_id": "CLI-123",
    "status": "pending"
})

# Read
order = await order_repo.find_by_order_id("ORD-001")
orders = await order_repo.find_by_client("CLI-123")

# Update
await order_repo.update_status("ORD-001", "processing")

# Delete
await order_repo.delete_one({"order_id": "ORD-001"})

# Count
count = await order_repo.count({"status": "pending"})
```

## 🛠 Troubleshooting

### MongoDB won't start

```bash
# Check container status
docker ps -a | grep mongodb

# Check logs
docker logs swiftlogistics-mongodb

# Restart
docker-compose restart mongodb
```

### Connection refused

**From host machine:** Use `localhost` instead of `mongodb`:

```
MONGODB_URI=mongodb://admin:admin123@localhost:27017/swiftlogistics?authSource=admin
```

**From Docker container:** Use `mongodb` as hostname:

```
MONGODB_URI=mongodb://admin:admin123@mongodb:27017/swiftlogistics?authSource=admin
```

### Import errors

Make sure the shared directory is in your Python path:

```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))
```

### Authentication failed

Verify credentials in `.env` match `docker-compose.yml`:

```yaml
# docker-compose.yml
mongodb:
  environment:
    MONGO_INITDB_ROOT_USERNAME: admin
    MONGO_INITDB_ROOT_PASSWORD: admin123
```

## 📖 Documentation

- **Full Integration Guide**: See `MONGODB_INTEGRATION.md`
- **Example Service**: See `shared/database/example_service.py`
- **API Reference**: Check repository method docs in `shared/database/repositories.py`

## 🔍 MongoDB Tools

### MongoDB Compass (GUI)

Download from: https://www.mongodb.com/products/compass

Connection String:

```
mongodb://admin:admin123@localhost:27017/?authSource=admin
```

### Command Line (mongosh)

```bash
# Enter MongoDB shell
docker exec -it swiftlogistics-mongodb mongosh -u admin -p admin123

# Switch to database
use swiftlogistics

# Show collections
show collections

# Query orders
db.orders.find().pretty()

# Count documents
db.orders.count()
```

## 🎯 Next Steps

1. ✅ Run the setup script
2. ✅ Verify tests pass
3. ✅ Review `MONGODB_INTEGRATION.md` for detailed examples
4. ✅ Check `shared/database/example_service.py` for complete service example
5. ✅ Integrate MongoDB into your services
6. ✅ Test your services with MongoDB

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review logs: `docker logs swiftlogistics-mongodb`
3. Verify environment variables in `.env`
4. Ensure MongoDB container is running: `docker ps`

---

**Created**: 2026-02-13  
**MongoDB Version**: 7.0  
**Python Driver**: Motor 3.3.2 (Async)
