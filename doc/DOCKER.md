# Docker Setup Guide

## Overview

This guide provides detailed instructions for running SwiftLogistics using Docker and Docker Compose.

## Prerequisites

- **Docker Engine**: 20.10 or higher
- **Docker Compose**: 2.0 or higher
- **System Requirements**:
  - 4GB RAM minimum (8GB recommended)
  - 10GB free disk space

## Installation

### Install Docker

**Ubuntu/Debian:**

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**macOS:**
Download Docker Desktop from https://www.docker.com/products/docker-desktop

**Windows:**
Download Docker Desktop from https://www.docker.com/products/docker-desktop

### Verify Installation

```bash
docker --version
docker-compose --version
```

## Quick Start

### Option 1: Using the start script (Recommended)

```bash
./scripts/start.sh
```

### Option 2: Manual setup

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Option 3: Using Makefile

```bash
# See all available commands
make help

# Build and start
make up-build

# View logs
make logs
```

## Service Architecture

The Docker Compose setup includes:

### Infrastructure Layer

- **MongoDB** (Port 27017) - Persistent storage
- **RabbitMQ** (Ports 5672, 15672) - Message broker

### Application Layer

- **API Gateway** (Port 3000) - Entry point
- **Orchestrator** (Port 3001) - Transaction manager
- **Notification Service** (Port 3002) - WebSocket server

### Adapter Layer

- **CMS Adapter** - SOAP/XML protocol translator
- **ROS Adapter** - REST/JSON protocol translator
- **WMS Adapter** - TCP socket protocol translator

### Mock Layer

- **CMS Mock** (Port 4000) - SOAP server simulator
- **ROS Mock** (Port 4001) - REST API simulator
- **WMS Mock** (Port 4002) - TCP server simulator

## Network Configuration

All services run on a custom bridge network: `swiftlogistics-network`

### Internal DNS Resolution

Services can communicate using their service names:

- `mongodb` → MongoDB database
- `rabbitmq` → RabbitMQ broker
- `orchestrator` → Orchestrator service
- `cms-mock` → CMS Mock service
- etc.

## Environment Variables

### Default Configuration

The Docker Compose file includes default environment variables. To customize:

1. Copy the example file:

```bash
cp .env.example .env
```

2. Edit `.env` with your values:

```bash
# Example customizations
MONGODB_URI=mongodb://admin:mypassword@mongodb:27017/swiftlogistics?authSource=admin
JWT_SECRET=your-production-secret-key
RATE_LIMIT_MAX_REQUESTS=200
```

3. Restart services:

```bash
docker-compose down
docker-compose up -d
```

### Key Environment Variables

| Variable       | Description               | Default                                                                  |
| -------------- | ------------------------- | ------------------------------------------------------------------------ |
| `MONGODB_URI`  | MongoDB connection string | `mongodb://admin:admin123@mongodb:27017/swiftlogistics?authSource=admin` |
| `RABBITMQ_URL` | RabbitMQ connection URL   | `amqp://admin:admin123@rabbitmq:5672`                                    |
| `JWT_SECRET`   | JWT signing secret        | `your-secret-key-change-in-production`                                   |
| `NODE_ENV`     | Environment mode          | `development`                                                            |

## Health Checks

Services include health checks to ensure proper startup order:

- **MongoDB**: Checks database ping
- **RabbitMQ**: Checks broker diagnostics

Dependent services wait for infrastructure to be healthy before starting.

## Volume Management

### Persistent Volumes

- `swiftlogistics-mongodb-data` - MongoDB data persistence
- `swiftlogistics-rabbitmq-data` - RabbitMQ data persistence

### Backup Data

```bash
# Backup MongoDB
docker-compose exec mongodb mongodump --out=/backup --authenticationDatabase=admin -u admin -p admin123

# Copy backup to host
docker cp swiftlogistics-mongodb:/backup ./mongodb-backup
```

### Restore Data

```bash
# Copy backup to container
docker cp ./mongodb-backup swiftlogistics-mongodb:/backup

# Restore MongoDB
docker-compose exec mongodb mongorestore /backup --authenticationDatabase=admin -u admin -p admin123
```

### Remove All Data (Clean Start)

```bash
docker-compose down -v
```

⚠️ **Warning**: This will delete all data including orders, queues, and messages.

## Troubleshooting

### Port Conflicts

If you get "port already in use" errors:

```bash
# Check what's using the port
sudo lsof -i :3000  # Replace with your port

# Kill the process or change the port in docker-compose.yml
```

### Container Won't Start

```bash
# Check logs
docker-compose logs <service-name>

# Check container status
docker-compose ps

# Restart specific service
docker-compose restart <service-name>
```

### Out of Memory

```bash
# Check Docker memory usage
docker stats

# Increase Docker memory limit in Docker Desktop settings
# Or clear unused resources:
docker system prune -a
```

### Database Connection Issues

```bash
# Verify MongoDB is running and healthy
docker-compose ps mongodb

# Check MongoDB logs
docker-compose logs mongodb

# Test connection from orchestrator
docker-compose exec orchestrator sh
# Inside container:
# curl mongodb:27017  # Should get a response
```

### RabbitMQ Connection Issues

```bash
# Check RabbitMQ status
docker-compose logs rabbitmq

# Access RabbitMQ Management UI
# http://localhost:15672
# Username: admin, Password: admin123

# Verify queues are created
# Should see: new_order_queue, notification_events_queue
```

