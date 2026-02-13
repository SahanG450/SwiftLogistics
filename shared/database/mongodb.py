"""
MongoDB connection management for SwiftLogistics

This module provides a singleton MongoDB client that manages database connections
across the application lifecycle.
"""
import logging
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import os

logger = logging.getLogger(__name__)


class MongoDBClient:
    """
    Singleton MongoDB client for managing database connections.
    
    This class ensures only one MongoDB connection is created and reused
    throughout the application lifecycle.
    """
    
    _client: Optional[AsyncIOMotorClient] = None
    _database: Optional[AsyncIOMotorDatabase] = None
    _database_name: str = "swiftlogistics"
    
    @classmethod
    async def connect(cls, mongodb_uri: Optional[str] = None) -> AsyncIOMotorDatabase:
        """
        Establish connection to MongoDB.
        
        Args:
            mongodb_uri: MongoDB connection string. If not provided, reads from environment.
            
        Returns:
            AsyncIOMotorDatabase: Connected database instance
            
        Raises:
            ConnectionFailure: If connection to MongoDB fails
        """
        if cls._client is not None and cls._database is not None:
            logger.info("Reusing existing MongoDB connection")
            return cls._database
        
        # Get MongoDB URI from parameter or environment
        uri = mongodb_uri or os.getenv(
            "MONGODB_URI",
            "mongodb://admin:admin123@localhost:27017/swiftlogistics?authSource=admin"
        )
        
        # Extract database name from URI or environment
        db_name = os.getenv("MONGO_INITDB_DATABASE", cls._database_name)
        
        try:
            logger.info(f"Connecting to MongoDB at {uri.split('@')[1] if '@' in uri else uri}")
            
            # Create async MongoDB client
            cls._client = AsyncIOMotorClient(
                uri,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                maxPoolSize=50,
                minPoolSize=10,
            )
            
            # Test the connection
            await cls._client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
            
            # Get database instance
            cls._database = cls._client[db_name]
            logger.info(f"Using database: {db_name}")
            
            # Create indexes (you can expand this based on your needs)
            await cls._create_indexes()
            
            return cls._database
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise ConnectionFailure(f"Could not connect to MongoDB: {e}")
    
    @classmethod
    async def _create_indexes(cls):
        """Create necessary indexes for collections"""
        if cls._database is None:
            return
        
        try:
            # Orders collection indexes
            await cls._database.orders.create_index("order_id", unique=True)
            await cls._database.orders.create_index("client_id")
            await cls._database.orders.create_index("status")
            await cls._database.orders.create_index("created_at")
            
            # Drivers collection indexes
            await cls._database.drivers.create_index("driver_id", unique=True)
            await cls._database.drivers.create_index("email", unique=True)
            await cls._database.drivers.create_index("status")
            
            # Clients collection indexes
            await cls._database.clients.create_index("client_id", unique=True)
            await cls._database.clients.create_index("email", unique=True)
            
            # Shipments collection indexes
            await cls._database.shipments.create_index("shipment_id", unique=True)
            await cls._database.shipments.create_index("order_id")
            await cls._database.shipments.create_index("driver_id")
            await cls._database.shipments.create_index("status")
            
            # Contracts collection indexes
            await cls._database.contracts.create_index("contract_id", unique=True)
            await cls._database.contracts.create_index("client_id")
            
            # Invoices collection indexes
            await cls._database.invoices.create_index("invoice_id", unique=True)
            await cls._database.invoices.create_index("order_id")
            await cls._database.invoices.create_index("client_id")
            
            logger.info("Database indexes created successfully")
            
        except Exception as e:
            logger.warning(f"Failed to create some indexes: {e}")
    
    @classmethod
    async def close(cls):
        """Close MongoDB connection"""
        if cls._client is not None:
            cls._client.close()
            cls._client = None
            cls._database = None
            logger.info("MongoDB connection closed")
    
    @classmethod
    def get_database(cls) -> Optional[AsyncIOMotorDatabase]:
        """
        Get the current database instance.
        
        Returns:
            AsyncIOMotorDatabase or None if not connected
        """
        return cls._database
    
    @classmethod
    def is_connected(cls) -> bool:
        """Check if MongoDB is connected"""
        return cls._client is not None and cls._database is not None


# Convenience functions
async def get_database() -> AsyncIOMotorDatabase:
    """
    Get or create MongoDB database connection.
    
    Returns:
        AsyncIOMotorDatabase: Connected database instance
    """
    if not MongoDBClient.is_connected():
        return await MongoDBClient.connect()
    return MongoDBClient.get_database()


async def close_database_connection():
    """Close the MongoDB connection"""
    await MongoDBClient.close()
