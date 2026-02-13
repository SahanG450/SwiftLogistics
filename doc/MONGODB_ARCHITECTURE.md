# MongoDB Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     SwiftLogistics System                            │
│                     (Python Services)                                │
└─────────────────────────────────────────────────────────────────────┘

                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
        ┌──────────────────┐         ┌──────────────────┐
        │  FastAPI Service │         │  FastAPI Service │
        │   (CMS Mock)     │         │   (ROS Mock)     │
        └──────────────────┘         └──────────────────┘
                    │                           │
                    │ import                    │ import
                    ▼                           ▼
        ┌────────────────────────────────────────────────┐
        │         shared/database/                       │
        │  ┌──────────────────────────────────────────┐ │
        │  │  mongodb.py (MongoDBClient)              │ │
        │  │  - Singleton connection manager          │ │
        │  │  - Connection pooling                    │ │
        │  │  - Automatic indexing                    │ │
        │  └──────────────────────────────────────────┘ │
        │                                                │
        │  ┌──────────────────────────────────────────┐ │
        │  │  base_repository.py                      │ │
        │  │  - Generic CRUD operations               │ │
        │  │  - Pagination & sorting                  │ │
        │  │  - Aggregation support                   │ │
        │  └──────────────────────────────────────────┘ │
        │                                                │
        │  ┌──────────────────────────────────────────┐ │
        │  │  repositories.py                         │ │
        │  │  ├─ OrderRepository                      │ │
        │  │  ├─ DriverRepository                     │ │
        │  │  ├─ ClientRepository                     │ │
        │  │  ├─ ShipmentRepository                   │ │
        │  │  ├─ ContractRepository                   │ │
        │  │  ├─ InvoiceRepository                    │ │
        │  │  └─ AdminRepository                      │ │
        │  └──────────────────────────────────────────┘ │
        └────────────────────────────────────────────────┘
                                  │
                                  │ Motor Driver (Async)
                                  ▼
                    ┌──────────────────────────┐
                    │   MongoDB 7.0            │
                    │   (Docker Container)     │
                    │                          │
                    │   Port: 27017            │
                    │   Database: swiftlogistics │
                    │                          │
                    │   Collections:           │
                    │   ├─ orders              │
                    │   ├─ drivers             │
                    │   ├─ clients             │
                    │   ├─ shipments           │
                    │   ├─ contracts           │
                    │   ├─ invoices            │
                    │   └─ admins              │
                    └──────────────────────────┘
                                  │
                                  │ Persistent Storage
                                  ▼
                    ┌──────────────────────────┐
                    │   Docker Volume          │
                    │   swiftlogistics-        │
                    │   mongodb-data           │
                    └──────────────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                        Data Flow Example                             │
└─────────────────────────────────────────────────────────────────────┘

1. CREATE ORDER
   ┌─────────┐                                      ┌──────────┐
   │ FastAPI │  await order_repo.create({...})     │  Motor   │
   │ Service │ ──────────────────────────────────> │  Driver  │
   └─────────┘                                      └──────────┘
                                                         │
                                                         ▼
                                                   ┌──────────┐
                                                   │ MongoDB  │
                                                   │  orders  │
                                                   └──────────┘

2. QUERY ORDERS
   ┌─────────┐                                      ┌──────────┐
   │ FastAPI │  await order_repo.find_many(...)    │  Motor   │
   │ Service │ ──────────────────────────────────> │  Driver  │
   └─────────┘                                      └──────────┘
                                                         │
                                                         ▼
                                                   ┌──────────┐
                                                   │ MongoDB  │
                  ┌──────────────────────────────  │  orders  │
                  │ [order1, order2, ...]          └──────────┘
                  ▼
             Return Results

3. UPDATE STATUS
   ┌─────────┐                                      ┌──────────┐
   │ FastAPI │  await order_repo.update_status(...) │  Motor   │
   │ Service │ ──────────────────────────────────> │  Driver  │
   └─────────┘                                      └──────────┘
                                                         │
                                                         ▼
                                                   ┌──────────┐
                                                   │ MongoDB  │
                                                   │  Update  │
                                                   └──────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                     Repository Pattern                               │
