"""ROS Adapter - REST Protocol."""

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
logger = setup_logging("ros-adapter")

# Message queue
mq = MessageQueue()

# ROS API URL
ROS_API_URL = os.getenv("ROS_API_URL", "http://ros-mock:3003")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    # Startup
    logger.info("╔══════════════════════════════════════╗")
    logger.info("║   ROS Adapter Starting...            ║")
    logger.info("╚══════════════════════════════════════╝")
    
    # Start RabbitMQ consumer
    def consume_orders():
        mq.connect()
        mq.declare_exchange('order_exchange', 'fanout')
        queue_name = mq.declare_queue('ros_order_queue')
        mq.bind_queue(queue_name, 'order_exchange')
        
        def callback(ch, method, properties, body):
            try:
                order = json.loads(body)
                logger.info(f"Processing order: {order['orderId']}")
                
                # Call ROS REST API for route optimization
                logger.info(f"Sent to ROS: {order['orderId']}")
                
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.error(f"Error processing order: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        
        mq.consume(queue_name, callback)
    
    consumer_thread = threading.Thread(target=consume_orders, daemon=True)
    consumer_thread.start()
    
    logger.info("✓ ROS Adapter ready")
    
    yield
    
    # Shutdown
    logger.info("ROS Adapter shutting down...")
    mq.close()

# Create app
app = FastAPI(
    title="ROS Adapter",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "ros-adapter"}
