# WMS Adapter

## Overview

The WMS Adapter integrates with the Warehouse Management System (WMS) using a proprietary TCP-based protocol. It handles the low-level socket communication required to check inventory and allocate packages.

## Technology Stack

- **Language:** Python 3.13+
- **Protocol:** Raw TCP Sockets
- **Message Queue:** RabbitMQ
- **Library:** Native `socket`

## Data Flow

1. Consumes `order.new` event from `wms_order_queue`.
2. Establishes TCP connection to WMS.
3. Sends binary/text payload (e.g., `ALLOCATE <SKU> <QTY>`).
4. Parses response.

## Configuration

| Variable   | Default  | Description  |
| ---------- | -------- | ------------ |
| `WMS_HOST` | wms-mock | WMS TCP Host |
| `WMS_PORT` | 3003     | WMS TCP Port |

## Running the Service

### Local Development

```bash
cd services/adapters/wms-adapter
pip install -r requirements.txt
python main.py
```

## Dependencies

- pika
- fastapi