└─────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│  Your FastAPI Service                                          │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  @app.get("/orders")                                     │ │
│  │  async def get_orders():                                 │ │
│  │      db = await get_database()                           │ │
│  │      order_repo = OrderRepository(db)  ◄── Repository    │ │
│  │      orders = await order_repo.find_many()               │ │
│  │      return {"orders": orders}                           │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                              │
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  OrderRepository (extends BaseRepository)                      │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Custom Methods:                                         │ │
│  │  - find_by_order_id(order_id)                           │ │
│  │  - find_by_client(client_id)                            │ │
│  │  - find_by_status(status)                               │ │
│  │  - update_status(order_id, status)                      │ │
│  │                                                           │ │
│  │  Inherited Methods (from BaseRepository):               │ │
│  │  - create(document)                                      │ │
│  │  - find_by_id(id)                                        │ │
│  │  - find_one(query)                                       │ │
│  │  - find_many(query, skip, limit, sort)                  │ │
│  │  - update_by_id(id, data)                                │ │
│  │  - update_one(query, data)                               │ │
│  │  - update_many(query, data)                              │ │
│  │  - delete_by_id(id)                                      │ │
│  │  - delete_one(query)                                     │ │
│  │  - delete_many(query)                                    │ │
│  │  - count(query)                                          │ │
│  │  - exists(query)                                         │ │
│  │  - aggregate(pipeline)                                   │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                              │
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  MongoDB Collection: orders                                    │
│  {                                                             │
│    "_id": ObjectId("..."),                                     │
│    "order_id": "ORD-001",                                      │
│    "client_id": "CLI-123",                                     │
│    "status": "pending",                                        │
│    "pickup_address": "123 Main St",                            │
│    "delivery_address": "456 Oak Ave",                          │
│    "items": [...],                                             │
│    "total_amount": 125.00,                                     │
│    "created_at": "2026-02-13T22:00:00",                        │
│    "updated_at": "2026-02-13T22:00:00"                         │
│  }                                                             │
└────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                     Connection Management                            │
└─────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│  MongoDBClient (Singleton)                                     │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Class Attributes:                                       │ │
│  │  _client: AsyncIOMotorClient (shared)                   │ │
│  │  _database: AsyncIOMotorDatabase (shared)               │ │
│  │                                                           │ │
│  │  Methods:                                                │ │
│  │  - connect() -> Create single connection                │ │
│  │  - get_database() -> Retrun existing database           │ │
│  │  - close() -> Close connection                          │ │
│  │  - _create_indexes() -> Setup indexes                   │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
           │
           │ Maintains single connection
           ▼
┌────────────────────────────────────────────────────────────────┐
│  AsyncIOMotorClient                                            │
│  - Connection Pool: min=10, max=50                             │
│  - Timeout: 5000ms                                             │
│  - Auto-reconnect: enabled                                     │
└────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                         Indexes                                      │
└─────────────────────────────────────────────────────────────────────┘

orders collection:
  - order_id (unique)
  - client_id
  - status
  - created_at

drivers collection:
  - driver_id (unique)
  - email (unique)
  - status

clients collection:
  - client_id (unique)
  - email (unique)

shipments collection:
  - shipment_id (unique)
  - order_id
  - driver_id
  - status

contracts collection:
  - contract_id (unique)
  - client_id

invoices collection:
  - invoice_id (unique)
  - order_id
  - client_id
```

## Key Design Decisions

### 1. Singleton Pattern

- **Why**: Prevents multiple MongoDB connections
- **Benefit**: Resource efficient, connection pooling

### 2. Repository Pattern

- **Why**: Abstracts database operations
- **Benefit**: Clean, testable, maintainable code

### 3. Async/Await (Motor)

- **Why**: Non-blocking I/O for FastAPI
- **Benefit**: Better performance, handles concurrent requests

### 4. Automatic Timestamps

- **Why**: Track document creation/updates
- **Benefit**: Audit trail, debugging

### 5. Automatic Indexing

- **Why**: Optimize common queries
- **Benefit**: Fast lookups, better performance

## Benefits

✅ **Clean Architecture**: Repository pattern separates concerns  
✅ **Reusable**: Same utilities across all services  
✅ **Type-Safe**: Pydantic models for validation  
✅ **Testable**: Easy to mock repositories  
✅ **Scalable**: Connection pooling, indexes  
✅ **Maintainable**: Centralized database logic
