# Notification Service

## Overview

The Notification Service handles real-time updates to connected clients (Web Portal and Driver App). It consumes events from RabbitMQ and broadcasts them via WebSockets (Socket.IO).

## Technology Stack

- **Language:** Python 3.13+
- **Framework:** FastAPI
- **WebSocket:** python-socketio
- **Message Queue:** RabbitMQ (via Pika)
- **Logging:** Loguru

## Real-time Events

### `order-update`

Payload sent to clients when an order status changes.

```json
{
  "orderId": "ORD-123",
  "status": "PROCESSING",
  "timestamp": "2026-02-04T10:00:00Z"
}
```

## Running the Service

**Port:** 3002

### Local Development

```bash
cd services/notification-service
pip install -r requirements.txt
python main.py
```

Or using Uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 3002
```

### Docker

```yaml
notification-service:
  build: ./services/notification-service
  ports:
    - "3002:3002"
  environment:
    - RABBITMQ_URL=amqp://user:password@rabbitmq:5672/
```

## API Endpoints

- `GET /health` - Service health check
- `GET /socket.io/` - WebSocket handshake

## Dependencies

Ref: `requirements.txt`

- fastapi
- uvicorn
- python-socketio
- pika
- aiohttp
