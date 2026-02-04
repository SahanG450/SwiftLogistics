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

---

## 8. Technical Deep Dive

### 8.1 API Gateway Internals & Security

The API Gateway (`services/api-gateway`) is the security shield of the platform.

#### Authentication Flow (JWT)

1.  **Login Request:** User POSTs credentials to `/api/auth/login`.
2.  **Verification:** Gateway hashes password with **bcrypt** and compares with stored hash from CMS Mock.
3.  **Token Generation:** If valid, generates a **JSON Web Token (JWT)** using `python-jose`.
    - **Algorithm:** HS256 (HMAC with SHA-256)
    - **Payload:** `sub` (user_id), `role`, `exp` (expiration).
    - **Secret:** `SECRET_KEY` env var.
4.  **Protected Routes:** Middleware intercepts requests.
    - Extracts `Authorization: Bearer <token>`.
    - Decodes and verifies signature.
    - Injects `user_id` into `request.state`.

#### Validation & Networking

- **Input Validation:** Uses **Pydantic** models to strictly validate JSON payloads (types, constraints) before processing.
- **Rate Limiting:** **SlowAPI** tracks request IP addresses in memory to prevent abuse (e.g., `5/minute`).
- **CORS:** Configured to allow requests from the Frontend URL (`http://localhost:5173`).

### 8.2 Data Flow: The "Place Order" Journey

Tracing a data packet through the system:

1.  **Frontend**: User clicks "Submit". React sends `POST /api/orders` with JSON body.
2.  **Gateway**:
    - Validates JWT.
    - Checks Rate Limit.
    - Forwards request to **Orchestrator** (`http://orchestrator:3001`).
3.  **Orchestrator**:
    - Generates internal `order_id`.
    - Saves initial state (`RECEIVED`) to **MongoDB**.
    - Publishes message to **RabbitMQ** exchange `order_exchange`.
    - Returns **202 Accepted** immediately to Gateway -> Frontend.
4.  **RabbitMQ (Fanout)**:
    - Copies message to 3 queues: `cms_queue`, `ros_queue`, `wms_queue`.
5.  **Adapters (Parallel Processing)**:
    - **CMS Adapter:** Reads queue -> Transforms to SOAP -> Calls CMS Mock.
    - **ROS Adapter:** Reads queue -> Transforms to REST -> Calls ROS Mock.
    - **WMS Adapter:** Reads queue -> Opens TCP Socket -> Calls WMS Mock.
6.  **Feedback Loop**:
    - Adapters receive responses from Mocks.
    - Adapters publish `order_update` events back to RabbitMQ.
7.  **Notification**:
    - Consumes `order_update`.
    - Pushes JSON payload to Frontend via **Socket.IO**.
8.  **Frontend**:
    - Receives WebSocket event.
    - Updates UI Status (e.g., content turns Green).

### 8.3 RabbitMQ Architecture

The system uses a "Pub/Sub" pattern for decoupling.

- **Brokers:** RabbitMQ Server (`rabbitmq:5672`).
- **Exchanges:**
  - `order_exchange` (Type: `fanout`): Broadcasts new orders to all adapters.
  - `events_exchange` (Type: `topic`): Routes updates based on source (e.g., `cms.success`).
- **Queues:**
  - `cms_order_queue`, `ros_order_queue`, `wms_order_queue` (Bound to `order_exchange`).
  - `notification_events_queue` (Bound to `events_exchange`).
- **Reliability:** Usage of **Durable Queues** ensures messages persist if services crash.

### 8.4 User Credential Handling

- **Storage:** Credentials are NOT stored in the gateway. They reside in the **CMS Mock** database (`customers.json`).
- **Hashing:** Passwords are hashed using **bcrypt** (salt rounds auto-handled by `passlib`).
- **Safety:** Plaintext passwords never leave the boundaries of the internal network after the initial HTTPS (simulated) request.

### 8.5 Inter-Container Communication

Docker Compose creates a private network (`custom_network`).

- **Service Discovery:** Containers resolve each other by name.
  - Gateway talks to `http://orchestrator:3001`.
  - Adapters talk to `amqp://rabbitmq:5672`.
- **Isolation:** Only ports `3000-3003` are exposed to host; internal database ports (`27017`) can be kept private if desired (currently exposed for debugging).
