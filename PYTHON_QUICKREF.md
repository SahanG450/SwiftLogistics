# Python Mock Services - Quick Reference

## 🚀 Quick Start Commands

### Setup (First Time)

```bash
./scripts/setup-python-mocks.sh
```

### Start All Services

```bash
# Using scripts
./scripts/start-python-mocks.sh

# Using Docker Compose
docker-compose -f docker-compose-python-mocks.yml up -d
```

### Stop All Services

```bash
# Using scripts
./scripts/stop-python-mocks.sh

# Using Docker Compose
docker-compose -f docker-compose-python-mocks.yml down
```

### Run Individual Service

```bash
cd services/mocks/<service-name>-python
source venv/bin/activate
python app.py
```

## 🔗 Service URLs

| Service  | URL                   | Docs                       | Health                       |
| -------- | --------------------- | -------------------------- | ---------------------------- |
| CMS Mock | http://localhost:3001 | http://localhost:3001/docs | http://localhost:3001/health |
| ROS Mock | http://localhost:3002 | http://localhost:3002/docs | http://localhost:3002/health |
| WMS Mock | http://localhost:3003 | http://localhost:3003/docs | http://localhost:3003/health |

## 📁 Service Locations

```
services/mocks/
├── cms-mock-python/    # Customer Management (Port 3001)
├── ros-mock-python/    # Route Optimization (Port 3002)
└── wms-mock-python/    # Warehouse Management (Port 3003)
```

## 🛠️ Common Commands

### Install Dependencies

```bash
cd services/mocks/<service>-python
pip install -r requirements.txt
```

### Run with Auto-Reload

```bash
cd services/mocks/<service>-python
uvicorn app:app --reload --host 0.0.0.0 --port <port>
```

### Build Docker Image

```bash
cd services/mocks/<service>-python
docker build -t <service>-python .
```

### Run Docker Container

```bash
docker run -p <port>:<port> <service>-python
```

### View Logs

```bash
docker logs <container-name>
```

## 🧪 Testing API Endpoints

### CMS - Create Customer

```bash
curl -X POST http://localhost:3001/api/customers \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com"}'
```

### ROS - Create Route

```bash
curl -X POST http://localhost:3002/api/routes \
  -H "Content-Type: application/json" \
  -d '{"origin":"New York","destination":"Boston"}'
```

### WMS - Create Inventory

```bash
curl -X POST http://localhost:3003/api/inventory \
  -H "Content-Type: application/json" \
  -d '{"sku":"PROD-001","name":"Product","quantity":100}'
```

### Get All Records

```bash
curl http://localhost:3001/api/customers  # CMS
curl http://localhost:3002/api/routes     # ROS
curl http://localhost:3003/api/inventory  # WMS
```

## 📦 Dependencies

All services use:

- fastapi==0.109.0
- uvicorn[standard]==0.27.0
- pydantic==2.5.3
- pydantic-settings==2.1.0
- python-dotenv==1.0.0

## 🐛 Troubleshooting

### Port Already in Use

```bash
lsof -i :3001  # Check which process is using port
kill -9 <PID>  # Kill the process
```

### Import Errors

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Docker Issues

```bash
# Remove all containers
docker-compose -f docker-compose-python-mocks.yml down

# Rebuild images
docker-compose -f docker-compose-python-mocks.yml build --no-cache

# Start fresh
docker-compose -f docker-compose-python-mocks.yml up -d
```

## 📚 Documentation Files

- `PYTHON_MOCKS.md` - Complete migration guide
- `PYTHON_MIGRATION_COMPLETE.md` - Implementation summary
- `services/mocks/*/README.md` - Individual service docs

## ✅ Checklist

- [ ] Run setup script
- [ ] Verify all services start
- [ ] Check health endpoints
- [ ] Test API endpoints
- [ ] Review API documentation
- [ ] Test with adapters
- [ ] Update main docker-compose (if needed)

---

**Ready to go!** All Python mock services are fully implemented and ready for use.
