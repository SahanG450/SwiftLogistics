# API Gateway Service

## Overview

The API Gateway serves as the single entry point for the SwiftLogistics platform. It handles authentication, rate limiting, request validation, and routing to backend services.

## Technology Stack

- **Language:** Python 3.13+
- **Framework:** FastAPI
- **Server:** Uvicorn
- **Security:** OAuth2 / JWT (planned)
- **Rate Limiting:** SlowAPI

## Running the Service

**Port:** 3000

### Local Development

```bash
cd services/api-gateway
pip install -r requirements.txt
python main.py
```

Or using Uvicorn with reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 3000
```

### Docker

```yaml
api-gateway:
  build: ./services/api-gateway
  ports:
    - "3000:3000"
  environment:
    - ORCHESTRATOR_URL=http://orchestrator:3001
```

## API Endpoints

### Authentication

- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration

### Orders

- `POST /api/orders` - Create new order
- `GET /api/orders/{id}` - Get order details
- `GET /api/orders` - List orders

### Driver

- `GET /api/driver/routes` - Get assigned routes
- `POST /api/driver/status` - Update delivery status

### System

- `GET /health` - Service health check

## Configuration

| Variable         | Default               | Description         |
| ---------------- | --------------------- | ------------------- |
| `PORT`           | 3000                  | Service port        |
| `NODE_ENV`       | development           | Environment mode    |
| `WEB_CLIENT_URL` | http://localhost:5173 | CORS allowed origin |

## Dependencies

Ref: `requirements.txt`

- fastapi
- uvicorn
- slowapi
- python-jose
- passlib
