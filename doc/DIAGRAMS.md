# SwiftLogistics - System Architecture Diagrams

## 1. High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           CLIENT (Browser)                           │
│                     SwiftTrack Web Portal / Driver App               │
└────────────────────┬────────────────────────────▲───────────────────┘
                     │ HTTP/HTTPS                 │ WebSocket
                     │ (JSON)                     │ (Real-time)
                     ▼                            │
┌─────────────────────────────────────────────────┴───────────────────┐
│                        API GATEWAY (Port 3000)                       │
│  ┌──────────────┐  ┌───────────────┐  ┌────────────────────┐       │
│  │ JWT Auth     │  │ Rate Limiter  │  │ Input Validation   │       │
│  │ Middleware   │  │ (100/15min)   │  │ (express-validator)│       │
│  └──────────────┘  └───────────────┘  └────────────────────┘       │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ REST API
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR (Port 3001)                          │
│  ┌────────────────────────────────────────────────────────┐         │
│  │               Order Lifecycle Management                │         │
│  │  • Receive → Persist → Queue → Track → Update          │         │
│  └────────────────────────────────────────────────────────┘         │
└───────┬────────────────────────┬────────────────────────────────────┘
        │                        │
        │ Store/Retrieve         │ Publish
        ▼                        ▼
   ┌─────────┐          ┌─────────────────┐
   │ MongoDB │          │   RABBITMQ      │
   │         │          │ Message Broker  │
   │ Orders  │          │   (Port 5672)   │
   └─────────┘          └────┬───┬───┬────┘
                             │   │   │
              ┌──────────────┘   │   └──────────────┐
              │                  │                   │
              ▼                  ▼                   ▼
     ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
     │  CMS ADAPTER   │ │  ROS ADAPTER   │ │  WMS ADAPTER   │
     │                │ │                │ │                │
     │ SOAP/XML       │ │ REST/JSON      │ │ TCP Socket     │
     │ Translator     │ │ Client         │ │ Client         │
     └────────┬───────┘ └────────┬───────┘ └────────┬───────┘
              │                  │                   │
              ▼                  ▼                   ▼
     ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
     │   CMS MOCK     │ │   ROS MOCK     │ │   WMS MOCK     │
     │ (Port 4000)    │ │ (Port 4001)    │ │ (Port 4002)    │
     │                │ │                │ │                │
     │ SOAP Server    │ │ REST API       │ │ TCP Server     │
     │ Legacy System  │ │ Route Optimize │ │ Warehouse Mgmt │
     └────────────────┘ └────────────────┘ └────────────────┘

              Events Flow Back ──────────────┐
                                             │
                                             ▼
                                  ┌────────────────────────┐
                                  │ NOTIFICATION SERVICE   │
                                  │    (Port 3002)        │
                                  │                        │
                                  │  Socket.io WebSocket   │
                                  │  Real-time Broadcaster │
                                  └───────────┬────────────┘
                                              │
                                              │ WebSocket Push
                                              ▼
                                          (Back to Client)
