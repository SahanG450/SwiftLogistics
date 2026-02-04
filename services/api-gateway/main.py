"""API Gateway - Main application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
