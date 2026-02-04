# Python Implementation Guide for SwiftLogistics

Complete implementation guide for converting SwiftLogistics backend from Node.js to Python using FastAPI.

---

## Table of Contents

1. [Common Utilities](#1-common-utilities)
2. [API Gateway Service](#2-api-gateway-service)
3. [Orchestrator Service](#3-orchestrator-service)
4. [Notification Service](#4-notification-service)
5. [Adapter Services](#5-adapter-services)
6. [Docker Configuration](#6-docker-configuration)
7. [Running the System](#7-running-the-system)

---

## 1. Common Utilities

Create shared utilities that all services will use.

### Directory Structure

```
services/common/
├── __init__.py
├── database.py
├── messaging.py
├── auth.py
├── logging_config.py
└── models.py
```

### `services/common/__init__.py`

```python
"""Common utilities for SwiftLogistics services."""

__version__ = "1.0.0"
```

### `services/common/database.py`

```python
"""MongoDB database utilities using Motor (async driver) and Beanie ODM."""

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import Optional
import os
from loguru import logger


class Database:
    """MongoDB database manager."""

    client: Optional[AsyncIOMotorClient] = None

    @classmethod
    async def connect_db(cls, document_models: list):
        """
        Connect to MongoDB and initialize Beanie ODM.

        Args:
            document_models: List of Beanie Document classes to initialize
        """
        try:
            mongodb_uri = os.getenv("MONGODB_URI", "mongodb://admin:admin123@mongodb:27017/swiftlogistics?authSource=admin")

            logger.info(f"Connecting to MongoDB...")
            cls.client = AsyncIOMotorClient(mongodb_uri)

            # Get database name from URI or use default
            database_name = "swiftlogistics"

            # Initialize Beanie with document models
            await init_beanie(
                database=cls.client[database_name],
                document_models=document_models
            )

            logger.info("✓ MongoDB connected successfully")

        except Exception as e:
            logger.error(f"✗ Failed to connect to MongoDB: {e}")
            raise

    @classmethod
    async def close_db(cls):
        """Close database connection."""
        if cls.client:
            cls.client.close()
            logger.info("MongoDB connection closed")


async def get_database():
    """Dependency for getting database instance."""
    return Database.client
```

### `services/common/messaging.py`

```python
"""RabbitMQ messaging utilities using pika."""

import pika
import json
import os
from typing import Callable, Optional
from loguru import logger
import asyncio
from functools import partial


class MessageQueue:
    """RabbitMQ message queue manager."""

    def __init__(self):
        self.connection: Optional[pika.BlockingConnection] = None
        self.channel: Optional[pika.channel.Channel] = None
        self.rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://admin:admin123@rabbitmq:5672")

    def connect(self):
        """Connect to RabbitMQ."""
        try:
            logger.info("Connecting to RabbitMQ...")

            # Parse connection URL
            params = pika.URLParameters(self.rabbitmq_url)
            params.heartbeat = 600
            params.blocked_connection_timeout = 300

            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()

            logger.info("✓ RabbitMQ connected successfully")

        except Exception as e:
            logger.error(f"✗ Failed to connect to RabbitMQ: {e}")
            raise

    def declare_exchange(self, exchange_name: str, exchange_type: str = 'fanout'):
        """
        Declare an exchange.

        Args:
            exchange_name: Name of the exchange
            exchange_type: Type of exchange (fanout, topic, direct)
        """
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")

        self.channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=exchange_type,
            durable=True
        )
        logger.info(f"Exchange declared: {exchange_name} ({exchange_type})")

    def declare_queue(self, queue_name: str) -> str:
        """
        Declare a queue.

        Args:
            queue_name: Name of the queue

        Returns:
            Queue name
        """
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")

        result = self.channel.queue_declare(
            queue=queue_name,
            durable=True,
            exclusive=False,
            auto_delete=False
        )
        logger.info(f"Queue declared: {queue_name}")
        return result.method.queue

    def bind_queue(self, queue_name: str, exchange_name: str, routing_key: str = ''):
        """
        Bind a queue to an exchange.

        Args:
            queue_name: Queue to bind
            exchange_name: Exchange to bind to
            routing_key: Routing key (empty for fanout)
        """
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")

        self.channel.queue_bind(
            queue=queue_name,
            exchange=exchange_name,
            routing_key=routing_key
        )
        logger.info(f"Queue bound: {queue_name} -> {exchange_name}")

    def publish(self, exchange_name: str, message: dict, routing_key: str = ''):
        """
        Publish a message to an exchange.

        Args:
            exchange_name: Exchange to publish to
            message: Message dictionary to publish
            routing_key: Routing key (empty for fanout)
        """
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")

        self.channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
                content_type='application/json'
            )
        )
        logger.debug(f"Message published to {exchange_name}")

    def consume(self, queue_name: str, callback: Callable, prefetch_count: int = 1):
        """
        Start consuming messages from a queue.

        Args:
            queue_name: Queue to consume from
            callback: Callback function to handle messages
            prefetch_count: Number of messages to prefetch
        """
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")

        self.channel.basic_qos(prefetch_count=prefetch_count)
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=False
        )

        logger.info(f"Started consuming from queue: {queue_name}")
        self.channel.start_consuming()

    def close(self):
        """Close RabbitMQ connection."""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("RabbitMQ connection closed")
```

### `services/common/auth.py`

```python
"""JWT authentication utilities."""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT token.

    Args:
        token: JWT token to decode

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    FastAPI dependency to get current authenticated user.

    Args:
        credentials: HTTP Bearer credentials

    Returns:
        User data from token
    """
    token = credentials.credentials
    payload = decode_access_token(token)

    user_id = payload.get("userId")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    return payload
```

### `services/common/logging_config.py`

```python
"""Logging configuration using loguru."""

from loguru import logger
import sys
import os


def setup_logging(service_name: str):
    """
    Configure logging for a service.

    Args:
        service_name: Name of the service for log identification
    """
    # Remove default handler
    logger.remove()

    # Get log level from environment
    log_level = os.getenv("LOG_LEVEL", "INFO")

    # Add console handler with custom format
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{extra[service]}</cyan> | <level>{message}</level>",
        level=log_level,
        colorize=True
    )

    # Add file handler for errors
    logger.add(
        f"logs/{service_name}_errors.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[service]} | {message}",
        level="ERROR",
        rotation="10 MB",
        retention="7 days"
    )

    # Bind service name to all log messages
    logger.configure(extra={"service": service_name})

    return logger
```

### `services/common/models.py`

```python
"""Shared Pydantic models for request/response schemas."""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime


class LocationSchema(BaseModel):
    """Geographic location."""
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lng: float = Field(..., ge=-180, le=180, description="Longitude")
    address: Optional[str] = Field(None, description="Address string")


class PackageDetailsSchema(BaseModel):
    """Package information."""
    weight: float = Field(..., gt=0, description="Weight in kg")
    description: Optional[str] = Field(None, description="Package description")
    dimensions: Optional[Dict[str, float]] = Field(None, description="Dimensions (length, width, height)")
    fragile: bool = Field(False, description="Is package fragile")


class OrderCreateRequest(BaseModel):
    """Request schema for creating an order."""
    pickupLocation: LocationSchema
    deliveryAddress: LocationSchema
    packageDetails: PackageDetailsSchema
    scheduledPickupTime: Optional[datetime] = None
    specialInstructions: Optional[str] = None


class OrderResponse(BaseModel):
    """Response schema for order."""
    orderId: str
    status: str
    message: Optional[str] = None
    customerId: Optional[str] = None
    createdAt: Optional[datetime] = None


class UserLoginRequest(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class UserRegisterRequest(BaseModel):
    """User registration request."""
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: Optional[str] = None
    company: Optional[str] = None


class TokenResponse(BaseModel):
    """Authentication token response."""
    token: str
    user: Dict[str, Any]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    service: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

---

## 2. API Gateway Service

The API Gateway is the entry point for all client requests.

### Directory Structure

```
services/api-gateway/
├── Dockerfile
├── requirements.txt
├── main.py
├── middleware/
│   ├── __init__.py
│   └── security.py
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── orders.py
│   ├── driver.py
│   └── health.py
└── services/
    ├── __init__.py
    └── orchestrator_client.py
```

### `services/api-gateway/requirements.txt`

```text
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
slowapi==0.1.9
httpx==0.26.0
python-dotenv==1.0.0
loguru==0.7.2
pydantic[email]==2.5.0
```

### `services/api-gateway/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy common utilities
COPY ../common /app/common

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p /app/logs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
```

### `services/api-gateway/main.py`

```python
"""API Gateway - Main application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
import sys

# Add common to path
sys.path.append('/app')
from common.logging_config import setup_logging

# Import routes
from routes import auth, orders, driver, health
from middleware.security import add_security_headers

# Setup logging
logger = setup_logging("api-gateway")

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI(
    title="SwiftLogistics API Gateway",
    version="1.0.0",
    description="API Gateway for SwiftLogistics middleware system"
)

# Rate limit exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        os.getenv("WEB_CLIENT_URL", "http://localhost:5173")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers middleware
app.middleware("http")(add_security_headers)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
app.include_router(driver.router, prefix="/api/driver", tags=["Driver"])

@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("╔══════════════════════════════════════╗")
    logger.info("║   API Gateway Starting...            ║")
    logger.info("╚══════════════════════════════════════╝")
    logger.info(f"Environment: {os.getenv('NODE_ENV', 'development')}")
    logger.info(f"Port: 3000")

@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("API Gateway shutting down...")
```

### `services/api-gateway/middleware/security.py`

```python
"""Security middleware for adding security headers."""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)

    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    # Remove server header
    if "server" in response.headers:
        del response.headers["server"]

    return response
```

### `services/api-gateway/routes/health.py`

```python
"""Health check endpoint."""

from fastapi import APIRouter
from datetime import datetime
import sys

sys.path.append('/app')
from common.models import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="api-gateway",
        timestamp=datetime.utcnow()
    )
```

### `services/api-gateway/routes/auth.py`

```python
"""Authentication routes."""

from fastapi import APIRouter, HTTPException, status
from slowapi import Limiter
from slowapi.util import get_remote_address
import httpx
import os
import sys

sys.path.append('/app')
from common.models import UserLoginRequest, UserRegisterRequest, TokenResponse
from common.auth import create_access_token
from loguru import logger

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

CMS_MOCK_URL = os.getenv("CMS_API_URL", "http://cms-mock:3001")

@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(request: UserLoginRequest):
    """
    User login endpoint.

    Rate limit: 5 requests per minute per IP
    """
    try:
        # Forward to CMS mock for authentication
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{CMS_MOCK_URL}/api/auth/login",
                data={
                    "username": request.email,
                    "password": request.password
                },
                timeout=10.0
            )

            if response.status_code == 200:
                user_data = response.json()

                # Generate JWT token
                token = create_access_token(
                    data={
                        "userId": user_data["id"],
                        "email": user_data["email"],
                        "role": user_data.get("role", "client")
                    }
                )

                logger.info(f"User logged in: {user_data['email']}")

                return TokenResponse(
                    token=token,
                    user=user_data
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )

    except httpx.TimeoutException:
        logger.error("CMS service timeout")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service unavailable"
        )
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.post("/register", response_model=TokenResponse)
@limiter.limit("3/hour")
async def register(request: UserRegisterRequest):
    """
    User registration endpoint.

    Rate limit: 3 requests per hour per IP
    """
    try:
        # Forward to CMS mock for registration
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{CMS_MOCK_URL}/api/customers",
                json={
                    "name": request.name,
                    "email": request.email,
                    "password": request.password,
                    "phone": request.phone or "",
                    "company": request.company or "",
                    "status": "active",
                    "role": "client"
                },
                timeout=10.0
            )

            if response.status_code == 200:
                user_data = response.json()

                # Generate JWT token
                token = create_access_token(
                    data={
                        "userId": user_data["id"],
                        "email": user_data["email"],
                        "role": user_data.get("role", "client")
                    }
                )

                logger.info(f"New user registered: {user_data['email']}")

                return TokenResponse(
                    token=token,
                    user=user_data
                )
            else:
                error_detail = response.json().get("detail", "Registration failed")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=error_detail
                )

    except httpx.TimeoutException:
        logger.error("CMS service timeout")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Registration service unavailable"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )
```

### `services/api-gateway/routes/orders.py`

```python
"""Order management routes."""

from fastapi import APIRouter, Depends, HTTPException, status
import httpx
import os
import sys

sys.path.append('/app')
from common.models import OrderCreateRequest, OrderResponse
from common.auth import get_current_user
from loguru import logger

router = APIRouter()

ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://orchestrator:3001")

@router.post("", response_model=OrderResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_order(
    order: OrderCreateRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new order.

    Requires authentication.
    """
    try:
        # Add user info to order
        order_data = order.dict()
        order_data["customerId"] = current_user["userId"]

        # Forward to orchestrator
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ORCHESTRATOR_URL}/api/orders",
                json=order_data,
                timeout=30.0
            )

            if response.status_code in [200, 202]:
                result = response.json()
                logger.info(f"Order created: {result['orderId']} by user {current_user['email']}")
                return OrderResponse(**result)
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to create order"
                )

    except httpx.TimeoutException:
        logger.error("Orchestrator service timeout")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Order service temporarily unavailable"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Order creation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order"
        )

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get order details by ID."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{ORCHESTRATOR_URL}/api/orders/{order_id}",
                timeout=10.0
            )

            if response.status_code == 200:
                return OrderResponse(**response.json())
            elif response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to retrieve order"
                )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve order"
        )
