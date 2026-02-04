# Orchestrator Service

## Overview

The Orchestrator is the central business logic unit of the SwiftLogistics platform. It manages the entire order lifecycle, coordinates between different adapters, and ensures data consistency across the system.

## Technology Stack

- **Language:** Python 3.13+
- **Framework:** FastAPI
- **Database:** MongoDB (via Beanie ODM)
- **Message Queue:** RabbitMQ (via Pika)
- **Logging:** Loguru

## Data Models

### Order

- `orderId`: Unique identifier (UUID based)
- `status`: RECEIVED, CONFIRMED, PROCESSING, COMPLETED, FAILED
- `pickupLocation`: Coordinates and address
- `deliveryAddress`: Coordinates and address
- `packageDetails`: Weight, dimensions, description
- `cmsStatus`: Integration status
- `rosStatus`: Integration status
- `wmsStatus`: Integration status

## Running the Service

**Port:** 3001

### Local Development

```bash
cd services/orchestrator
pip install -r requirements.txt
python main.py
```

Or using Uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 3001
```

### Docker

```yaml
orchestrator:
  build: ./services/orchestrator
  ports:
    - "3001:3001"
  environment:
    - MONGODB_URL=mongodb://mongodb:27017/swiftlogistics
    - RABBITMQ_URL=amqp://user:password@rabbitmq:5672/
```

## API Endpoints

### Orders

- `POST /api/orders` - Submit new order for processing
- `GET /api/orders/{id}` - Get order status
- `PUT /api/orders/{id}/status` - Update order status (Internal use)

### System

- `GET /health` - Service health check

## Dependencies

Ref: `requirements.txt`

- fastapi
- uvicorn
- motor (MongoDB driver)
- beanie (ODM)
- pika (RabbitMQ client)