### Service Can't Resolve Other Services

```bash
# Verify network exists
docker network ls | grep swiftlogistics

# Check service is on the network
docker inspect swiftlogistics-api-gateway | grep NetworkMode

# Test DNS resolution
docker-compose exec api-gateway ping mongodb
```

## Development Workflow

### Hot Reload (Development Mode)

For development with hot reload, mount your source code:

```yaml
# Add to docker-compose.yml under the service
volumes:
  - ./services/api-gateway/src:/app/src
```

Then restart:

```bash
docker-compose restart api-gateway
```

### Debugging

#### View Real-time Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f orchestrator

# Last 100 lines
docker-compose logs --tail=100 orchestrator
```

#### Execute Commands in Container

```bash
# Open shell
docker-compose exec orchestrator sh

# Run Node.js REPL
docker-compose exec orchestrator node

# Run npm commands
docker-compose exec orchestrator npm test
```

#### Inspect Container

```bash
# View container details
docker inspect swiftlogistics-orchestrator

# View resource usage
docker stats swiftlogistics-orchestrator
```

### Rebuilding After Code Changes

```bash
# Rebuild specific service
docker-compose build orchestrator
docker-compose up -d orchestrator

# Or rebuild and restart all
docker-compose up --build -d
```

## Production Deployment

### Security Hardening

1. **Change default passwords**:

```bash
# In .env file
MONGO_INITDB_ROOT_PASSWORD=<strong-password>
RABBITMQ_DEFAULT_PASS=<strong-password>
JWT_SECRET=<random-256-bit-key>
```

2. **Remove management ports**:

```yaml
# In docker-compose.yml, comment out:
# - "15672:15672"  # RabbitMQ UI
```

3. **Use secrets management**:

```bash
# Use Docker secrets or external secret managers
# like AWS Secrets Manager, HashiCorp Vault
```

### Resource Limits

Add resource limits to prevent container resource exhaustion:

```yaml
services:
  orchestrator:
    # ...existing config...
    deploy:
      resources:
        limits:
          cpus: "1"
          memory: 512M
        reservations:
          cpus: "0.5"
          memory: 256M
```

### Production Compose Override

Create `docker-compose.prod.yml`:

```yaml
version: "3.8"

services:
  mongodb:
    restart: always
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  rabbitmq:
    restart: always
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # Add for all services...
```

Run with:

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Monitoring

### Container Metrics

```bash
# Real-time stats
docker stats

# Specific service
docker stats swiftlogistics-orchestrator
```

### RabbitMQ Monitoring

Access management UI:

- URL: http://localhost:15672
- Username: `admin`
- Password: `admin123`

Monitor:

- Queue depths
- Message rates
- Connection status
- Memory usage

### MongoDB Monitoring

```bash
# Connect to MongoDB shell
docker-compose exec mongodb mongosh -u admin -p admin123

# View database stats
use swiftlogistics
db.stats()

# View collection stats
db.orders.stats()
```

## Scaling

### Horizontal Scaling

Scale adapters to handle more load:

```bash
# Scale CMS adapter to 3 instances
docker-compose up --scale cms-adapter=3 -d

# Scale all adapters
docker-compose up --scale cms-adapter=3 --scale ros-adapter=3 --scale wms-adapter=3 -d
```

### Load Balancing

For API Gateway scaling, add a reverse proxy (nginx):

```yaml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
  depends_on:
    - api-gateway
```

## Cleanup

### Remove Stopped Containers

```bash
docker-compose rm
```

### Remove All Project Resources

```bash
# Stop and remove containers, networks
docker-compose down

# Also remove volumes
docker-compose down -v

# Also remove images
docker-compose down -v --rmi all
```

### Clean Docker System

```bash
# Remove all unused containers, networks, images
docker system prune -a

# Remove volumes too
docker system prune -a --volumes
```

## Advanced Configuration

### Custom Network

To use an existing network:

```yaml
networks:
  swiftlogistics-network:
    external: true
    name: my-existing-network
```

### Using External MongoDB/RabbitMQ

To use external MongoDB or RabbitMQ:

1. Remove the service from docker-compose.yml
2. Update connection URLs in environment variables
3. Ensure network connectivity

```yaml
services:
  orchestrator:
    environment:
      MONGODB_URI: mongodb://external-mongo:27017/swiftlogistics
      RABBITMQ_URL: amqp://external-rabbitmq:5672
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Docker Build

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build images
        run: docker-compose build
      - name: Run tests
        run: docker-compose run orchestrator npm test
```

### GitLab CI Example

```yaml
stages:
  - build
  - test

build:
  stage: build
  script:
    - docker-compose build

test:
  stage: test
  script:
    - docker-compose up -d
    - docker-compose exec -T orchestrator npm test
    - docker-compose down
```

## Support

For issues and questions:

- Check logs: `docker-compose logs`
- Review documentation: `./ARCHITECTURE.md`
- Check service status: `docker-compose ps`

## Next Steps

1. ✅ Start services: `./scripts/start.sh`
2. 📊 Check RabbitMQ UI: http://localhost:15672
3. 🧪 Test API: Submit an order to `http://localhost:3000/api/orders`
4. 📡 Connect WebSocket: `http://localhost:3002`
5. 📚 Read architecture docs: `./ARCHITECTURE.md`
