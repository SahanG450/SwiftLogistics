# SwiftLogistics

Event-driven middleware architecture for order management and logistics operations using microservices, message queues, and multiple integration patterns.

## 🏗️ Architecture Overview

SwiftLogistics implements a modern event-driven architecture with:
- **API Gateway** - Single entry point with authentication and rate limiting
- **Orchestrator** - Transaction management and order lifecycle coordination
- **Notification Service** - Real-time WebSocket updates
- **Protocol Adapters** - CMS (SOAP), ROS (REST), WMS (TCP)
- **Mock Systems** - For testing integration patterns
- **Message Broker** - RabbitMQ for async communication
- **Database** - MongoDB for order persistence

## 🚀 Quick Start with Docker

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+

### Running the Application

1. **Clone the repository**
```bash
git clone <repository-url>
cd SwiftLogistics
```

2. **Start all services**
```bash
docker-compose up --build
```

This will start:
- MongoDB (localhost:27017)
- RabbitMQ (localhost:5672, Management UI: localhost:15672)
- API Gateway (localhost:3000)
- Orchestrator (localhost:3001)
- Notification Service (localhost:3002)
- CMS Mock (localhost:4000)
- ROS Mock (localhost:4001)
- WMS Mock (localhost:4002)
- All adapters (CMS, ROS, WMS)

3. **Verify services are running**
```bash
docker-compose ps
```

### Service Endpoints

| Service | URL | Description |
|---------|-----|-------------|
| API Gateway | http://localhost:3000 | Main entry point |
| Orchestrator | http://localhost:3001 | Order management |
| Notification Service | http://localhost:3002 | WebSocket server |
| RabbitMQ Management | http://localhost:15672 | Username: admin, Password: admin123 |

### Common Commands

**Start services in detached mode:**
```bash
docker-compose up -d
```

**View logs:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api-gateway
docker-compose logs -f orchestrator
```

**Stop services:**
```bash
docker-compose down
```

**Stop and remove volumes (clean slate):**
```bash
docker-compose down -v
```

**Rebuild specific service:**
```bash
docker-compose up --build api-gateway
```

**Scale adapters (if needed):**
```bash
docker-compose up --scale cms-adapter=2 --scale ros-adapter=2
```

## 📡 Testing the System

### Submit an Order
```bash
curl -X POST http://localhost:3000/api/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{
    "customerName": "John Doe",
    "items": ["Item1", "Item2"],
    "pickupAddress": "Colombo",
    "deliveryAddress": "Kandy"
  }'
```

### Get Order Status
```bash
curl http://localhost:3000/api/orders/:orderId \
  -H "Authorization: Bearer <your-jwt-token>"
```

### Connect to WebSocket for Real-time Updates
```javascript
const socket = io('http://localhost:3002');
socket.on('notification', (data) => {
  console.log('Order update:', data);
});
```

## 🔧 Configuration

Environment variables can be customized in `docker-compose.yml` or by creating a `.env` file:

```bash
cp .env.example .env
# Edit .env with your settings
```

## 📊 Monitoring

### RabbitMQ Management UI
- URL: http://localhost:15672
- Username: `admin`
- Password: `admin123`

Monitor queues, exchanges, and message flow.

### MongoDB
Connect with MongoDB Compass or CLI:
```bash
mongodb://admin:admin123@localhost:27017/swiftlogistics?authSource=admin
```

## 🛠️ Development

### Running Services Locally (without Docker)

Each service can be run independently:

```bash
cd services/api-gateway
npm install
npm start
```

Make sure MongoDB and RabbitMQ are running and update connection URLs in the service configuration.

## 📚 Documentation

- [Architecture Documentation](./ARCHITECTURE.md) - Detailed system design
- [System Diagrams](./DIAGRAMS.md) - Visual architecture diagrams

## 🐛 Troubleshooting

**Services won't start:**
- Check if ports are already in use: `netstat -tulpn | grep <port>`
- Ensure Docker has enough resources (Memory, CPU)
- Check logs: `docker-compose logs`

**Database connection issues:**
- Wait for MongoDB healthcheck to pass
- Verify connection string in environment variables

**RabbitMQ connection fails:**
- Ensure RabbitMQ is fully started (check healthcheck)
- Verify credentials in environment variables

**Adapters not processing:**
- Check RabbitMQ UI for queue bindings
- Verify mock services are running
- Check adapter logs for errors

## 📝 License

MIT

## 👥 Contributors

UCSC - Middleware Architecture SCS2314
