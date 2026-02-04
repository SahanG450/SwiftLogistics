# SwiftLogistics System Reference Manual

**Version:** 2.0.0
**Last Updated:** February 2026

---

## 1. Executive Summary

SwiftLogistics is a middleware platform designed to modernize logistics operations for Swift Logistics (Pvt) Ltd. It acts as a central nervous system, integrating legacy Customer Management Systems (CMS), modern Route Optimization Systems (ROS), and proprietary Warehouse Management Systems (WMS).

The system enables:

- **Real-time Order Processing:** Event-driven architecture handling high volumes.
- **Protocol Unification:** Integration of SOAP, REST, and TCP services.
- **Live Tracking:** WebSocket updates for drivers and clients.

---

## 2. System Architecture

### High-Level Components

1.  **Frontend Applications** (Client Portal, Driver App)
2.  **API Gateway** (Entry point, Auth, Ratelimiting)
3.  **Orchestrator** (Business Logic, State Management)
4.  **Message Broker** (RabbitMQ for async communication)
5.  **Adapters** (Protocol translation for CMS, ROS, WMS)
6.  **External/Mock Services** (The actual endpoint systems)
7.  **Notification Service** (Real-time WebSocket push)

### Technology Stack

- **Backend:** Python 3.13+, FastAPI
- **Database:** MongoDB
- **Messaging:** RabbitMQ
- **Frontend:** React, React Native (Planned)
- **Infrastructure:** Docker, Docker Compose

---

## 3. Deployment & Operations

### Prerequisites

- Docker & Docker Compose
- Make (Optional, but recommended)

### Quick Start

The entire system can be managed using the `Makefile` in the root directory.

```bash
# Start all services
make start

# View logs
make logs

# Check health
make test

# Stop everything
make stop
```

### Manual Start

If `make` is not available:

```bash
./scripts/start-all.sh
```

---

## 4. Service Catalog

For detailed technical specifications of each service, refer to the `docs/services/` directory:

- **[API Gateway](services/api_gateway.md):** Entry point and security.
- **[Orchestrator](services/orchestrator.md):** Order lifecycle management.
- **[Notification Service](services/notification_service.md):** Real-time updates.
- Adapters:
  - **[CMS Adapter](services/cms_adapter.md):** SOAP integration.
  - **[ROS Adapter](services/ros_adapter.md):** REST integration.
  - **[WMS Adapter](services/wms_adapter.md):** TCP integration.
- Mocks:
  - **[CMS Mock](services/mock_cms.md)**
  - **[ROS Mock](services/mock_ros.md)**
  - **[WMS Mock](services/mock_wms.md)**

---

## 5. Development Workflow

To add a new feature:

1.  **Update API Gateway:** Add routes in `services/api-gateway/routes`.
2.  **Update Orchestrator:** Add logic in `services/orchestrator/routes`.
3.  **Define Events:** If async, add event types in RabbitMQ exchanges.
4.  **Update Adapters:** If external systems are involved, update the relevant adapter.

---

## 6. Project Structure

```
SwiftLogistics/
├── docs/               # Documentation
│   ├── services/       # Technical Service Docs
│   └── SYSTEM_REFERENCE_MANUAL.md
├── services/           # Source Code
│   ├── api-gateway/
│   ├── orchestrator/
│   ├── notification-service/
│   ├── adapters/
│   └── mocks/
├── scripts/            # Helper scripts (start, test, setup)
├── Makefile            # Main management command
└── docker-compose.yml  # Container orchestration
```

---

## 7. Troubleshooting

- **Service Fails to Start:** Check ports (3000-3003, 4000-4002, 5672, 27017). Stop other services using these ports.
- **RabbitMQ Connection Error:** Ensure RabbitMQ container is healthy before services start (Scripts handle this wait).
- **Database Error:** Ensure MongoDB is running. connection string format: `mongodb://mongodb:27017/swiftlogistics`.
