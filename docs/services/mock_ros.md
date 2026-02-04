# ROS Mock Service

## Overview

Simulates the Route Optimization System. It provides a REST API to calculate optimal routes.

## Technology Stack

- **Language:** Python
- **Port:** 3002
- **Data Storage:** JSON file (`data/routes.json`)

## API Endpoints

- `POST /api/routes/optimize` - Calculate optimal route
- `GET /api/routes/{id}` - Get route details

## Configuration

| Variable | Default | Description  |
| -------- | ------- | ------------ |
| `PORT`   | 3002    | Service Port |

## Development

```bash
cd services/mocks/ros-mock
python app.py
```
