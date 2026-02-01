# CMS Mock Service (Python)

Customer Management System Mock Service for Swift Logistics.

## Features

- Customer CRUD operations
- Customer status management
- FastAPI with automatic API documentation
- File-based JSON data storage (persists across restarts)

## Installation

```bash
pip install -r requirements.txt
```

## Running the Service

### Local Development

```bash
python app.py
```

The service will be available at `http://localhost:3001`

### Using Docker

```bash
docker build -t cms-mock-python .
docker run -p 3001:3001 cms-mock-python
```

## API Endpoints

- `GET /api/customers` - Get all customers
- `GET /api/customers/{id}` - Get customer by ID
- `POST /api/customers` - Create new customer
- `PUT /api/customers/{id}` - Update customer
- `DELETE /api/customers/{id}` - Delete customer
- `GET /health` - Health check

## API Documentation

Once running, visit:

- Swagger UI: `http://localhost:3001/docs`
- ReDoc: `http://localhost:3001/redoc`

## Environment Variables

- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 3001)
- `DEBUG` - Debug mode (default: true)

## Data Storage

Customer data is persisted to `data/customers.json`. 

### View Data
```bash
cat data/customers.json | jq
```

### Reset Data
```bash
# Delete the JSON file - it will be recreated with mock data on next startup
rm data/customers.json
```

### Backup Data
```bash
# Backup customer data
cp data/customers.json ~/backup/customers-$(date +%Y%m%d).json
```

## Sample Data

On first run, the service initializes with 2 mock customers:
- John Doe (Tech Corp)
- Jane Smith (Retail Inc)
