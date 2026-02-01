# ROS Mock Service (Python)

Route Optimization System Mock Service for Swift Logistics.

## Features

- Route CRUD operations
- Route optimization algorithm (mock)
- Distance and duration calculation
- Route status management
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

The service will be available at `http://localhost:3002`

### Using Docker

```bash
docker build -t ros-mock-python .
docker run -p 3002:3002 ros-mock-python
```

## API Endpoints

- `GET /api/routes` - Get all routes
- `GET /api/routes/{id}` - Get route by ID
- `POST /api/routes` - Create new route
- `PUT /api/routes/{id}` - Update route
- `DELETE /api/routes/{id}` - Delete route
- `POST /api/routes/{id}/optimize` - Optimize route
- `GET /health` - Health check

## API Documentation

Once running, visit:

- Swagger UI: `http://localhost:3002/docs`
- ReDoc: `http://localhost:3002/redoc`

## Environment Variables

- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 3002)
- `DEBUG` - Debug mode (default: true)
