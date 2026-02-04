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
