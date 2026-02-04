# CMS Adapter

## Overview

The CMS Adapter acts as a bridge between the core Orchestrator and the legacy Customer Management System (CMS). It consumes order events from RabbitMQ, transforms them into SOAP envelopes, and communicates with the CMS Mock service.

## Technology Stack

- **Language:** Python 3.13+
- **Framework:** FastAPI (for health checks/metrics)
- **Protocol:** SOAP / XML
- **Message Queue:** RabbitMQ
- **Library:** Zeep

## Data Flow

1. Consumes `order.new` event from `cms_order_queue`.
2. Validates customer existence via CMS SOAP API.
3. Updates local status.
4. (Future) Publishes confirmation back to RabbitMQ.

## Configuration

| Variable       | Default              | Description         |
| -------------- | -------------------- | ------------------- |
| `CMS_API_URL`  | http://cms-mock:3001 | SOAP Service URL    |
| `RABBITMQ_URL` | amqp://...           | RabbitMQ Connection |

## Running the Service

**Port:** N/A (Background Worker) - Health check on random/assigned port if configured.

### Local Development

```bash
cd services/adapters/cms-adapter
pip install -r requirements.txt
python main.py
```

### Docker

```yaml
cms-adapter:
  build: ./services/adapters/cms-adapter
  environment:
    - CMS_API_URL=http://cms-mock:3001
```

## Dependencies

Ref: `requirements.txt`

- pika
- zeep
- fastapi
