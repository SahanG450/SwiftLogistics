# SwiftLogistics - Quick Reference Guide

## 🚀 Quick Start Commands

```bash
# Start everything
./scripts/start.sh

# Stop everything
./scripts/stop.sh

# Check health
./scripts/health-check.sh

# Test API
./scripts/test-api.sh
```

## 📦 Docker Compose Commands

### Starting Services

```bash
# Build and start all services
docker-compose up --build -d

# Start in foreground (see logs)
docker-compose up

# Start specific service
docker-compose up api-gateway

# Rebuild without cache
docker-compose build --no-cache
```

### Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop and remove images
docker-compose down --rmi all

# Stop specific service
docker-compose stop orchestrator
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f orchestrator

# Last 100 lines
docker-compose logs --tail=100 orchestrator

# Since specific time
docker-compose logs --since 2024-01-25T10:00:00
```

### Service Management

```bash
# List running containers
docker-compose ps

# Restart service
docker-compose restart orchestrator

# Restart all services
docker-compose restart

# Scale service
docker-compose up --scale cms-adapter=3 -d
```

## 🔧 Container Commands

### Execute Commands

```bash
# Open shell in container
docker-compose exec orchestrator sh

# Run command in container
docker-compose exec orchestrator node --version

# Run as root
docker-compose exec -u root orchestrator sh
```

### Inspect Containers

```bash
# View container details
docker inspect swiftlogistics-orchestrator

# View resource usage
docker stats

# View processes
docker-compose top
```

## 🗄️ Database Commands

### MongoDB

```bash
# Connect to MongoDB shell
docker-compose exec mongodb mongosh -u admin -p admin123

# Backup database
docker-compose exec mongodb mongodump --out=/backup

# Restore database
docker-compose exec mongodb mongorestore /backup

# View collections
docker-compose exec mongodb mongosh -u admin -p admin123 --eval "use swiftlogistics; show collections"

# Query orders
docker-compose exec mongodb mongosh -u admin -p admin123 --eval "use swiftlogistics; db.orders.find().pretty()"
```

### RabbitMQ

```bash
# List queues
curl -u admin:admin123 http://localhost:15672/api/queues

# List exchanges
curl -u admin:admin123 http://localhost:15672/api/exchanges

# View queue details
curl -u admin:admin123 http://localhost:15672/api/queues/%2F/new_order_queue

# Purge queue
curl -u admin:admin123 -X DELETE http://localhost:15672/api/queues/%2F/new_order_queue/contents
```

## 🔍 Debugging Commands

### View Logs

```bash
# Follow logs for debugging
docker-compose logs -f orchestrator cms-adapter ros-adapter wms-adapter

# Search logs
docker-compose logs orchestrator | grep ERROR

# Export logs
docker-compose logs > logs.txt
```

### Network Debugging

```bash
# List networks
docker network ls

# Inspect network
docker network inspect swiftlogistics-network

# Test connectivity
docker-compose exec api-gateway ping orchestrator
docker-compose exec api-gateway wget -O- http://orchestrator:3001
```

### Resource Usage

```bash
# View resource stats
docker stats

# View disk usage
docker system df

# Clean up unused resources
docker system prune -a
```

## 🧪 Testing Commands

### Manual API Testing

```bash
# Submit order (needs JWT)
curl -X POST http://localhost:3000/api/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "customerName": "John Doe",
    "items": ["Item1"],
    "pickupAddress": "Colombo",
    "deliveryAddress": "Kandy"
  }'

# Get order status
curl http://localhost:3000/api/orders/ORDER_ID \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Health check
curl http://localhost:3000/health
```

## 📊 Monitoring URLs

| Service              | URL                            | Credentials      |
| -------------------- | ------------------------------ | ---------------- |
| API Gateway          | http://localhost:3000          | -                |
| Orchestrator         | http://localhost:3001          | -                |
| Notification Service | http://localhost:3002          | -                |
| RabbitMQ Management  | http://localhost:15672         | admin / admin123 |
| MongoDB              | mongodb://localhost:27017      | admin / admin123 |
| CMS Mock             | http://localhost:4000/cms?wsdl | -                |
| ROS Mock             | http://localhost:4001          | -                |
| WMS Mock             | tcp://localhost:4002           | -                |

## 🛠️ Makefile Commands

```bash
# See all available commands
make help

# Build and start
make up-build

# View logs
make logs
make logs-orchestrator

# Restart services
make restart
make restart-orchestrator

# Clean everything
make clean

# Open RabbitMQ UI
make rabbitmq-ui

# Open MongoDB shell
make shell-mongo
```

## 🔐 Security Commands

### Change Passwords

```bash
# MongoDB
# Edit docker-compose.yml:
# MONGO_INITDB_ROOT_PASSWORD: new_password

# RabbitMQ
# Edit docker-compose.yml:
# RABBITMQ_DEFAULT_PASS: new_password

# Then restart
docker-compose down
docker-compose up -d
```

### Generate JWT Secret

```bash
# Generate random secret
openssl rand -base64 32

# Update in .env or docker-compose.yml:
# JWT_SECRET: <generated-secret>
```

## 🔄 Backup & Restore

### Full System Backup

```bash
# Stop services
docker-compose down

# Backup volumes
docker run --rm -v swiftlogistics-mongodb-data:/data -v $(pwd):/backup ubuntu tar czf /backup/mongodb-backup.tar.gz /data
docker run --rm -v swiftlogistics-rabbitmq-data:/data -v $(pwd):/backup ubuntu tar czf /backup/rabbitmq-backup.tar.gz /data

# Restart services
docker-compose up -d
```

### Restore from Backup

```bash
# Stop services
docker-compose down -v

# Restore volumes
docker run --rm -v swiftlogistics-mongodb-data:/data -v $(pwd):/backup ubuntu tar xzf /backup/mongodb-backup.tar.gz -C /
docker run --rm -v swiftlogistics-rabbitmq-data:/data -v $(pwd):/backup ubuntu tar xzf /backup/rabbitmq-backup.tar.gz -C /

# Start services
docker-compose up -d
```

## ⚡ Performance Optimization

### Resource Limits

```yaml
# Add to docker-compose.yml
services:
  orchestrator:
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
        reservations:
          cpus: "0.5"
          memory: 256M
```

### Clean Up

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove everything unused
docker system prune -a --volumes
```

## 🐛 Common Issues

### Port Already in Use

```bash
# Find process using port
lsof -i :3000

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
```

### Out of Memory

```bash
# Increase Docker memory in Docker Desktop settings
# Or clear resources:
docker system prune -a
```

### Container Won't Start

```bash
# Check logs
docker-compose logs <service-name>

# Rebuild
docker-compose build --no-cache <service-name>
docker-compose up <service-name>
```

### Database Connection Failed

```bash
# Wait for health check
docker-compose ps

# Check MongoDB logs
docker-compose logs mongodb

# Restart
docker-compose restart mongodb orchestrator
```

## 📚 Additional Resources

- [Docker Documentation](./DOCKER.md)
- [Architecture Guide](./ARCHITECTURE.md)
- [System Diagrams](./DIAGRAMS.md)
- [Official Docker Docs](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)

## 💡 Tips

1. Use `make help` for quick command reference
2. Always check logs when debugging: `docker-compose logs -f`
3. Use health checks to ensure services are ready
4. Scale adapters for better performance
5. Monitor RabbitMQ queues for bottlenecks
6. Backup data regularly
7. Use `.env` file for environment-specific configs
8. Don't commit `.env` files to git