```

### `services/api-gateway/routes/driver.py`

```python
"""Driver-related routes."""

from fastapi import APIRouter, Depends
import sys

sys.path.append('/app')
from common.auth import get_current_user

router = APIRouter()

@router.get("/location")
async def get_driver_location(current_user: dict = Depends(get_current_user)):
    """Get driver location (placeholder)."""
    return {
        "driverId": current_user["userId"],
        "location": {"lat": 6.9271, "lng": 79.8612},
        "status": "available"
    }
```

---

## 3. Orchestrator Service

The orchestrator manages order lifecycle and coordinates with adapters.

### Directory Structure

```
services/orchestrator/
├── Dockerfile
├── requirements.txt
├── main.py
├── models/
│   ├── __init__.py
│   ├── order.py
│   └── schemas.py
├── routes/
│   ├── __init__.py
│   ├── orders.py
│   └── health.py
└── services/
    ├── __init__.py
    ├── message_queue.py
    └── order_manager.py
```

### `services/orchestrator/requirements.txt`

```text
fastapi==0.109.0
uvicorn[standard]==0.27.0
motor==3.3.2
beanie==1.24.0
pika==1.3.2
python-dotenv==1.0.0
loguru==0.7.2
httpx==0.26.0
pydantic[email]==2.5.0
```

### `services/orchestrator/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy common utilities
COPY ../common /app/common

