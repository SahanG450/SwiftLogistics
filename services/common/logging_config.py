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
