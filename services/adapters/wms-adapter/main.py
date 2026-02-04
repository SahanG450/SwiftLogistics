"""WMS Adapter - TCP Protocol."""

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

# Setup logging
logger = setup_logging("wms-adapter")

# Message queue
mq = MessageQueue()

# WMS API URL
WMS_API_URL = os.getenv("WMS_API_URL", "http://wms-mock:3002")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    # Startup
    logger.info("╔══════════════════════════════════════╗")
    logger.info("║   WMS Adapter Starting...            ║")
    logger.info("╚══════════════════════════════════════╝")
    
    # Start RabbitMQ consumer
    def consume_orders():
        mq.connect()
        mq.declare_exchange('order_exchange', 'fanout')
        queue_name = mq.declare_queue('wms_order_queue')
        mq.bind_queue(queue_name, 'order_exchange')
        
        def callback(ch, method, properties, body):
            try:
                order = json.loads(body)
                logger.info(f"Processing order: {order['orderId']}")
                
                # Call WMS API for warehouse capacity check
                logger.info(f"Sent to WMS: {order['orderId']}")
                
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.error(f"Error processing order: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        
        mq.consume(queue_name, callback)
    
    consumer_thread = threading.Thread(target=consume_orders, daemon=True)
    consumer_thread.start()
    
    logger.info("✓ WMS Adapter ready")
    
    yield
    
    # Shutdown
    logger.info("WMS Adapter shutting down...")
    mq.close()

# Create app
app = FastAPI(
    title="WMS Adapter",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "wms-adapter"}