# Copy application
COPY . .

# Create logs directory
RUN mkdir -p /app/logs

# Expose port
EXPOSE 3001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:3001/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3001"]
```

### `services/orchestrator/main.py`

```python
"""Orchestrator Service - Main application."""

from fastapi import FastAPI
from contextlib import asynccontextmanager
import sys

sys.path.append('/app')
from common.logging_config import setup_logging
from common.database import Database
from models.order import Order
from routes import orders, health
from services.message_queue import message_queue
from loguru import logger

# Setup logging
logger = setup_logging("orchestrator")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    # Startup
    logger.info("╔══════════════════════════════════════╗")
    logger.info("║   Orchestrator Starting...           ║")
    logger.info("╚══════════════════════════════════════╝")

    # Connect to MongoDB
    await Database.connect_db([Order])

    # Connect to RabbitMQ
    message_queue.connect()
    message_queue.declare_exchange('order_exchange', 'fanout')
    message_queue.declare_exchange('events_exchange', 'fanout')

    logger.info("✓ Orchestrator ready")

    yield

    # Shutdown
    logger.info("Orchestrator shutting down...")
    await Database.close_db()
    message_queue.close()

# Create app
app = FastAPI(
    title="SwiftLogistics Orchestrator",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
```

### `services/orchestrator/models/order.py`

```python
"""Order document model using Beanie ODM."""

from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional, Dict, Any


class Order(Document):
    """Order document stored in MongoDB."""

    orderId: str = Field(..., description="Unique order identifier")
    customerId: str = Field(..., description="Customer ID")

    # Location data
    pickupLocation: Dict[str, Any]
    deliveryAddress: Dict[str, Any]

    # Package information
    packageDetails: Dict[str, Any]

    # Order metadata
    status: str = Field(default="RECEIVED", description="Order status")
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    # Integration status
    integrationStatus: Dict[str, str] = Field(
        default_factory=lambda: {
            "cms": "PENDING",
            "ros": "PENDING",
            "wms": "PENDING"
        }
    )

    # Additional fields
    scheduledPickupTime: Optional[datetime] = None
    specialInstructions: Optional[str] = None

    class Settings:
        name = "orders"
        indexes = [
            "orderId",
            "customerId",
            "status",
            "createdAt"
        ]
```

### `services/orchestrator/routes/orders.py`

```python
"""Order routes."""

from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import sys

sys.path.append('/app')
from common.models import OrderCreateRequest, OrderResponse
from models.order import Order
from services.order_manager import create_order_id
from services.message_queue import message_queue
from loguru import logger

router = APIRouter()

@router.post("", response_model=OrderResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_order(order_request: OrderCreateRequest):
    """Create a new order."""
    try:
        # Generate order ID
        order_id = create_order_id()

        # Create order document
        order = Order(
            orderId=order_id,
            customerId=order_request.dict().get("customerId", "unknown"),
            pickupLocation=order_request.pickupLocation.dict(),
            deliveryAddress=order_request.deliveryAddress.dict(),
            packageDetails=order_request.packageDetails.dict(),
            scheduledPickupTime=order_request.scheduledPickupTime,
            specialInstructions=order_request.specialInstructions,
            status="RECEIVED",
            createdAt=datetime.utcnow()
        )

        # Save to database
        await order.insert()

        logger.info(f"Order created: {order_id}")

        # Publish to RabbitMQ
        message_queue.publish(
            exchange_name='order_exchange',
            message={
                "orderId": order_id,
                "customerId": order.customerId,
                "pickupLocation": order.pickupLocation,
                "deliveryAddress": order.deliveryAddress,
                "packageDetails": order.packageDetails,
                "timestamp": order.createdAt.isoformat()
            }
        )

        logger.info(f"Order published to queue: {order_id}")

        # Publish event
        message_queue.publish(
            exchange_name='events_exchange',
            message={
                "type": "ORDER_CREATED",
                "data": {
                    "orderId": order_id,
                    "status": "RECEIVED",
                    "message": "Order received and being processed"
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        )

        return OrderResponse(
            orderId=order_id,
            status="RECEIVED",
            message="Order received and being processed",
            customerId=order.customerId,
            createdAt=order.createdAt
        )

    except Exception as e:
        logger.error(f"Failed to create order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order"
        )

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    """Get order by ID."""
    order = await Order.find_one(Order.orderId == order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return OrderResponse(
        orderId=order.orderId,
        status=order.status,
        customerId=order.customerId,
        createdAt=order.createdAt
    )
```

### `services/orchestrator/services/message_queue.py`

```python
"""Message queue service instance."""

import sys
sys.path.append('/app')
from common.messaging import MessageQueue

# Create singleton instance
message_queue = MessageQueue()
```

### `services/orchestrator/services/order_manager.py`

```python
"""Order management utilities."""

from datetime import datetime
import random
import string


def create_order_id() -> str:
    """Generate a unique order ID."""
    timestamp = int(datetime.utcnow().timestamp())
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"ORD-{timestamp}-{random_suffix}"
```

---

## 4. Notification Service

Handles real-time notifications via WebSockets.

### `services/notification-service/requirements.txt`

```text
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-socketio==5.11.0
pika==1.3.2
python-dotenv==1.0.0
loguru==0.7.2
```

### `services/notification-service/main.py`

```python
"""Notification Service with WebSocket support."""

from fastapi import FastAPI
import socketio
from contextlib import asynccontextmanager
import threading
import sys
import os

sys.path.append('/app')
from common.logging_config import setup_logging
from common.messaging import MessageQueue
from loguru import logger

# Setup logging
logger = setup_logging("notification-service")

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        os.getenv("WEB_CLIENT_URL", "*")
    ]
)

# Message queue
mq = MessageQueue()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    # Startup
    logger.info("╔══════════════════════════════════════╗")
    logger.info("║   Notification Service Starting...   ║")
    logger.info("╚══════════════════════════════════════╝")

    # Start RabbitMQ consumer in background thread
    def consume_events():
        mq.connect()
        mq.declare_exchange('events_exchange', 'fanout')
        queue_name = mq.declare_queue('notification_events_queue')
        mq.bind_queue(queue_name, 'events_exchange')

        def callback(ch, method, properties, body):
            import json
            event = json.loads(body)
            logger.info(f"Received event: {event.get('type')}")

            # Broadcast to all connected clients (sync version)
            import asyncio
            asyncio.run(sio.emit('order-update', event.get('data', {})))

            ch.basic_ack(delivery_tag=method.delivery_tag)

        mq.consume(queue_name, callback)

    consumer_thread = threading.Thread(target=consume_events, daemon=True)
    consumer_thread.start()

    logger.info("✓ Notification service ready")

    yield

    # Shutdown
    logger.info("Notification service shutting down...")
    mq.close()

# Create FastAPI app
app = FastAPI(
    title="SwiftLogistics Notification Service",
    version="1.0.0",
    lifespan=lifespan
)

# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    """Handle client connection."""
    logger.info(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    """Handle client disconnection."""
    logger.info(f"Client disconnected: {sid}")

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "notification-service"}

# Wrap with Socket.IO
socket_app = socketio.ASGIApp(sio, app)
```

---

## 5. Adapter Services

All three adapters (CMS, ROS, WMS) follow similar patterns.

### CMS Adapter Example

### `services/adapters/cms-adapter/requirements.txt`

```text
fastapi==0.109.0
uvicorn[standard]==0.27.0
pika==1.3.2
zeep==4.2.1
httpx==0.26.0
python-dotenv==1.0.0
loguru==0.7.2
```

### `services/adapters/cms-adapter/main.py`

```python
"""CMS Adapter - SOAP Protocol."""

from fastapi import FastAPI
from contextlib import asynccontextmanager
import threading
import sys
import os
import json

sys.path.append('/app')
from common.logging_config import setup_logging
from common.messaging import MessageQueue
from loguru import logger
from zeep import Client

# Setup logging
logger = setup_logging("cms-adapter")

# Message queue
mq = MessageQueue()

# SOAP client
CMS_SOAP_URL = os.getenv("CMS_API_URL", "http://cms-mock:3001")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    # Startup
    logger.info("╔══════════════════════════════════════╗")
    logger.info("║   CMS Adapter Starting...            ║")
    logger.info("╚══════════════════════════════════════╝")

    # Start RabbitMQ consumer
    def consume_orders():
        mq.connect()
        mq.declare_exchange('order_exchange', 'fanout')
        queue_name = mq.declare_queue('cms_order_queue')
        mq.bind_queue(queue_name, 'order_exchange')

        def callback(ch, method, properties, body):
            try:
                order = json.loads(body)
                logger.info(f"Processing order: {order['orderId']}")

                # Transform and send to CMS (SOAP)
                # In real implementation, use zeep to call SOAP service
                logger.info(f"Sent to CMS: {order['orderId']}")

                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.error(f"Error processing order: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

        mq.consume(queue_name, callback)

    consumer_thread = threading.Thread(target=consume_orders, daemon=True)
    consumer_thread.start()

    logger.info("✓ CMS Adapter ready")

    yield

    # Shutdown
    logger.info("CMS Adapter shutting down...")
    mq.close()

# Create app
app = FastAPI(
    title="CMS Adapter",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "cms-adapter"}
```

---

## 6. Docker Configuration

### Updated `docker-compose.yml`

```yaml
services:
  # Infrastructure (unchanged)
  mongodb:
    image: mongo:7.0
    container_name: swiftlogistics-mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin123
    volumes:
      - mongodb_data:/data/db
    networks:
      - swiftlogistics-network
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 10s
      timeout: 5s
      retries: 5

  rabbitmq:
    image: rabbitmq:3.12-management-alpine
    container_name: swiftlogistics-rabbitmq
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin123
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    networks:
      - swiftlogistics-network
    healthcheck:
      test: rabbitmq-diagnostics -q ping
      interval: 10s
      timeout: 5s
      retries: 5

  # Python Services
  api-gateway:
    build:
      context: ./services
      dockerfile: api-gateway/Dockerfile
    container_name: swiftlogistics-api-gateway
    ports:
      - "3000:3000"
    environment:
      JWT_SECRET: "your-secret-key-change-in-production"
      CMS_API_URL: "http://cms-mock:3001"
      ORCHESTRATOR_URL: "http://orchestrator:3001"
      LOG_LEVEL: "INFO"
    depends_on:
      - orchestrator
      - cms-mock
    networks:
      - swiftlogistics-network

  orchestrator:
    build:
      context: ./services
      dockerfile: orchestrator/Dockerfile
    container_name: swiftlogistics-orchestrator
    ports:
      - "3001:3001"
    environment:
      MONGODB_URI: "mongodb://admin:admin123@mongodb:27017/swiftlogistics?authSource=admin"
      RABBITMQ_URL: "amqp://admin:admin123@rabbitmq:5672"
      LOG_LEVEL: "INFO"
    depends_on:
      mongodb:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    networks:
      - swiftlogistics-network

  notification-service:
    build:
      context: ./services
      dockerfile: notification-service/Dockerfile
    container_name: swiftlogistics-notification
    ports:
      - "3004:3004"
    environment:
      RABBITMQ_URL: "amqp://admin:admin123@rabbitmq:5672"
      LOG_LEVEL: "INFO"
    depends_on:
      rabbitmq:
        condition: service_healthy
    networks:
      - swiftlogistics-network

  # Mock services (unchanged - already Python)
  # ... rest of mock services ...

networks:
  swiftlogistics-network:
    driver: bridge

volumes:
  mongodb_data:
  rabbitmq_data:
```

---

## 7. Running the System

### Build and Start

```bash
# Navigate to project directory
cd /home/snake/UCSC/UCSC/Year\ 2/sem\ 2/Middleware\ Architecture\ SCS2314/Assignment\ 4/SwiftLogistics

# Build all services
docker-compose build

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api-gateway orchestrator notification-service
```

### Testing

```bash
# Health checks
curl http://localhost:3000/health
curl http://localhost:3001/health

# Register user
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123"
  }'

# Login
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'

# Create order (use token from login)
curl -X POST http://localhost:3000/api/orders \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "pickupLocation": {
      "lat": 6.9271,
      "lng": 79.8612,
      "address": "Colombo Fort"
    },
    "deliveryAddress": {
      "lat": 6.9344,
      "lng": 79.8428,
      "address": "Pettah"
    },
    "packageDetails": {
      "weight": 5,
      "description": "Test package"
    }
  }'
```

---

## Next Steps

1. **Implement remaining adapters** (ROS, WMS) following CMS adapter pattern
2. **Add comprehensive error handling** and retry logic
3. **Implement monitoring** with Prometheus/Grafana
4. **Add automated tests** using pytest
5. **Update documentation** with Python examples

This completes the Python implementation guide for SwiftLogistics!
