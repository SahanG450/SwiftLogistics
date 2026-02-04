# SwiftLogistics - Complete System Architecture Document

**Version:** 2.0.0  
**Last Updated:** February 4, 2026  
**Status:** Production Ready (Development Use)

---

## 📑 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Business Context](#business-context)
3. [System Architecture](#system-architecture)
4. [Design Patterns](#design-patterns)
5. [Data Flows](#data-flows)
6. [Technology Stack](#technology-stack)
7. [Service Catalog](#service-catalog)
8. [Frontend Applications](#frontend-applications)
9. [Integration Patterns](#integration-patterns)
10. [Deployment Architecture](#deployment-architecture)
11. [Security Model](#security-model)
12. [Performance & Scalability](#performance--scalability)

---

## 1. Executive Summary

**SwiftLogistics** is a comprehensive middleware-based logistics platform for **Swift Logistics (Pvt) Ltd.**, a Sri Lankan last-mile delivery company serving e-commerce businesses.

### Key Capabilities

- **Real-time Order Processing**: Asynchronous, event-driven architecture handling 10,000+ orders/day
- **Multi-Protocol Integration**: Seamlessly connects legacy (SOAP/XML), modern (REST/JSON), and proprietary (TCP) systems
- **Live Tracking**: WebSocket-based real-time notifications for drivers and clients
- **Scalable Architecture**: Microservices-based design with message queue orchestration

### Core Problem Solved

Replaces siloed manual systems with an integrated platform connecting:

- **CMS** (Client Management System) - Legacy SOAP-based
- **ROS** (Route Optimization System) - Modern REST API
- **WMS** (Warehouse Management System) - Proprietary TCP/IP

---

## 2. Business Context

### 🏢 Company Profile

**Swift Logistics (Pvt) Ltd.**

- **Industry**: Last-mile delivery for e-commerce
- **Location**: Sri Lanka (Colombo, Kandy, Galle, Jaffna)
- **Clients**: Daraz Lanka, Kapruka.com, Takas.lk, PickMe Market, independent sellers
- **Platform**: SwiftTrack (Web portal + Mobile app)

### Business Metrics

| Metric             | Capacity |
| ------------------ | -------- |
| Orders/day         | 10,000+  |
| Concurrent drivers | 500+     |
| Warehouse zones    | 100+     |
| Active clients     | 1,000+   |
| Packages tracked   | 50,000+  |
| Routes optimized   | 500+/day |

### Peak Seasons

- **Black Friday** (November) - High volume sales
- **Avurudu** (April) - Cultural festival deliveries
- **Christmas** (December) - Holiday shopping
- **Vesak** (May) - Gift deliveries

### Key Use Cases

1. **Black Friday Sale**: Handle 5000+ orders in 24 hours with priority marking and batch processing
2. **Avurudu Delivery Rush**: Time-sensitive gift deliveries with proof of delivery
3. **Same-Day Delivery**: Urgent delivery within 4 hours with real-time route updates

---

## 3. System Architecture

### 3.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER                               │
│                                                                       │
│  ┌──────────────────┐              ┌─────────────────────┐         │
│  │  Client Portal   │              │  Driver Mobile App   │         │
│  │  (React Web)     │              │  (React Native)      │         │
│  │  Port: 5173      │              │  (Expo)              │         │
│  └────────┬─────────┘              └──────────┬──────────┘         │
└───────────┼────────────────────────────────────┼───────────────────┘
            │                                    │
            │         HTTP/REST + WebSocket      │
            └────────────┬───────────────────────┘
                         │
         ┌───────────────▼───────────────┐
         │      API GATEWAY              │
         │      Port: 3000               │
         │  ┌──────────────────────┐    │
         │  │ JWT Authentication   │    │
         │  │ Rate Limiter         │    │
         │  │ Input Validation     │    │
         │  └──────────────────────┘    │
         └───────────┬───────────────────┘
                     │
         ┌───────────▼───────────────┐
         │    ORCHESTRATOR           │
         │    Port: 3001             │
         │  Order Lifecycle Mgmt     │
         └────┬──────────────┬───────┘
              │              │
     ┌────────▼────┐    ┌───▼──────────┐
     │   MongoDB   │    │  RabbitMQ    │
     │   Database  │    │  Port: 5672  │
     └─────────────┘    └───┬──┬───┬───┘
                            │  │   │
            ┌───────────────┘  │   └──────────────┐
            │                  │                   │
    ┌───────▼────────┐ ┌──────▼───────┐ ┌────────▼────────┐
    │  CMS ADAPTER   │ │  ROS ADAPTER │ │  WMS ADAPTER    │
    │  SOAP/XML      │ │  REST/JSON   │ │  TCP Socket     │
    └───────┬────────┘ └──────┬───────┘ └────────┬────────┘
            │                 │                   │
    ┌───────▼────────┐ ┌──────▼───────┐ ┌────────▼────────┐
    │   CMS MOCK     │ │   ROS MOCK   │ │   WMS MOCK      │
    │   Port: 4000   │ │   Port: 4001 │ │   Port: 4002    │
    │   SOAP Server  │ │   REST API   │ │   TCP Server    │
    └────────────────┘ └──────────────┘ └─────────────────┘

            Events Flow Back via RabbitMQ
                         │
             ┌───────────▼──────────────┐
             │  NOTIFICATION SERVICE    │
             │  Port: 3002              │
             │  Socket.io WebSocket     │
             └───────────┬──────────────┘
                         │
                         ▼
                  (Real-time to Clients)
```

### 3.2 Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  React.js • React Native • Socket.io Client • Axios         │
└─────────────────────────────────────────────────────────────┘
                               │
┌─────────────────────────────▼───────────────────────────────┐
│                      API/GATEWAY LAYER                       │
│  Express.js • JWT • Rate Limiting • Input Validation        │
└─────────────────────────────────────────────────────────────┘
                               │
┌─────────────────────────────▼───────────────────────────────┐
│                   BUSINESS LOGIC LAYER                       │
│  Node.js Orchestrator • Order Lifecycle Management          │
└─────────────────────────────────────────────────────────────┘
                               │
┌─────────────────────────────▼───────────────────────────────┐
│                  INTEGRATION LAYER                           │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  SOAP    │    │  REST    │    │   TCP    │              │
│  │ Adapter  │    │ Adapter  │    │ Adapter  │              │
│  └──────────┘    └──────────┘    └──────────┘              │
└─────────────────────────────────────────────────────────────┘
                               │
┌─────────────────────────────▼───────────────────────────────┐
│                   MESSAGE BROKER LAYER                       │
│              RabbitMQ • AMQP • Pub/Sub                       │
└─────────────────────────────────────────────────────────────┘
                               │
┌─────────────────────────────▼───────────────────────────────┐
│                     DATA LAYER                               │
│              MongoDB • Mongoose • NoSQL                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Design Patterns

### 4.1 Architectural Patterns

| Pattern           | Implementation         | Purpose                 | Benefits                                                                                |
| ----------------- | ---------------------- | ----------------------- | --------------------------------------------------------------------------------------- |
| **API Gateway**   | Express.js @ Port 3000 | Single entry point      | - Centralized auth<br>- Hide backend complexity<br>- Rate limiting<br>- Security shield |
| **Orchestrator**  | Node.js @ Port 3001    | Transaction coordinator | - Order lifecycle management<br>- Status tracking<br>- Non-blocking responses           |
| **Adapter**       | CMS/ROS/WMS Adapters   | Protocol translation    | - Legacy system integration<br>- Unified internal format<br>- Decoupled services        |
| **Pub/Sub**       | RabbitMQ AMQP          | Event-driven messaging  | - Asynchronous processing<br>- Service decoupling<br>- Scalability                      |
| **Event-Driven**  | Entire system          | Real-time updates       | - Non-blocking<br>- Responsive<br>- Parallel processing                                 |
| **Microservices** | Independent services   | Service isolation       | - Independent deployment<br>- Technology flexibility<br>- Fault isolation               |

### 4.2 Adapter Pattern Details

The adapter pattern transforms various protocols into a unified internal JSON format:

```
┌────────────────────────────────────────────────────────────┐
│              UNIFIED INTERNAL FORMAT (JSON)                 │
│  {                                                          │
│    orderId: "ORD-123",                                      │
│    customerName: "John Doe",                                │
│    pickup: "Colombo", delivery: "Kandy"                     │
│  }                                                          │
└───────────────────┬────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│   CMS    │  │   ROS    │  │   WMS    │
│ ADAPTER  │  │ ADAPTER  │  │ ADAPTER  │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │            │            │
     │Transform   │Transform   │Transform
     ▼            ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│   XML    │  │   JSON   │  │  BINARY  │
│  SOAP    │  │   REST   │  │   TCP    │
│ Envelope │  │  Payload │  │  Packet  │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │            │            │
     ▼            ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Legacy   │  │ Third-   │  │ Old      │
│ CMS      │  │ Party    │  │ Warehouse│
│ System   │  │ ROS API  │  │ System   │
└──────────┘  └──────────┘  └──────────┘
```

### 4.3 Message Queue Pattern

```
                     ┌─────────────────────────┐
                     │      ORCHESTRATOR       │
                     │   (Order Received)      │
                     └───────────┬─────────────┘
                                 │ Publish
                                 ▼
                     ┌─────────────────────────┐
                     │      RABBITMQ           │
                     │  ┌──────────────────┐   │
                     │  │ order_exchange   │   │
                     │  │   (topic)        │   │
                     │  └────────┬─────────┘   │
                     │           │             │
                     │  ┌────────▼─────────┐   │
                     │  │ new_order_queue  │   │
                     │  │    (durable)     │   │
                     │  └────────┬─────────┘   │
                     └───────────┼─────────────┘
                                 │
                 ┌───────────────┼───────────────┐
                 │               │               │
                 ▼               ▼               ▼
         ┌───────────┐   ┌───────────┐   ┌───────────┐
         │    CMS    │   │    ROS    │   │    WMS    │
         │  Adapter  │   │  Adapter  │   │  Adapter  │
         │ Consumer  │   │ Consumer  │   │ Consumer  │
         └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
               │               │               │
               └───────────────┼───────────────┘
                               │ Publish Events
                               ▼
                     ┌─────────────────────────┐
                     │      RABBITMQ           │
                     │  ┌──────────────────┐   │
                     │  │ events_exchange  │   │
                     │  │   (fanout)       │   │
                     │  └────────┬─────────┘   │
                     └───────────┼─────────────┘
                                 │
                                 ▼
                     ┌─────────────────────────┐
                     │   NOTIFICATION SERVICE  │
                     │      (Consumer)         │
                     └───────────┬─────────────┘
                                 │ Broadcast
                                 ▼
                             WebSocket Clients
```

---

## 5. Data Flows

### 5.1 Order Submission Flow (Detailed Sequence)

```
Client    Gateway   Orchestrator  MongoDB  RabbitMQ   Adapters    Notification  Client
  │         │           │            │         │          │            │          │
  │─POST────▶│           │            │         │          │            │          │
  │ /orders │           │            │         │          │            │          │
  │         │──Validate─│            │         │          │            │          │
  │         │   JWT     │            │         │          │            │          │
  │         │──Forward──▶│            │         │          │            │          │
  │         │           │──Save──────▶│         │          │            │          │
  │         │           │  (RECEIVED) │         │          │            │          │
  │         │           │◀───OK───────│         │          │            │          │
  │         │           │──Publish────────────▶│          │            │          │
  │◀─202────│◀──202─────│            │         │          │            │          │
  │Accepted │  Accepted │            │     ┌───┴───┐      │            │          │
  │         │           │            │     │Fanout │      │            │          │
  │         │           │            │     └┬──┬──┬┘      │            │          │
  │         │           │            │      │  │  └───────▶ WMS        │          │
  │         │           │            │      │  └──────────▶ ROS        │          │
  │         │           │            │      └─────────────▶ CMS        │          │
  │         │           │            │          ┌─────────┴────┐       │          │
  │         │           │            │          │ PARALLEL     │       │          │
  │         │           │            │          │ PROCESSING   │       │          │
  │         │           │            │          └─────────┬────┘       │          │
  │         │           │◀─Update────────────────────────│            │          │
  │         │           │            │     ┌──Event───────│            │          │
  │         │           │            │     │              │            │          │
  │         │           │            │     ▼              │            │          │
  │         │           │            │  RabbitMQ──────────────────────▶│          │
  │         │           │            │  (events)                       │──Push────▶│
  │         │           │            │                                 │WebSocket │
```

### 5.2 Message Flow Steps

```
1. Client submits order (JSON) → API Gateway
2. Gateway validates JWT and data
3. Gateway forwards to Orchestrator
4. Orchestrator saves to MongoDB (Status: RECEIVED)
5. Orchestrator publishes to RabbitMQ
6. Orchestrator returns 202 Accepted to client

--- Parallel Processing (all adapters run simultaneously) ---

7a. CMS Adapter picks up message → Calls CMS SOAP → Updates status
7b. ROS Adapter picks up message → Calls ROS REST → Stores route
7c. WMS Adapter picks up message → Calls WMS TCP → Updates status

8. Each adapter publishes completion event to RabbitMQ
9. Notification Service consumes events
10. Notification Service broadcasts to client via WebSocket
11. Client sees real-time status update
```

### 5.3 Complete Order Lifecycle

```
1. ORDER INTAKE (Client Portal)
   ├─► POST /api/orders/ (CMS)
   │   Status: PENDING → CONFIRMED
   ▼

2. WAREHOUSE RECEIPT (WMS)
   ├─► POST /api/packages/ (WMS)
   │   Tracking: SL100001
   │   Status: RECEIVED
   ▼

3. QUALITY INSPECTION (WMS)
   ├─► POST /api/packages/{id}/inspect
   │   Condition: GOOD/FAIR/DAMAGED
   │   Status: INSPECTED
   ▼

4. WAREHOUSE STORAGE (WMS)
   ├─► POST /api/packages/{id}/store
   │   Location: ZONE-A-RACK-12-SHELF-3
   │   Status: STORED
   ▼

5. ROUTE OPTIMIZATION (ROS)
   ├─► POST /api/manifests/
   │   Optimize delivery sequence
   │   Manifest: MAN-2026-2001
   ▼

6. LOADING (WMS)
   ├─► POST /api/packages/{id}/load
   │   Assign to driver
   │   Status: LOADED
   ▼

7. DELIVERY START (Driver App)
   ├─► POST /api/manifests/{id}/start
   │   GPS tracking enabled
   │   Status: IN_PROGRESS
   ▼

8. DELIVERY COMPLETION (Driver App)
   ├─► POST /api/orders/{id}/mark-delivered
   │   Capture signature/photo
   │   Status: DELIVERED
   │   OR
   ├─► POST /api/orders/{id}/mark-failed
   │   Status: FAILED
   ▼

9. BILLING (Automated)
   └─► POST /api/billing/
       Invoice: INV-2026-10001
```

### 5.4 Data Flow Diagram

```
Client Order → CMS (Order Created)
                 │
                 ├─► WMS (Package Received)
                 │    │
                 │    ├─► Inspect → Store → Pick
                 │    │
                 │    └─► Package Ready
                 │
                 ├─► ROS (Route Optimization)
                 │    │
                 │    ├─► Create Manifest
                 │    │
                 │    └─► Optimize Sequence
                 │
                 ├─► WMS (Load Package)
                 │
                 ├─► Driver (Start Delivery)
                 │
                 ├─► Driver (Complete Delivery)
                 │
                 └─► CMS (Generate Invoice)
```

---

## 6. User Journey Workflows

### 6.1 User Registration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     WEB CLIENT PORTAL                            │
│                   Registration Form                              │
│  - Name, Email, Password                                        │
│  - Company Name                                                  │
│  - Phone Number                                                  │
│  - Address                                                       │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       │ 1. POST /api/auth/register
                       │    { name, email, password, company, ... }
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY                                 │
│                      Port 3000                                   │
└───┬─────────────────────────────────────────────────────────────┘
    │
    │ 2. Validate Input
    │    - Email format validation
    │    - Password strength check
    │    - Required fields check
    │
    │ 3. Forward to CMS Mock
    │    POST http://cms-mock:3001/api/customers
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CMS MOCK SERVICE                            │
│                      Port 4000                                   │
└───┬─────────────────────────────────────────────────────────────┘
    │
    │ 4. Check if email exists
    │    - Query customers.json
    │    - Return error if duplicate
    │
    │ 5. Hash password (bcrypt)
    │
    │ 6. Generate customer ID
    │    - UUID v4
    │
    │ 7. Create customer record
    │    - Save to customers.json
    │    - Status: "active"
    │
    │ 8. Return customer data
    │    { id, name, email, company, status }
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY                                 │
└───┬─────────────────────────────────────────────────────────────┘
    │
    │ 9. Return success to client
    │    201 Created
    │    { message: "Registration successful", user: {...} }
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                     WEB CLIENT PORTAL                            │
│                   Redirect to Login                              │
└─────────────────────────────────────────────────────────────────┘
```

**Registration Data Structure:**

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePassword123!",
  "company": "Acme Corp",
  "phone": "+94-77-1234567",
  "address": "123 Main St, Colombo",
  "role": "client"
}
```

---

### 6.2 User Login Flow (Detailed)

```
┌─────────────────────────────────────────────────────────────────┐
│                     WEB CLIENT PORTAL                            │
│                      Login Form                                  │
│  - Email: user@example.com                                      │
│  - Password: ********                                            │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       │ 1. POST /api/auth/login
                       │    { email, password }
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY (Port 3000)                     │
│                   JWT Authentication Middleware                  │
└───┬─────────────────────────────────────────────────────────────┘
    │
    │ 2. Validate Input
    │    - Email format
    │    - Password present
    │
    │ 3. Forward to CMS Mock
    │    POST http://cms-mock:3001/api/auth/login
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CMS MOCK SERVICE (Port 4000)                   │
└───┬─────────────────────────────────────────────────────────────┘
    │
    │ 4. Find user by email
    │    - Read customers.json
    │    - Return 401 if not found
    │
    │ 5. Verify password
    │    - bcrypt.compare(password, hashedPassword)
    │    - Return 401 if mismatch
    │
    │ 6. Check account status
    │    - Verify status === "active"
    │    - Return 403 if inactive
    │
    │ 7. Return user data
    │    { id, name, email, role, company }
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY                                 │
└───┬─────────────────────────────────────────────────────────────┘
    │
    │ 8. Generate JWT Token
    │    jwt.sign({
    │      userId: user.id,
    │      email: user.email,
    │      role: user.role
    │    }, JWT_SECRET, { expiresIn: '24h' })
    │
    │ 9. Return response
    │    200 OK
    │    {
    │      token: "eyJhbGciOiJIUzI1NiIs...",
    │      user: { id, name, email, role }
    │    }
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                     WEB CLIENT PORTAL                            │
└───┬─────────────────────────────────────────────────────────────┘
    │
    │ 10. Store Auth Data
    │     localStorage.setItem('authToken', token)
    │     localStorage.setItem('user', JSON.stringify(user))
    │
    │ 11. Update UI State
    │     - Set authenticated = true
    │     - Update AuthContext
    │
    │ 12. Redirect to Dashboard
    │     navigate('/dashboard')
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DASHBOARD PAGE                               │
│  - Welcome message                                              │
│  - Order management                                              │
│  - Billing information                                           │
└─────────────────────────────────────────────────────────────────┘
```

**JWT Token Structure:**

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "role": "client",
    "iat": 1738652100,
    "exp": 1738738500
  },
  "signature": "HMACSHA256(...)"
}
```

**Subsequent Authenticated Requests:**

```
Client Request → API Gateway
                  │
                  ├─ 1. Extract token from header
                  │    Authorization: Bearer <token>
                  │
                  ├─ 2. Verify JWT signature
                  │    jwt.verify(token, JWT_SECRET)
                  │
                  ├─ 3. Check expiration
                  │    if expired → 401 Unauthorized
                  │
                  ├─ 4. Attach user to request
                  │    req.user = decoded
                  │
                  └─ 5. Forward to backend services
```

---

### 6.3 Place Order Flow (Complete Journey)

```
┌─────────────────────────────────────────────────────────────────┐
│                     WEB CLIENT PORTAL                            │
│                   Order Submission Form                          │
│  - Pickup Location: Colombo Central                            │
│  - Delivery Address: Kandy Main Street                          │
│  - Package Details: Electronics                                 │
│  - Priority: Standard/Urgent                                    │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       │ 1. User fills form
                       │    - Enter pickup/delivery
                       │    - Package weight/dimensions
                       │    - Select priority
                       │
                       │ 2. Client-side validation
                       │    - Required fields
                       │    - Format validation
                       │
                       │ 3. POST /api/orders
                       │    Authorization: Bearer <JWT_TOKEN>
                       │    {
                       │      pickupLocation: {...},
                       │      deliveryAddress: {...},
                       │      packageDetails: {...},
                       │      priority: "standard"
                       │    }
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                  API GATEWAY (Port 3000)                         │
│                  Authentication & Validation Layer               │
└───┬─────────────────────────────────────────────────────────────┘
    │
    │ 4. JWT Authentication
    │    - Extract token from header
    │    - Verify signature & expiration
    │    - Attach user info to request
    │
    │ 5. Rate Limiting Check
    │    - Check request count (100/15min)
    │    - Return 429 if exceeded
    │
    │ 6. Input Validation
    │    - express-validator rules
    │    - Pickup/delivery required
    │    - Valid coordinates
    │    - Weight/dimensions within limits
    │
    │ 7. Forward to Orchestrator
    │    POST http://orchestrator:3001/api/orders
    │    - Add user ID from JWT
    │    - Include timestamp
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                  ORCHESTRATOR (Port 3001)                        │
│                  Transaction Coordinator                         │
└───┬─────────────────────────────────────────────────────────────┘
    │
    │ 8. Generate Order ID
    │    orderId = "ORD-" + Date.now() + "-" + uuid()
    │    Example: ORD-1738652100-a1b2c3
    │
    │ 9. Create Order Object
    │    {
    │      orderId: "ORD-...",
    │      customerId: req.user.userId,
    │      status: "RECEIVED",
    │      pickupLocation: {...},
    │      deliveryAddress: {...},
    │      packageDetails: {...},
    │      priority: "standard",
    │      cmsStatus: "PENDING",
    │      rosStatus: "PENDING",
    │      wmsStatus: "PENDING",
    │      createdAt: new Date(),
    │      updatedAt: new Date()
    │    }
    │
    │ 10. Persist to MongoDB
    │     await Order.create(orderObject)
    │     - Save to swiftlogistics database
    │     - orders collection
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                  MONGODB (Port 27017)                            │
│                  Document Stored in 'orders' collection         │
└─────────────────────────────────────────────────────────────────┘
    │
    │ 11. Return success to Orchestrator
    │     { _id, orderId, ... }
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                  ORCHESTRATOR                                    │
└───┬─────────────────────────────────────────────────────────────┘
    │
    │ 12. Publish to RabbitMQ
    │     channel.publish(
    │       'order_exchange',
    │       'order.new',
    │       orderObject
    │     )
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                  RABBITMQ (Port 5672)                            │
│                  Message Queue                                   │
└───┬─────────────────────────────────────────────────────────────┘
    │
    │ 13. Fanout to Queues
    │     ├─ new_order_queue (CMS)
    │     ├─ new_order_queue (ROS)
    │     └─ new_order_queue (WMS)
    │
    ├──────────────┬──────────────┬──────────────┐
    │              │              │              │
    ▼              ▼              ▼              │
┌──────────┐ ┌──────────┐ ┌──────────┐         │
│   CMS    │ │   ROS    │ │   WMS    │         │
│ ADAPTER  │ │ ADAPTER  │ │ ADAPTER  │         │
└────┬─────┘ └────┬─────┘ └────┬─────┘         │
     │            │            │                │
     │            │            │                │
     │ PARALLEL PROCESSING BEGINS               │
     │            │            │                │
     ▼            ▼            ▼                │
┌──────────┐ ┌──────────┐ ┌──────────┐         │
│ CMS Mock │ │ ROS Mock │ │ WMS Mock │         │
│Port 4000 │ │Port 4001 │ │Port 4002 │         │
└────┬─────┘ └────┬─────┘ └────┬─────┘         │
     │            │            │                │
     │            │            │                │
     │ Process    │ Calculate  │ Check         │
     │ Customer   │ Route      │ Warehouse     │
     │ Contract   │ Optimize   │ Capacity      │
     │            │            │                │
     └────────────┴────────────┴────────────────┘
                       │
                       │ 14. Update Orchestrator
                       │     PUT /api/orders/{orderId}/status
                       │     - cmsStatus: "SUCCESS"
                       │     - rosStatus: "SUCCESS"
                       │     - wmsStatus: "SUCCESS"
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                  ORCHESTRATOR                                    │
└───┬─────────────────────────────────────────────────────────────┘
    │
    │ 15. Update Order Status
    │     status: "PROCESSING" → "CONFIRMED"
    │
    │ 16. Publish Event
    │     channel.publish(
    │       'events_exchange',
    │       '',
    │       {
    │         type: "ORDER_CONFIRMED",
    │         orderId: "ORD-...",
    │         data: { status: "CONFIRMED" }
    │       }
    │     )
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│             NOTIFICATION SERVICE (Port 3002)                     │
│             WebSocket Server                                     │
└───┬─────────────────────────────────────────────────────────────┘
    │
    │ 17. Consume Event from RabbitMQ
    │     - Receive ORDER_CONFIRMED event
    │
    │ 18. Broadcast via WebSocket
    │     io.emit('order-update', {
    │       orderId: "ORD-...",
    │       status: "CONFIRMED",
    │       message: "Your order has been confirmed!"
    │     })
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                     WEB CLIENT PORTAL                            │
│                     (WebSocket Connected)                        │
└───┬─────────────────────────────────────────────────────────────┘
    │
    │ 19. Receive Real-time Update
    │     socket.on('order-update', (data) => {
    │       // Update UI with new status
    │       showNotification(data.message)
    │     })
    │
    │ 20. Display to User
    │     ✓ Order confirmed!
    │     📦 Order ID: ORD-1738652100-a1b2c3
    │     🚚 Estimated delivery: 2 days
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                     USER SEES CONFIRMATION                       │
│  "Your order has been successfully placed and confirmed!"       │
│  "You will receive updates in real-time."                       │
└─────────────────────────────────────────────────────────────────┘
```

**Meanwhile, back at Orchestrator:**

```
│ Step 3 (from above): Return response to API Gateway
│     202 Accepted (Non-blocking response)
│     {
│       orderId: "ORD-1738652100-a1b2c3",
│       status: "RECEIVED",
│       message: "Order received and being processed",
│       estimatedTime: "2-3 business days"
│     }
│
▼
API GATEWAY → Returns to Client
│
▼
WEB CLIENT PORTAL
│ User sees immediate confirmation:
│ "✓ Order submitted successfully!"
│ "You'll receive real-time updates as it's processed"
```

**Complete Timeline:**

```
T+0ms    : User clicks "Submit Order"
T+50ms   : API Gateway validates & forwards
T+100ms  : Orchestrator saves to MongoDB
T+150ms  : Orchestrator publishes to RabbitMQ
T+200ms  : Client receives "202 Accepted" response
T+250ms  : Adapters start processing (parallel)
T+2000ms : Adapters complete, update orchestrator
T+2050ms : Event published to notification queue
T+2100ms : WebSocket pushes update to client
T+2150ms : User sees "Order Confirmed!" notification
```

---

## 7. Docker Container Communication

### 7.1 Docker Networking Architecture

**Network Name:** `swiftlogistics-network`  
**Driver:** bridge  
**Subnet:** Auto-assigned by Docker

All containers communicate within an isolated Docker bridge network, providing:

- **Service Discovery**: Containers can reference each other by service name
- **Network Isolation**: External traffic cannot reach internal services
- **Port Mapping**: Selective exposure of services to host machine

```
┌─────────────────────────────────────────────────────────────────┐
│                          HOST MACHINE                            │
│                      (Your Computer)                             │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       │ Port Mappings:
                       │ 3000 → api-gateway:3000
                       │ 3001 → orchestrator:3001
                       │ 3002 → notification:3002
                       │ 4000 → cms-mock:3001
                       │ 4001 → ros-mock:3003
                       │ 4002 → wms-mock:3002
                       │ 27017 → mongodb:27017
                       │ 5672 → rabbitmq:5672
                       │ 15672 → rabbitmq:15672
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│              DOCKER BRIDGE NETWORK                               │
│              swiftlogistics-network                              │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  LAYER 1: CLIENT-FACING SERVICES                         │  │
│  │                                                           │  │
│  │  ┌────────────────┐                                      │  │
│  │  │  api-gateway   │  Accessible from host via port 3000  │  │
│  │  │  Port: 3000    │  Internal: http://api-gateway:3000   │  │
│  │  └────────┬───────┘                                      │  │
│  └───────────┼──────────────────────────────────────────────┘  │
│              │                                                  │
│  ┌───────────▼──────────────────────────────────────────────┐  │
│  │  LAYER 2: ORCHESTRATION SERVICES                         │  │
│  │                                                           │  │
│  │  ┌────────────────┐      ┌─────────────────┐            │  │
│  │  │ orchestrator   │      │ notification-   │            │  │
│  │  │ Port: 3001     │      │ service         │            │  │
│  │  │                │      │ Port: 3002      │            │  │
│  │  └────────┬───────┘      └────────┬────────┘            │  │
│  └───────────┼───────────────────────┼──────────────────────┘  │
│              │                       │                         │
│  ┌───────────┼───────────────────────┼──────────────────────┐  │
│  │  LAYER 3: INFRASTRUCTURE                                 │  │
│  │           │                       │                       │  │
│  │  ┌────────▼─────────┐    ┌───────▼─────────┐            │  │
│  │  │    mongodb       │    │    rabbitmq     │            │  │
│  │  │    Port: 27017   │    │    Port: 5672   │            │  │
│  │  └──────────────────┘    │    Port: 15672  │            │  │
│  │                          └─────────────────┘            │  │
│  └──────────────────────────────────────────────────────────┘  │
│              │                                                  │
│  ┌───────────▼──────────────────────────────────────────────┐  │
│  │  LAYER 4: INTEGRATION ADAPTERS                           │  │
│  │                                                           │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │  │
│  │  │ cms-adapter │  │ ros-adapter │  │ wms-adapter │      │  │
│  │  │ (no port)   │  │ (no port)   │  │ (no port)   │      │  │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘      │  │
│  └─────────┼─────────────────┼─────────────────┼────────────┘  │
│            │                 │                 │               │
│  ┌─────────▼─────────────────▼─────────────────▼────────────┐  │
│  │  LAYER 5: MOCK SERVICES                                  │  │
│  │                                                           │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │  │
│  │  │  cms-mock  │  │  ros-mock  │  │  wms-mock  │         │  │
│  │  │ Port: 3001 │  │ Port: 3003 │  │ Port: 3002 │         │  │
│  │  └────────────┘  └────────────┘  └────────────┘         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Service-to-Service Communication Patterns

#### Pattern 1: HTTP REST Communication

```
┌─────────────────┐
│  api-gateway    │
└────────┬────────┘
         │ HTTP Request
         │ GET http://orchestrator:3001/api/orders/123
         │
         ▼
┌─────────────────┐
│  orchestrator   │
└────────┬────────┘
         │ HTTP Request
         │ GET http://mongodb:27017
         │
         ▼
┌─────────────────┐
│    mongodb      │
└─────────────────┘
```

**Environment Variable Configuration:**

```yaml
api-gateway:
  environment:
    ORCHESTRATOR_URL: http://orchestrator:3001
    # Uses service name, not localhost!

orchestrator:
  environment:
    MONGODB_URI: mongodb://admin:admin123@mongodb:27017/swiftlogistics
    # Uses service name 'mongodb'
```

#### Pattern 2: Message Queue Communication

```
┌─────────────────┐
│  orchestrator   │
└────────┬────────┘
         │ 1. Publish message
         │ amqp://rabbitmq:5672
         │
         ▼
┌─────────────────┐
│    rabbitmq     │
└────────┬────────┘
         │ 2. Fanout to subscribers
         │
    ┌────┼────┬────────┐
    │    │    │        │
    ▼    ▼    ▼        ▼
┌────┐ ┌────┐ ┌────┐
│CMS │ │ROS │ │WMS │
│Adpt│ │Adpt│ │Adpt│
└────┘ └────┘ └────┘
```

**Environment Variable Configuration:**

```yaml
orchestrator:
  environment:
    RABBITMQ_URL: amqp://admin:admin123@rabbitmq:5672

cms-adapter:
  environment:
    RABBITMQ_URL: amqp://admin:admin123@rabbitmq:5672
    # All adapters use same RabbitMQ URL with service name
```

#### Pattern 3: WebSocket Communication

```
┌─────────────────┐
│   Web Browser   │ (Outside Docker)
└────────┬────────┘
         │ ws://localhost:3002
         │ (Port mapping: 3002 → 3002)
         │
         ▼
┌─────────────────┐
│  notification-  │
│   service       │
└────────┬────────┘
         │ Subscribe to RabbitMQ
         │ amqp://rabbitmq:5672
         │
         ▼
┌─────────────────┐
│    rabbitmq     │
└─────────────────┘
```

### 7.3 Container Dependencies & Startup Order

**Docker Compose Dependencies:**

```yaml
services:
  # TIER 1: Infrastructure (Start First)
  mongodb:
    # No dependencies

  rabbitmq:
    # No dependencies

  # TIER 2: Mock Services (Start Second)
  cms-mock:
    # No dependencies

  ros-mock:
    # No dependencies

  wms-mock:
    # No dependencies

  # TIER 3: Core Services (Start Third)
  orchestrator:
    depends_on:
      mongodb:
        condition: service_healthy # Wait for health check
      rabbitmq:
        condition: service_healthy

  notification-service:
    depends_on:
      rabbitmq:
        condition: service_healthy

  api-gateway:
    depends_on:
      - orchestrator # Wait for start (not health)

  # TIER 4: Adapters (Start Last)
  cms-adapter:
    depends_on:
      rabbitmq:
        condition: service_healthy
      cms-mock:
        condition: service_started
      orchestrator:
        condition: service_started
```

**Health Check Examples:**

```yaml
mongodb:
  healthcheck:
    test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
    interval: 10s
    timeout: 5s
    retries: 5

rabbitmq:
  healthcheck:
    test: rabbitmq-diagnostics -q ping
    interval: 10s
    timeout: 5s
    retries: 5

cms-mock:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:3001/health"]
    interval: 30s
    timeout: 10s
    retries: 3
```

### 7.4 Volume Persistence

**Data Persistence Across Container Restarts:**

```yaml
volumes:
  mongodb_data:
    name: swiftlogistics-mongodb-data
  rabbitmq_data:
    name: swiftlogistics-rabbitmq-data

services:
  mongodb:
    volumes:
      - mongodb_data:/data/db
      # Persists database across restarts

  rabbitmq:
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
      # Persists messages/queues across restarts

  cms-mock:
    volumes:
      - ./services/mocks/cms-mock/data:/app/data
      # Bind mount for development (hot reload)
```

### 7.5 Inter-Container Communication Flow Example

**Complete Order Flow with Container Names:**

```
1. Browser → http://localhost:3000/api/orders
   (Host port mapping)

2. Docker routes to: api-gateway:3000
   (Internal container port)

3. api-gateway → http://orchestrator:3001/api/orders
   (Service name resolution via Docker DNS)

4. orchestrator → mongodb://mongodb:27017
   (Database connection using service name)

5. orchestrator → amqp://rabbitmq:5672
   (Message queue using service name)

6. rabbitmq → [cms-adapter, ros-adapter, wms-adapter]
   (Fanout to all subscribers)

7. cms-adapter → http://cms-mock:3001/api/customers
   (Note: cms-mock runs on internal port 3001,
    exposed to host as 4000)

8. ros-adapter → http://ros-mock:3003/api/routes
   (Internal port 3003, exposed as 4001)

9. wms-adapter → http://wms-mock:3002/api/inventory
   (Internal port 3002, exposed as 4002)

10. adapters → http://orchestrator:3001/api/orders/{id}/status
    (Update order status)

11. orchestrator → amqp://rabbitmq:5672
    (Publish completion event)

12. notification-service (subscribed to rabbitmq)
    → WebSocket push to Browser
    (ws://localhost:3002 from browser perspective)
```

**Key Principle:**

- **Internal communication**: Use service names (e.g., `http://orchestrator:3001`)
- **External access**: Use `localhost` with mapped ports (e.g., `http://localhost:3000`)

### 7.6 Network Troubleshooting Commands

```bash
# Inspect the network
docker network inspect swiftlogistics-network

# Check which containers are on the network
docker network inspect swiftlogistics-network | grep Name

# Test connectivity between containers
docker exec swiftlogistics-api-gateway ping orchestrator
docker exec swiftlogistics-orchestrator ping mongodb
docker exec swiftlogistics-cms-adapter ping cms-mock

# Check DNS resolution
docker exec swiftlogistics-api-gateway nslookup orchestrator
docker exec swiftlogistics-api-gateway nslookup rabbitmq

# View container logs
docker logs swiftlogistics-api-gateway
docker logs swiftlogistics-orchestrator -f

# Check open ports inside a container
docker exec swiftlogistics-orchestrator netstat -tuln
```

---

## 8. API Gateway Deep Dive

### 8.1 Request Processing Pipeline

The API Gateway acts as the single entry point for all client requests, implementing multiple layers of middleware for security, validation, and routing.

**Middleware Execution Flow:**

```
┌─────────────────────────────────────────────────────────────────┐
│                      INCOMING REQUEST                            │
│  POST http://localhost:3000/api/orders                          │
│  Headers:                                                        │
│    Authorization: Bearer eyJhbGciOiJIUzI1NiIs...                │
│    Content-Type: application/json                               │
│  Body: { pickupLocation: {...}, deliveryAddress: {...} }        │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 1: CORS MIDDLEWARE                                       │
│  - Check origin header                                          │
│  - Set Access-Control-Allow-Origin                              │
│  - Set Access-Control-Allow-Methods                             │
│  - Set Access-Control-Allow-Headers                             │
│  ✓ Allow request from http://localhost:5173                     │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 2: HELMET SECURITY MIDDLEWARE                            │
│  - Set X-Content-Type-Options: nosniff                          │
│  - Set X-Frame-Options: DENY                                    │
│  - Set X-XSS-Protection: 1; mode=block                          │
│  - Remove X-Powered-By header                                   │
│  ✓ Security headers applied                                     │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 3: BODY PARSER MIDDLEWARE                                │
│  - Parse JSON payload                                           │
│  - Limit body size (10MB)                                       │
│  - Validate JSON syntax                                         │
│  ✓ req.body = { pickupLocation: {...}, ... }                    │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 4: RATE LIMITER MIDDLEWARE                               │
│  - Extract client IP: req.ip                                    │
│  - Check request count in time window                           │
│  - Window: 15 minutes (900,000ms)                               │
│  - Max requests: 100                                            │
│  - Current: 45/100 requests                                     │
│  ✓ Rate limit OK, proceed                                       │
│                                                                  │
│  [If exceeded]                                                  │
│  ✗ 429 Too Many Requests                                        │
│    { error: "Too many requests, try again later" }              │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 5: JWT AUTH MIDDLEWARE                                   │
│  - Extract token from header                                    │
│    Authorization: Bearer <token>                                │
│  - Verify JWT signature                                         │
│    jwt.verify(token, JWT_SECRET)                                │
│  - Check expiration                                             │
│    if (decoded.exp < Date.now()/1000) → 401                     │
│  - Attach user to request                                       │
│    req.user = {                                                 │
│      userId: "550e8400-e29b-41d4-a716-446655440000",            │
│      email: "user@example.com",                                 │
│      role: "client"                                             │
│    }                                                            │
│  ✓ Authentication successful                                    │
│                                                                  │
│  [If invalid/missing token]                                     │
│  ✗ 401 Unauthorized                                             │
│    { error: "Invalid or missing token" }                        │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 6: INPUT VALIDATION MIDDLEWARE                           │
│  - express-validator rules                                      │
│  - Check required fields:                                       │
│    ✓ pickupLocation exists                                      │
│    ✓ deliveryAddress exists                                     │
│    ✓ packageDetails exists                                      │
│  - Validate formats:                                            │
│    ✓ pickupLocation.lat is numeric (-90 to 90)                  │
│    ✓ pickupLocation.lng is numeric (-180 to 180)                │
│    ✓ packageDetails.weight > 0                                  │
│  - Sanitize inputs                                              │
│  ✓ All validations passed                                       │
│                                                                  │
│  [If validation fails]                                          │
│  ✗ 400 Bad Request                                              │
│    { errors: [{ field, message }] }                             │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 7: ROUTE HANDLER                                         │
│  - Match route: POST /api/orders                                │
│  - Execute controller function                                  │
│  - Prepare request for orchestrator:                            │
│    {                                                            │
│      ...req.body,                                               │
│      customerId: req.user.userId,                               │
│      timestamp: new Date()                                      │
│    }                                                            │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 8: PROXY TO ORCHESTRATOR                                 │
│  - Forward to backend service                                   │
│    POST http://orchestrator:3001/api/orders                     │
│  - Add internal headers                                         │
│    X-User-Id: req.user.userId                                   │
│    X-Request-Id: uuid()                                         │
│  - Set timeout: 30 seconds                                      │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                  ORCHESTRATOR SERVICE                            │
│  - Process order                                                │
│  - Returns: 202 Accepted                                        │
│    { orderId, status: "RECEIVED", message }                     │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 9: RESPONSE FORMATTING                                   │
│  - Add response headers                                         │
│    X-Response-Time: 145ms                                       │
│    Content-Type: application/json                               │
│  - Log request metrics                                          │
│    [INFO] POST /api/orders - 202 - 145ms                        │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                     RESPONSE TO CLIENT                           │
│  Status: 202 Accepted                                           │
│  Body: {                                                        │
│    orderId: "ORD-1738652100-a1b2c3",                            │
│    status: "RECEIVED",                                          │
│    message: "Order received and being processed"                │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 API Gateway Code Structure

**Key Files:**

```javascript
// services/api-gateway/index.js
const express = require("express");
const helmet = require("helmet");
const cors = require("cors");
const rateLimit = require("express-rate-limit");

const app = express();

// LAYER 1: CORS
app.use(
  cors({
    origin: ["http://localhost:5173", "http://localhost:3000"],
    credentials: true,
  }),
);

// LAYER 2: Security Headers
app.use(helmet());

// LAYER 3: Body Parser
app.use(express.json({ limit: "10mb" }));
app.use(express.urlencoded({ extended: true }));

// LAYER 4: Rate Limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: "Too many requests, please try again later.",
});
app.use("/api/", limiter);

// LAYER 5-7: Routes (include auth & validation)
app.use("/api/orders", require("./routes/orders"));
app.use("/api/driver", require("./routes/driver"));

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.status || 500).json({
    error: err.message || "Internal Server Error",
  });
});

app.listen(3000);
```

**Authentication Middleware:**

```javascript
// services/api-gateway/middleware/auth.js
const jwt = require("jsonwebtoken");

module.exports = (req, res, next) => {
  try {
    // Extract token
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return res.status(401).json({ error: "No token provided" });
    }

    const token = authHeader.substring(7);

    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    // Check expiration
    if (decoded.exp < Date.now() / 1000) {
      return res.status(401).json({ error: "Token expired" });
    }

    // Attach user to request
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ error: "Invalid token" });
  }
};
```

**Validation Middleware:**

```javascript
// services/api-gateway/middleware/validation.js
const { body, validationResult } = require("express-validator");

exports.validateOrder = [
  body("pickupLocation").notEmpty().withMessage("Pickup location required"),
  body("pickupLocation.lat").isFloat({ min: -90, max: 90 }),
  body("pickupLocation.lng").isFloat({ min: -180, max: 180 }),
  body("deliveryAddress").notEmpty().withMessage("Delivery address required"),
  body("packageDetails.weight").isFloat({ min: 0.1 }),

  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    next();
  },
];
```

---

## 9. RabbitMQ Event Routing Architecture

### 9.1 Exchange and Queue Configuration

RabbitMQ uses **exchanges** to route messages to **queues** based on routing rules. The SwiftLogistics system uses two primary exchanges:

```
┌─────────────────────────────────────────────────────────────────┐
│                        RABBITMQ BROKER                           │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  EXCHANGE 1: order_exchange (Topic)                    │    │
│  │  - Type: topic                                         │    │
│  │  - Durable: true                                       │    │
│  │  - Purpose: Route new orders to adapters               │    │
│  └───────────┬────────────────────────────────────────────┘    │
│              │                                                  │
│              │ Bindings (routing keys):                        │
│              ├─ order.new → new_order_queue                    │
│              ├─ order.update → order_update_queue              │
│              └─ order.* → all_orders_queue                     │
│              │                                                  │
│  ┌───────────▼────────────────────────────────────────────┐    │
│  │  QUEUE 1: new_order_queue                              │    │
│  │  - Durable: true                                       │    │
│  │  - Prefetch: 1 (process one at a time)                │    │
│  │  - Multiple consumers: CMS, ROS, WMS adapters          │    │
│  └───────────┬────────────────────────────────────────────┘    │
│              │                                                  │
│              │ Consumers (with tags):                          │
│              ├─ cms-adapter (consumer tag: cms-1)              │
│              ├─ ros-adapter (consumer tag: ros-1)              │
│              └─ wms-adapter (consumer tag: wms-1)              │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  EXCHANGE 2: events_exchange (Fanout)                  │    │
│  │  - Type: fanout                                        │    │
│  │  - Durable: true                                       │    │
│  │  - Purpose: Broadcast events to all listeners          │    │
│  └───────────┬────────────────────────────────────────────┘    │
│              │                                                  │
│              │ Fanout (no routing key needed):                 │
│              ├─ → notification_events_queue                    │
│              ├─ → audit_events_queue (future)                  │
│              └─ → analytics_events_queue (future)              │
│              │                                                  │
│  ┌───────────▼────────────────────────────────────────────┐    │
│  │  QUEUE 2: notification_events_queue                    │    │
│  │  - Durable: true                                       │    │
│  │  - Consumer: notification-service                      │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 Message Flow: Order Processing

**Step-by-Step Message Routing:**

```
1. ORCHESTRATOR PUBLISHES ORDER
┌─────────────────────────────────────────────────────────────────┐
│  Orchestrator Service                                           │
│  - Creates order in MongoDB                                     │
│  - Publishes message to RabbitMQ:                               │
│                                                                  │
│  channel.publish(                                               │
│    'order_exchange',           // Exchange name                 │
│    'order.new',                // Routing key                   │
│    Buffer.from(JSON.stringify({                                 │
│      orderId: 'ORD-123',                                        │
│      customerId: '550e8400...',                                 │
│      pickupLocation: {...},                                     │
│      deliveryAddress: {...},                                    │
│      packageDetails: {...},                                     │
│      timestamp: '2026-02-04T11:38:00Z'                          │
│    })),                                                         │
│    {                                                            │
│      persistent: true,         // Message survives restarts     │
│      contentType: 'application/json',                           │
│      messageId: uuid(),                                         │
│      timestamp: Date.now()                                      │
│    }                                                            │
│  );                                                             │
└─────────────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  RabbitMQ: order_exchange (Topic Exchange)                      │
│                                                                  │
│  - Receives message with routing key 'order.new'                │
│  - Checks all queue bindings                                    │
│  - Finds binding: 'order.new' → new_order_queue                 │
│  - Routes message to queue                                      │
└─────────────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  RabbitMQ: new_order_queue                                      │
│                                                                  │
│  - Stores message in queue                                      │
│  - Message count: 1                                             │
│  - Consumers: 3 (CMS, ROS, WMS adapters)                        │
│                                                                  │
│  RabbitMQ Work Queue Pattern:                                   │
│  - Each message delivered to ONE consumer only                  │
│  - Round-robin distribution                                     │
│  - Acknowledgment required before next delivery                 │
└─────────────────────────────────────────────────────────────────┘
                       │
                       │ [But we want ALL adapters to process!]
                       │ [Solution: Each adapter gets its own queue]
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  CORRECTED ARCHITECTURE: Separate Queues per Adapter            │
│                                                                  │
│  Exchange: order_exchange (Fanout, not Topic!)                  │
│  │                                                               │
│  ├─ Binding → cms_order_queue → CMS Adapter                     │
│  ├─ Binding → ros_order_queue → ROS Adapter                     │
│  └─ Binding → wms_order_queue → WMS Adapter                     │
│                                                                  │
│  Now each adapter processes the SAME message independently!     │
└─────────────────────────────────────────────────────────────────┘
```

### 9.3 Complete RabbitMQ Setup Code

**Orchestrator: Publisher Configuration**

```javascript
// services/orchestrator/services/messageQueue.js
const amqp = require("amqplib");

class MessageQueue {
  constructor() {
    this.connection = null;
    this.channel = null;
  }

  async connect() {
    // Connect to RabbitMQ
    this.connection = await amqp.connect(process.env.RABBITMQ_URL);
    this.channel = await this.connection.createChannel();

    // Declare ORDER exchange (Fanout - broadcasts to all)
    await this.channel.assertExchange("order_exchange", "fanout", {
      durable: true, // Survives broker restarts
    });

    // Declare EVENTS exchange (Fanout - broadcasts to all)
    await this.channel.assertExchange("events_exchange", "fanout", {
      durable: true,
    });

    console.log("[MessageQueue] Connected to RabbitMQ");
  }

  async publishOrder(orderData) {
    const message = Buffer.from(JSON.stringify(orderData));

    this.channel.publish(
      "order_exchange",
      "", // Routing key ignored in fanout
      message,
      {
        persistent: true,
        contentType: "application/json",
        timestamp: Date.now(),
      },
    );

    console.log(`[MessageQueue] Published order: ${orderData.orderId}`);
  }

  async publishEvent(eventType, eventData) {
    const event = {
      type: eventType,
      data: eventData,
      timestamp: new Date().toISOString(),
    };

    const message = Buffer.from(JSON.stringify(event));

    this.channel.publish("events_exchange", "", message, { persistent: true });

    console.log(`[MessageQueue] Published event: ${eventType}`);
  }
}

module.exports = new MessageQueue();
```

**Adapter: Consumer Configuration**

```javascript
// services/adapters/cms-adapter/services/queueConsumer.js
const amqp = require("amqplib");

class QueueConsumer {
  constructor(adapterName) {
    this.adapterName = adapterName;
    this.connection = null;
    this.channel = null;
  }

  async connect() {
    // Connect to RabbitMQ
    this.connection = await amqp.connect(process.env.RABBITMQ_URL);
    this.channel = await this.connection.createChannel();

    // Declare the exchange (idempotent - safe to redeclare)
    await this.channel.assertExchange("order_exchange", "fanout", {
      durable: true,
    });

    // Declare adapter-specific queue
    const queueName = `${this.adapterName}_order_queue`;
    await this.channel.assertQueue(queueName, {
      durable: true,
      exclusive: false, // Other consumers can use if needed
      autoDelete: false, // Don't delete when consumer disconnects
    });

    // Bind queue to exchange
    await this.channel.bindQueue(queueName, "order_exchange", "");

    // Set prefetch count (process one message at a time)
    await this.channel.prefetch(1);

    console.log(`[${this.adapterName}] Waiting for orders...`);

    // Start consuming
    this.channel.consume(
      queueName,
      async (msg) => {
        if (msg) {
          try {
            const orderData = JSON.parse(msg.content.toString());
            console.log(
              `[${this.adapterName}] Received order: ${orderData.orderId}`,
            );

            // Process order (call external service)
            await this.processOrder(orderData);

            // Acknowledge message (remove from queue)
            this.channel.ack(msg);
            console.log(`[${this.adapterName}] Order processed successfully`);
          } catch (error) {
            console.error(
              `[${this.adapterName}] Error processing order:`,
              error,
            );

            // Negative acknowledgment - requeue message
            this.channel.nack(msg, false, true);
          }
        }
      },
      {
        noAck: false, // Require manual acknowledgment
      },
    );
  }

  async processOrder(orderData) {
    // CMS Adapter: Transform to XML and call SOAP service
    // ROS Adapter: Call REST API for route optimization
    // WMS Adapter: Check warehouse capacity via TCP
    // Implementation specific to each adapter...
  }
}

module.exports = QueueConsumer;
```

### 9.4 Event Broadcasting to External Services

**Notification Service: Event Consumer**

```javascript
// services/notification-service/services/eventConsumer.js
const amqp = require("amqplib");
const socketManager = require("./socketManager");

class EventConsumer {
  async connect() {
    const connection = await amqp.connect(process.env.RABBITMQ_URL);
    const channel = await connection.createChannel();

    // Declare events exchange
    await channel.assertExchange("events_exchange", "fanout", {
      durable: true,
    });

    // Declare notification queue
    const queueName = "notification_events_queue";
    await channel.assertQueue(queueName, {
      durable: true,
    });

    // Bind to events exchange
    await channel.bindQueue(queueName, "events_exchange", "");

    console.log("[EventConsumer] Waiting for events...");

    // Consume events
    channel.consume(queueName, (msg) => {
      if (msg) {
        const event = JSON.parse(msg.content.toString());
        console.log(`[EventConsumer] Received event: ${event.type}`);

        // Broadcast to all connected WebSocket clients
        socketManager.broadcastEvent(event);

        // Acknowledge
        channel.ack(msg);
      }
    });
  }
}

module.exports = new EventConsumer();
```

**WebSocket Broadcasting:**

```javascript
// services/notification-service/services/socketManager.js
const socketIO = require("socket.io");

class SocketManager {
  constructor() {
    this.io = null;
  }

  initialize(server) {
    this.io = socketIO(server, {
      cors: {
        origin: ["http://localhost:5173"],
        credentials: true,
      },
    });

    this.io.on("connection", (socket) => {
      console.log(`[Socket] Client connected: ${socket.id}`);

      socket.on("disconnect", () => {
        console.log(`[Socket] Client disconnected: ${socket.id}`);
      });
    });
  }

  broadcastEvent(event) {
    // Broadcast to ALL connected clients
    this.io.emit("order-update", {
      orderId: event.data.orderId,
      status: event.data.status,
      message: event.data.message,
      timestamp: event.timestamp,
    });

    console.log(
      `[Socket] Broadcasted event to ${this.io.sockets.sockets.size} clients`,
    );
  }
}

module.exports = new SocketManager();
```

### 9.5 Message Acknowledgment Patterns

```
┌─────────────────────────────────────────────────────────────────┐
│  Pattern 1: MANUAL ACKNOWLEDGMENT (Reliable Processing)         │
│                                                                  │
│  Queue → Consumer                                               │
│    │                                                             │
│    ├─ Deliver message                                           │
│    │                                                             │
│    │  Consumer processes:                                       │
│    │  1. Parse message                                          │
│    │  2. Call external service                                  │
│    │  3. Update database                                        │
│    │                                                             │
│    │  If SUCCESS:                                               │
│    │    channel.ack(msg)  ✓                                     │
│    │    → Message removed from queue                            │
│    │                                                             │
│    │  If FAILURE:                                               │
│    │    channel.nack(msg, false, true)                          │
│    │    → Message requeued for retry                            │
│    │                                                             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Pattern 2: AUTO ACKNOWLEDGMENT (Fire and Forget)               │
│                                                                  │
│  Queue → Consumer                                               │
│    │                                                             │
│    ├─ Deliver message                                           │
│    └─ Immediately acknowledge (noAck: true)                     │
│                                                                  │
│  ⚠️ Message removed before processing                           │
│  ⚠️ If consumer fails, message is lost!                         │
│  ⚠️ Not recommended for critical operations                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 9.6 RabbitMQ Management & Monitoring

**Access RabbitMQ Management UI:**

```
URL: http://localhost:15672
Username: admin
Password: admin123
```

**Key Metrics to Monitor:**

```
Queues:
  - Message count (ready + unacknowledged)
  - Consumer count (active consumers)
  - Message rate (in/out per second)
  - Acknowledgment rate

Exchanges:
  - Publish rate (messages per second)
  - Return rate (unroutable messages)

Connections:
  - Active connections per service
  - Channel count
  - Connection state
```

**CLI Commands:**

```bash
# List all queues
docker exec swiftlogistics-rabbitmq rabbitmqctl list_queues

# List all exchanges
docker exec swiftlogistics-rabbitmq rabbitmqctl list_exchanges

# List all bindings
docker exec swiftlogistics-rabbitmq rabbitmqctl list_bindings

# Purge a queue (delete all messages)
docker exec swiftlogistics-rabbitmq rabbitmqctl purge_queue cms_order_queue

# List consumers
docker exec swiftlogistics-rabbitmq rabbitmqctl list_consumers
```

---

## 10. Technology Stack

### 10.1 Backend Services

| Service                  | Technology                             | Port | Protocol   |
| ------------------------ | -------------------------------------- | ---- | ---------- |
| **API Gateway**          | Express.js, Node.js                    | 3000 | HTTP/REST  |
| **Orchestrator**         | Express.js, Node.js, MongoDB, RabbitMQ | 3001 | HTTP/REST  |
| **Notification Service** | Socket.io, Node.js, RabbitMQ           | 3002 | WebSocket  |
| **CMS Adapter**          | Node.js, SOAP client                   | N/A  | SOAP/XML   |
| **ROS Adapter**          | Node.js, Axios                         | N/A  | REST/JSON  |
| **WMS Adapter**          | Node.js, net module                    | N/A  | TCP Socket |

### 6.2 Mock Services

| Service      | Technology      | Port | Protocol   |
| ------------ | --------------- | ---- | ---------- |
| **CMS Mock** | Python, FastAPI | 4000 | SOAP/XML   |
| **ROS Mock** | Python, FastAPI | 4001 | REST/JSON  |
| **WMS Mock** | Python, FastAPI | 4002 | TCP Socket |

### 6.3 Frontend Applications

| Application           | Technology                        | Port | Platform    |
| --------------------- | --------------------------------- | ---- | ----------- |
| **Web Client Portal** | React 18, TypeScript, Vite, Axios | 5173 | Web Browser |
| **Mobile Driver App** | React Native, Expo, TypeScript    | N/A  | iOS/Android |

### 6.4 Infrastructure

| Component              | Technology             | Port  | Purpose           |
| ---------------------- | ---------------------- | ----- | ----------------- |
| **Database**           | MongoDB                | 27017 | Order persistence |
| **Message Broker**     | RabbitMQ               | 5672  | Event queue       |
| **RabbitMQ UI**        | RabbitMQ Management    | 15672 | Admin interface   |
| **Container Platform** | Docker, Docker Compose | N/A   | Orchestration     |

### 6.5 Key Libraries

**Backend:**

- `express` - Web framework
- `jsonwebtoken` - JWT authentication
- `express-rate-limit` - Rate limiting
- `express-validator` - Input validation
- `mongoose` - MongoDB ODM
- `amqplib` - RabbitMQ client
- `socket.io` - WebSocket server
- `soap` - SOAP client
- `axios` - HTTP client
- `winston` - Logging

**Frontend (Web):**

- `react` - UI library
- `react-router-dom` - Routing
- `axios` - API client
- `socket.io-client` - WebSocket client
- `vite` - Build tool

**Frontend (Mobile):**

- `react-native` - Mobile framework
- `expo` - Development platform
- `expo-location` - GPS tracking
- `expo-camera` - Photo capture
- `axios` - API client

---

## 7. Service Catalog

### 7.1 API Gateway (Port 3000)

**Role:** Single entry point for all external traffic

**Responsibilities:**

- JWT authentication
- Rate limiting (100 req/15min)
- Input validation
- Request routing

**Key Endpoints:**

- `POST /api/orders` → Orchestrator
- `GET /api/orders/:id` → Orchestrator
- `GET /api/driver/*` → Driver endpoints

**Key Files:**

- `index.js` - Express server
- `middleware/auth.js` - JWT validation
- `middleware/rateLimiter.js` - Rate limiting
- `routes/orders.js` - Order routes
- `routes/driver.js` - Driver routes

### 7.2 Orchestrator Service (Port 3001)

**Role:** Transaction manager and order lifecycle coordinator

**Responsibilities:**

- Receive validated orders
- Persist to MongoDB
- Publish to RabbitMQ
- Track integration status
- Update order status

**Key Endpoints:**

- `POST /api/orders` - Create order
- `GET /api/orders/:id` - Get order
- `PUT /api/orders/:id` - Update order
- `GET /api/orders` - List orders

**Key Files:**

- `index.js` - Express server
- `models/Order.js` - MongoDB schema
- `services/messageQueue.js` - RabbitMQ publisher
- `services/orderService.js` - Business logic
- `routes/orders.js` - REST endpoints

### 7.3 Notification Service (Port 3002)

**Role:** Real-time event broadcaster via WebSockets

**Responsibilities:**

- Maintain WebSocket connections
- Listen to RabbitMQ events
- Broadcast real-time notifications
- Enable live tracking

**Event Types:**

- `ORDER_RECEIVED`
- `PROCESSING_UPDATE`
- `DELIVERY_STATUS_CHANGE`

**Key Files:**

- `index.js` - Socket.io server
- `services/socketManager.js` - Connection manager
- `services/eventConsumer.js` - RabbitMQ listener

### 7.4 Integration Adapters

#### CMS Adapter (SOAP/XML)

**Protocol:** SOAP  
**Integrates with:** Legacy Content Management System  
**Port:** 4000 (mock)

**Responsibilities:**

- Subscribe to `new_order_queue`
- Transform JSON → XML
- Send SOAP requests
- Update orchestrator status

#### ROS Adapter (REST/JSON)

**Protocol:** REST  
**Integrates with:** Route Optimization Service  
**Port:** 4001 (mock)

**Responsibilities:**

- Subscribe to `new_order_queue`
- Extract addresses
- Call REST API
- Store route data

#### WMS Adapter (TCP Socket)

**Protocol:** Raw TCP  
**Integrates with:** Warehouse Management System  
**Port:** 4002 (mock)

**Responsibilities:**

- Subscribe to `new_order_queue`
- Open TCP connection
- Send binary packets
- Receive warehouse confirmation

### 7.5 Mock Services

#### CMS Mock (Port 4000)

**28 Endpoints:**

- Orders: 7 endpoints
- Contracts: 7 endpoints
- Billing: 7 endpoints
- Customers: 5 endpoints
- Drivers: 2 endpoints

#### ROS Mock (Port 4001)

**8 Endpoints:**

- Manifests: 8 endpoints
- Route optimization
- Driver assignment

#### WMS Mock (Port 4002)

**9 Endpoints:**

- Packages: 9 endpoints
- Inventory management
- Warehouse operations

**Total: 45+ REST API endpoints**

---

## 8. Frontend Applications

### 8.1 Web Client Portal

**Technology:** React 18 + TypeScript + Vite  
**Port:** 5173  
**Target Users:** E-commerce clients

**Features:**

- 📦 Submit New Orders
- 📊 Track Deliveries
- 📋 Order History
- 💰 Billing & Invoices
- 📜 Contract Management
- 🔐 JWT Authentication
- 🔄 Real-time Updates (WebSocket)

**Key Services:**

- `ApiService` - REST API integration
- `AuthService` - JWT authentication
- `LocationService` - Location tracking
- `WebSocketService` - Real-time notifications

**Project Structure:**

```
web-client-portal/
├── src/
│   ├── components/       # UI components
│   ├── pages/           # Route pages
│   ├── services/        # API integration
│   ├── hooks/           # React hooks
│   ├── types/           # TypeScript types
│   └── App.tsx          # Main app
├── public/
└── package.json
```

### 8.2 Mobile Driver App

**Technology:** React Native + Expo + TypeScript  
**Platform:** iOS & Android  
**Target Users:** Delivery drivers

**Features:**

- 📋 Today's Manifest
- 🗺️ Optimized Route
- 📍 GPS Location Tracking
- ✅ Mark Delivered
- ❌ Report Failure
- 📸 Capture Proof of Delivery
- 🔐 JWT Authentication
- 🔄 Real-time Updates

**Key Services:**

- `ApiService` - REST API integration
- `AuthService` - JWT authentication
- `LocationService` - GPS tracking (Expo Location)
- `CameraService` - Photo capture (Expo Camera)

**Project Structure:**

```
mobile-driver-app/
├── src/
│   ├── components/       # UI components
│   ├── screens/         # Navigation screens
│   ├── services/        # API integration
│   ├── navigation/      # Navigation config
│   ├── types/           # TypeScript types
│   └── App.tsx          # Main app
├── assets/
└── package.json
```

---

## 9. Integration Patterns

### 9.1 Protocol Integration Matrix

| System  | Protocol   | Adapter     | Transform     | Challenge                    |
| ------- | ---------- | ----------- | ------------- | ---------------------------- |
| **CMS** | SOAP/XML   | CMS Adapter | JSON → XML    | Legacy system, no modern API |
| **ROS** | REST/JSON  | ROS Adapter | JSON → JSON   | Third-party API, rate limits |
| **WMS** | TCP Socket | WMS Adapter | JSON → Binary | Proprietary protocol         |

### 9.2 Authentication Flow

```
1. User submits credentials → API Gateway
2. Gateway validates against database
3. Gateway generates JWT token
4. Token returned to client
5. Client includes token in Authorization header
6. Gateway validates token on each request
7. Valid token → Forward to services
8. Invalid token → 401 Unauthorized
```

### 9.3 Real-time Notification Flow

```
1. Client establishes WebSocket connection → Notification Service
2. Client authenticated via JWT
3. Notification Service maintains connection
4. Adapter completes task → Publishes event to RabbitMQ
5. Notification Service consumes event
6. Notification Service broadcasts to connected clients
7. Client receives real-time update
```

---

## 10. Deployment Architecture

### 10.1 Docker Compose Setup

**File:** `docker-compose.yml`

**Services:**

- `api-gateway`
- `orchestrator`
- `notification-service`
- `cms-adapter`
- `ros-adapter`
- `wms-adapter`
- `cms-mock`
- `ros-mock`
- `wms-mock`
- `mongodb`
- `rabbitmq`

### 10.2 Port Mapping

| Service      | Internal Port | External Port | Protocol  |
| ------------ | ------------- | ------------- | --------- |
| API Gateway  | 3000          | 3000          | HTTP      |
| Orchestrator | 3001          | 3001          | HTTP      |
| Notification | 3002          | 3002          | WebSocket |
| CMS Mock     | 4000          | 4000          | SOAP      |
| ROS Mock     | 4001          | 4001          | HTTP      |
| WMS Mock     | 4002          | 4002          | TCP       |
| MongoDB      | 27017         | 27017         | MongoDB   |
| RabbitMQ     | 5672          | 5672          | AMQP      |
| RabbitMQ UI  | 15672         | 15672         | HTTP      |
| Web Portal   | 5173          | 5173          | HTTP      |

### 10.3 Environment Variables

**Backend Services:**

```env
MONGODB_URI=mongodb://mongodb:27017/swiftlogistics
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672
JWT_SECRET=your_secret_key_here
JWT_EXPIRATION=24h
PORT=3000
NODE_ENV=development
```

**Frontend Applications:**

```env
VITE_API_URL=http://localhost:3000
VITE_WS_URL=http://localhost:3002
```

### 10.4 Deployment Commands

```bash
# Start all services
docker-compose up -d

# Start backend only
docker-compose up api-gateway orchestrator notification-service mongodb rabbitmq -d

# Start mock services
docker-compose up cms-mock ros-mock wms-mock -d

# View logs
docker-compose logs -f [service-name]

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up --build -d
```

---

## 11. Security Model

### 11.1 Authentication & Authorization

**JWT Token Authentication:**

- Token generation on login
- Expiration: 24 hours
- Refresh token support
- Role-based access control (planned)

**Token Structure:**

```json
{
  "userId": "user123",
  "role": "client|driver|admin",
  "iat": 1234567890,
  "exp": 1234654290
}
```

### 11.2 API Gateway Security

**Implemented:**

- ✅ JWT validation middleware
- ✅ Rate limiting (100 req/15min)
- ✅ Input validation (express-validator)
- ✅ CORS configuration
- ✅ Helmet security headers

**Planned for Production:**

- ⏳ HTTPS/TLS encryption
- ⏳ API key rotation
- ⏳ OAuth 2.0 integration
- ⏳ Request logging & audit trail
- ⏳ IP whitelisting

### 11.3 Data Security

**MongoDB:**

- Connection string authentication
- Network isolation (Docker network)
- Backup strategy (planned)

**RabbitMQ:**

- Default credentials (development)
- User access control (planned)
- Message encryption (planned)

### 11.4 Mock Services Security

⚠️ **Important:** Mock services are for **development/testing only**

**Current Status:**

- ❌ No authentication
- ❌ No authorization
- ❌ No encryption at rest
- ❌ CORS allows all origins

---

## 12. Performance & Scalability

### 12.1 Performance Metrics

| Service      | Response Time | Throughput |
| ------------ | ------------- | ---------- |
| API Gateway  | < 50ms        | 1000 req/s |
| Orchestrator | < 100ms       | 800 req/s  |
| CMS Mock     | < 50ms        | 1000 req/s |
| ROS Mock     | < 40ms        | 1200 req/s |
| WMS Mock     | < 30ms        | 1500 req/s |

### 12.2 Scalability Features

**Horizontal Scaling:**

- Stateless services
- Load balancer ready
- Multiple adapter instances
- Message queue buffering

**Database Scaling:**

- MongoDB replica sets (planned)
- Sharding strategy (planned)
- Index optimization

**Message Queue:**

- Durable queues
- Message persistence
- Queue prefetch limits
- Consumer acknowledgments

### 12.3 Capacity Planning

| Metric             | Current | Target (Production) |
| ------------------ | ------- | ------------------- |
| Concurrent users   | 100+    | 10,000+             |
| Orders/second      | 10      | 100+                |
| Database size      | < 1GB   | 100GB+              |
| Message throughput | 1000/s  | 10,000/s            |

### 12.4 Monitoring & Observability

**Logging:**

- Winston structured logging
- Log levels: error, warn, info, debug
- Centralized log aggregation (planned)

**Metrics (Planned):**

- Prometheus metrics collection
- Grafana dashboards
- Service health endpoints
- Performance monitoring

---

## 📚 Additional Documentation

For more detailed information, refer to:

- **[ARCHITECTURE.md](doc/ARCHITECTURE.md)** - Service-level architecture
- **[DIAGRAMS.md](doc/DIAGRAMS.md)** - Visual diagrams
- **[SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)** - Business context
- **[SERVICES_INDEX.md](doc/SERVICES_INDEX.md)** - API reference
- **[FRONTEND_QUICKSTART.md](FRONTEND_QUICKSTART.md)** - Frontend setup
- **[DOCKER.md](doc/DOCKER.md)** - Deployment guide

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+
- MongoDB
- RabbitMQ

### Start Backend Services

```bash
# Start infrastructure
docker-compose up mongodb rabbitmq -d

# Start all services
docker-compose up -d

# Verify services
curl http://localhost:3000/health
```

### Start Frontend Applications

```bash
# Web Portal
cd frontend/web-client-portal
npm install
npm run dev

# Mobile App
cd frontend/mobile-driver-app
npm install
npx expo start
```

---

**Document Version:** 2.0.0  
**Last Updated:** February 4, 2026  
**Maintained By:** SwiftLogistics Development Team
