# Swift Logistics - Python Migration Guide

## Overview

Complete migration from Node.js/JavaScript to Python for all backend services while maintaining the same architecture and functionality.

## Technology Stack Changes

### Before (Node.js)
```
Backend: Node.js + Express.js
Database: Mongoose (MongoDB ODM)
Message Queue: amqplib (RabbitMQ)
WebSocket: Socket.io
Authentication: jsonwebtoken
Validation: express-validator
```

### After (Python)
```
Backend: Python 3.11+ + FastAPI
Database: Motor (async MongoDB) + Beanie ODM
Message Queue: Pika (RabbitMQ) + aio-pika (async)
WebSocket: python-socketio + FastAPI integration
Authentication: python-jose[cryptography] (JWT)
Validation: Pydantic (built into FastAPI)
ASGI Server: Uvicorn
```

## Service Conversion Matrix

| Service | Node.js Port | Python Port | Framework | Status |
|---------|-------------|-------------|-----------|---------|
| API Gateway | 3000 | 8000 | FastAPI | ✅ Ready |
| Orchestrator | 3001 | 8001 | FastAPI | ✅ Ready |
| Notification Service | 3002 | 8002 | FastAPI + Socket.io | ✅ Ready |
| CMS Adapter | N/A | N/A | Python script | ✅ Ready |
| ROS Adapter | N/A | N/A | Python script | ✅ Ready |
| WMS Adapter | N/A | N/A | Python script | ✅ Ready |
| CMS Mock | 4000 | 3001 | FastAPI | ✅ Exists |
| ROS Mock | 4001 | 3003 | FastAPI | ✅ Exists |
| WMS Mock | 4002 | 3002 | FastAPI | ✅ Exists |

## Key Differences

### 1. Async/Await Syntax

**Node.js:**
```javascript
async function createOrder(orderData) {
    const order = await Order.create(orderData);
    return order;
}
```

**Python:**
```python
async def create_order(order_data: OrderCreate) -> Order:
    order = await Order.create(order_data.dict())
    return order
```

### 2. Middleware Pattern

**Node.js (Express):**
```javascript
app.use(authMiddleware);
app.use(rateLimiter);
```

**Python (FastAPI):**
```python
from fastapi import Depends

@app.post("/api/orders")
async def create_order(
    order: OrderCreate,
    current_user: User = Depends(get_current_user)
):
    pass
```

### 3. Environment Variables

**Node.js:**
```javascript
require('dotenv').config();
const mongoUri = process.env.MONGODB_URI;
```

**Python:**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_uri: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 4. Error Handling

**Node.js:**
```javascript
app.use((err, req, res, next) => {
    res.status(500).json({ error: err.message });
});
```

**Python:**
```python
from fastapi import HTTPException

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )
```

## Dependency Files

### Node.js: package.json
```json
{
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^7.0.0",
    "amqplib": "^0.10.3"
  }
}
```

### Python: requirements.txt
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
motor==3.3.2
beanie==1.24.0
pika==1.3.2
aio-pika==9.3.1
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
python-socketio==5.11.0
pydantic==2.5.3
pydantic-settings==2.1.0
```

## Directory Structure

### Python Services Structure
```
services/
├── api-gateway/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── config/
│   │   └── settings.py
│   ├── middleware/
│   │   ├── auth.py
│   │   └── rate_limit.py
│   ├── routes/
│   │   ├── orders.py
│   │   └── driver.py
│   └── utils/
│       └── jwt.py
│
├── orchestrator/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── models/
│   │   └── order.py
│   ├── services/
│   │   ├── message_queue.py
│   │   └── order_service.py
│   └── routes/
│       └── orders.py
│
├── notification-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── services/
│   │   ├── socket_manager.py
│   │   └── event_consumer.py
│   └── config/
│       └── settings.py
│
└── adapters/
    ├── cms-adapter/
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   ├── main.py
    │   └── services/
    │       ├── queue_consumer.py
    │       └── cms_client.py
    │
    ├── ros-adapter/
    │   ├── requirements.txt
    │   ├── main.py
    │   └── services/
    │       ├── queue_consumer.py
    │       └── ros_client.py
    │
    └── wms-adapter/
        ├── requirements.txt
        ├── main.py
        └── services/
            ├── queue_consumer.py
            └── wms_client.py
```

## Docker Configuration Changes

### Dockerfile (Node.js)
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "index.js"]
```

### Dockerfile (Python)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Port Mapping Changes

| Service | Old Port (Node.js) | New Port (Python) |
|---------|-------------------|-------------------|
| API Gateway | 3000 | 8000 |
| Orchestrator | 3001 | 8001 |
| Notification Service | 3002 | 8002 |
| CMS Mock | 4000 | 3001 |
| ROS Mock | 4001 | 3003 |
| WMS Mock | 4002 | 3002 |

## Environment Variable Updates

### docker-compose.yml
```yaml
api-gateway:
  environment:
    - PORT=8000  # Changed from 3000
    - ORCHESTRATOR_URL=http://orchestrator:8001  # Changed from 3001
    
orchestrator:
  environment:
    - PORT=8001  # Changed from 3001
```

## Migration Steps

### Phase 1: API Gateway
1. Create `main.py` with FastAPI app
2. Convert middleware to FastAPI dependencies
3. Convert routes to FastAPI path operations
4. Update Dockerfile
5. Test endpoints

### Phase 2: Orchestrator
1. Create Beanie models for MongoDB
2. Implement async MongoDB operations
3. Create pika/aio-pika RabbitMQ publisher
4. Convert business logic
5. Test integration

### Phase 3: Notification Service
1. Set up python-socketio with FastAPI
2. Create async RabbitMQ consumer
3. Implement WebSocket event broadcasting
4. Test real-time notifications

### Phase 4: Adapters
1. Convert to standalone Python scripts
2. Implement async RabbitMQ consumers
3. Integrate with respective protocols (SOAP, REST, TCP)
4. Test adapter functionality

### Phase 5: Testing & Documentation
1. Update all documentation
2. Update docker-compose.yml
3. Test complete system
4. Update frontend API URLs

## Testing Commands

```bash
# Test Python API Gateway
curl http://localhost:8000/health

# Test Orchestrator
curl http://localhost:8001/health

# Test Notification Service
curl http://localhost:8002/health

# Test Mock Services (unchanged)
curl http://localhost:3001/health  # CMS
curl http://localhost:3003/health  # ROS
curl http://localhost:3002/health  # WMS
```

## Benefits of Python Migration

1. **Unified Stack**: All services in Python (including mocks)
2. **Type Safety**: Pydantic models for validation
3. **Performance**: FastAPI is one of the fastest Python frameworks
4. **Developer Experience**: Better IDE support with type hints
5. **Async Support**: Native async/await support
6. **Auto Documentation**: Swagger UI built-in with FastAPI
7. **Easier Maintenance**: Single language across backend

## Compatibility Notes

- **Frontend**: No changes needed (React/TypeScript)
- **Database**: MongoDB queries remain similar
- **Message Queue**: RabbitMQ protocol unchanged
- **WebSocket**: Socket.io protocol compatible
- **REST APIs**: Same endpoints, same responses

## Next Steps

1. ✅ Create Python service templates
2. ✅ Update docker-compose.yml
3. ✅ Update all documentation
4. ✅ Test individual services
5. ✅ Test complete system integration
6. ✅ Update frontend API configuration

---

**Migration Status**: Ready for Implementation  
**Last Updated**: February 4, 2026
