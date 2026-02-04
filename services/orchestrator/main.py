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
