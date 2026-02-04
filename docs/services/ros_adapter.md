# ROS Adapter

## Overview

The ROS Adapter connects the system to the Route Optimization System (ROS). It converts internal order objects into the REST format required by the external ROS API.

## Technology Stack

- **Language:** Python 3.13+
- **Framework:** FastAPI (Health check)
- **Protocol:** REST / JSON
- **Message Queue:** RabbitMQ
- **Library:** Httpx

## Data Flow

1. Consumes `order.new` event from `ros_order_queue`.
2. Extracts pickup and delivery coordinates.
3. Calls ROS API `POST /api/routes/optimize`.
4. Stores route token/ID.

## Configuration

| Variable       | Default              | Description         |
| -------------- | -------------------- | ------------------- |
| `ROS_API_URL`  | http://ros-mock:3002 | REST API URL        |
| `RABBITMQ_URL` | amqp://...           | RabbitMQ Connection |

## Running the Service

### Local Development

```bash
cd services/adapters/ros-adapter
pip install -r requirements.txt
python main.py
```

## Dependencies

- pika
- httpx
- fastapi
