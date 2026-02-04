# WMS Mock Service

## Overview

Simulates the Warehouse Management System. It listens on a TCP port for commands.

## Technology Stack

- **Language:** Python
- **Port:** 3003 (TCP)
- **Data Storage:** JSON file (`data/inventory.json`)

## Protocol

Command based TCP protocol.
Example: `CHECK_STOCK <SKU>`

## Configuration

| Variable   | Default | Description        |
| ---------- | ------- | ------------------ |
| `TCP_PORT` | 3003    | TCP Listening Port |

## Development

```bash
cd services/mocks/wms-mock
python app.py
```