```

---

## 2. Order Submission Flow (Sequence)

```
Client    Gateway   Orchestrator  MongoDB  RabbitMQ   Adapters    Notification  Client
  │         │           │            │         │          │            │          │
  │─POST────▶│           │            │         │          │            │          │
  │ /orders │           │            │         │          │            │          │
  │         │           │            │         │          │            │          │
  │         │──Validate─│            │         │          │            │          │
  │         │   JWT     │            │         │          │            │          │
  │         │           │            │         │          │            │          │
  │         │──Forward──▶│            │         │          │            │          │
  │         │           │            │         │          │            │          │
  │         │           │──Save──────▶│         │          │            │          │
  │         │           │  (RECEIVED) │         │          │            │          │
  │         │           │◀───OK───────│         │          │            │          │
  │         │           │            │         │          │            │          │
  │         │           │──Publish────────────▶│          │            │          │
  │         │           │   order              │          │            │          │
  │         │           │            │         │          │            │          │
  │◀─202────│◀──202─────│            │         │          │            │          │
  │Accepted │  Accepted │            │         │          │            │          │
  │         │           │            │         │          │            │          │
  │         │           │            │     ┌───┴───┐      │            │          │
  │         │           │            │     │Fanout │      │            │          │
  │         │           │            │     └┬──┬──┬┘      │            │          │
  │         │           │            │      │  │  │       │            │          │
  │         │           │            │      │  │  └───────▶ WMS        │          │
  │         │           │            │      │  │          │ Adapter    │          │
  │         │           │            │      │  └──────────▶ ROS        │          │
  │         │           │            │      │             │ Adapter    │          │
  │         │           │            │      └─────────────▶ CMS        │          │
  │         │           │            │                    │ Adapter    │          │
  │         │           │            │                    │            │          │
  │         │           │            │          ┌─────────┴────┐       │          │
  │         │           │            │          │ PARALLEL     │       │          │
  │         │           │            │          │ PROCESSING   │       │          │
  │         │           │            │          └─────────┬────┘       │          │
  │         │           │            │                    │            │          │
  │         │           │◀─Update────────────────────────│            │          │
  │         │           │  Status                        │            │          │
  │         │           │            │                    │            │          │
  │         │           │            │     ┌──Event───────│            │          │
  │         │           │            │     │              │            │          │
  │         │           │            │     ▼              │            │          │
  │         │           │            │  RabbitMQ──────────────────────▶│          │
  │         │           │            │  (events)                       │          │
  │         │           │            │                                 │          │
  │         │           │            │                                 │──Push────▶│
  │         │           │            │                                 │WebSocket │
  │◀────────────────────────────────────────────────────────────────────Real-time─│
  │                                                                     Update     │
```

---

## 3. Technology Stack Mapping

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                            │
│  React.js • Socket.io Client • Axios • WebSocket                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API LAYER                                   │
│  Express.js • JWT • express-rate-limit • express-validator      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                           │
│  Node.js • Event Loop • Async/Await • Custom Services           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  INTEGRATION LAYER                               │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │  SOAP    │    │  REST    │    │   TCP    │                  │
│  │ (soap)   │    │ (axios)  │    │  (net)   │                  │
│  └──────────┘    └──────────┘    └──────────┘                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MESSAGE BROKER LAYER                           │
│              RabbitMQ • amqplib • Pub/Sub                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DATA LAYER                                   │
│              MongoDB • Mongoose • NoSQL                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  REAL-TIME LAYER                                 │
│              Socket.io • WebSocket • Event Broadcasting          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Message Queue Pattern

```
                    ┌─────────────────────────┐
                    │      ORCHESTRATOR       │
                    │   (Order Received)      │
                    └───────────┬─────────────┘
                                │
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
        │           │   │           │   │           │
        │ Consumer  │   │ Consumer  │   │ Consumer  │
        └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
              │               │               │
              └───────────────┼───────────────┘
                              │
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
                                │
                                │ Broadcast
                                ▼
                            WebSocket
                            Clients
```

---

## 5. Adapter Pattern Implementation

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

---

## Legend

```
───▶  Synchronous HTTP Request (blocking)
- -▶  Asynchronous Message Queue (non-blocking)
~~~▶  WebSocket Real-time Push
═══▶  Database Operation
```

---

## Port Summary

| Service | Port | Protocol | Purpose |
|---------|------|----------|---------|
| API Gateway | 3000 | HTTP/REST | Client entry point |
| Orchestrator | 3001 | HTTP/REST | Transaction mgmt |
| Notification | 3002 | WebSocket | Real-time updates |
| CMS Mock | 4000 | SOAP/XML | Legacy system sim |
| ROS Mock | 4001 | REST/JSON | Route service sim |
| WMS Mock | 4002 | TCP | Warehouse sim |
| MongoDB | 27017 | MongoDB | Database |
| RabbitMQ | 5672 | AMQP | Message broker |
| RabbitMQ UI | 15672 | HTTP | Admin interface |
