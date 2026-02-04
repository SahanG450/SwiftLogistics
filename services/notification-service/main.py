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
            import asyncio
            event = json.loads(body)
            logger.info(f"Received event: {event.get('type')}")
            
            # Broadcast to all connected clients
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
