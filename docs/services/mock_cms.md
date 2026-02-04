# CMS Mock Service

## Overview

Simulates the Customer Management System. It provides a SOAP-like or REST interface to manage customer data.

## Technology Stack

- **Language:** Python
- **Port:** 3001
- **Data Storage:** JSON file (`data/customers.json`)

## API Endpoints

- `GET /api/customers` - List customers
- `POST /api/customers` - Create customer
- `GET /api/customers/{id}` - Get customer details

## Configuration

| Variable | Default | Description  |
| -------- | ------- | ------------ |
| `PORT`   | 3001    | Service Port |

## Development

```bash
cd services/mocks/cms-mock
python app.py
```
