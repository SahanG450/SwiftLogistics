# WMS Mock Service (Python)

Warehouse Management System Mock Service for Swift Logistics.

## Features

- Inventory CRUD operations
- SKU-based inventory lookup
- Stock level checking
- Reorder level management
- Inventory status tracking
- FastAPI with automatic API documentation
- In-memory data storage

## Installation

```bash
pip install -r requirements.txt
```

## Running the Service

### Local Development

```bash
python app.py
```

The service will be available at `http://localhost:3003`

### Using Docker

```bash
docker build -t wms-mock-python .
docker run -p 3003:3003 wms-mock-python
```

## API Endpoints

- `GET /api/inventory` - Get all inventory items
- `GET /api/inventory/{id}` - Get inventory item by ID
- `GET /api/inventory/sku/{sku}` - Get inventory item by SKU
- `POST /api/inventory` - Create new inventory item
- `PUT /api/inventory/{id}` - Update inventory item
- `DELETE /api/inventory/{id}` - Delete inventory item
- `GET /api/inventory/check-stock/{sku}` - Check stock level
- `GET /health` - Health check

## API Documentation

Once running, visit:

- Swagger UI: `http://localhost:3003/docs`
- ReDoc: `http://localhost:3003/redoc`

## Environment Variables

- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 3003)
- `DEBUG` - Debug mode (default: true)
