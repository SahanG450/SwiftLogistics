"""RabbitMQ messaging utilities using pika."""

import pika
import json
import os
from typing import Callable, Optional
from loguru import logger


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
