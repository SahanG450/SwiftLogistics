"""
Base repository pattern for MongoDB operations

Provides common CRUD operations and can be extended by specific repositories
"""
from typing import TypeVar, Generic, Optional, List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from bson import ObjectId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """
    Base repository class providing common CRUD operations for MongoDB collections.
    
    This class implements the repository pattern to abstract database operations
    and can be extended by specific entity repositories.
    """
    
    def __init__(self, database: AsyncIOMotorDatabase, collection_name: str):
        """
        Initialize repository with database and collection.
        
        Args:
            database: MongoDB database instance
            collection_name: Name of the collection to operate on
        """
        self.database = database
        self.collection_name = collection_name
        self.collection: AsyncIOMotorCollection = database[collection_name]
    
    async def create(self, document: Dict[str, Any]) -> str:
        """
        Create a new document in the collection.
        
        Args:
            document: Document data to insert
            
        Returns:
            str: ID of the created document
        """
        # Add timestamps
        document['created_at'] = datetime.utcnow()
        document['updated_at'] = datetime.utcnow()
        
        result = await self.collection.insert_one(document)
        logger.info(f"Created document in {self.collection_name}: {result.inserted_id}")
        return str(result.inserted_id)
    
    async def find_by_id(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Find a document by its MongoDB ObjectId.
        
        Args:
            document_id: MongoDB ObjectId as string
            
        Returns:
            Document data or None if not found
        """
        try:
            result = await self.collection.find_one({"_id": ObjectId(document_id)})
            if result:
                result['_id'] = str(result['_id'])
            return result
        except Exception as e:
            logger.error(f"Error finding document by ID {document_id}: {e}")
            return None
    
    async def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Find a single document matching the query.
        
        Args:
            query: MongoDB query filter
            
        Returns:
            Document data or None if not found
        """
        result = await self.collection.find_one(query)
        if result and '_id' in result:
            result['_id'] = str(result['_id'])
        return result
    
    async def find_many(
        self,
        query: Dict[str, Any] = None,
        skip: int = 0,
        limit: int = 100,
        sort: List[tuple] = None
    ) -> List[Dict[str, Any]]:
        """
        Find multiple documents matching the query.
        
        Args:
            query: MongoDB query filter (default: all documents)
            skip: Number of documents to skip
            limit: Maximum number of documents to return
            sort: List of (field, direction) tuples for sorting
            
        Returns:
            List of matching documents
        """
        query = query or {}
        cursor = self.collection.find(query).skip(skip).limit(limit)
        
        if sort:
            cursor = cursor.sort(sort)
        
        results = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string
        for result in results:
            if '_id' in result:
                result['_id'] = str(result['_id'])
        
        return results
    
    async def update_by_id(self, document_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Update a document by its MongoDB ObjectId.
        
        Args:
            document_id: MongoDB ObjectId as string
            update_data: Fields to update
            
        Returns:
            bool: True if document was updated, False otherwise
        """
        try:
            # Add updated timestamp
            update_data['updated_at'] = datetime.utcnow()
            
            result = await self.collection.update_one(
                {"_id": ObjectId(document_id)},
                {"$set": update_data}
            )
            
            success = result.modified_count > 0
            if success:
                logger.info(f"Updated document in {self.collection_name}: {document_id}")
            return success
            
        except Exception as e:
            logger.error(f"Error updating document {document_id}: {e}")
            return False
    
    async def update_one(self, query: Dict[str, Any], update_data: Dict[str, Any]) -> bool:
        """
        Update a single document matching the query.
        
        Args:
            query: MongoDB query filter
            update_data: Fields to update
            
        Returns:
            bool: True if document was updated, False otherwise
        """
        # Add updated timestamp
        update_data['updated_at'] = datetime.utcnow()
        
        result = await self.collection.update_one(query, {"$set": update_data})
        return result.modified_count > 0
    
    async def update_many(self, query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        """
        Update multiple documents matching the query.
        
        Args:
            query: MongoDB query filter
            update_data: Fields to update
            
        Returns:
            int: Number of documents updated
        """
        # Add updated timestamp
        update_data['updated_at'] = datetime.utcnow()
        
        result = await self.collection.update_many(query, {"$set": update_data})
        logger.info(f"Updated {result.modified_count} documents in {self.collection_name}")
        return result.modified_count
    
    async def delete_by_id(self, document_id: str) -> bool:
        """
        Delete a document by its MongoDB ObjectId.
        
        Args:
            document_id: MongoDB ObjectId as string
            
        Returns:
            bool: True if document was deleted, False otherwise
        """
        try:
            result = await self.collection.delete_one({"_id": ObjectId(document_id)})
            success = result.deleted_count > 0
            if success:
                logger.info(f"Deleted document from {self.collection_name}: {document_id}")
            return success
        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {e}")
            return False
    
    async def delete_one(self, query: Dict[str, Any]) -> bool:
        """
        Delete a single document matching the query.
        
        Args:
            query: MongoDB query filter
            
        Returns:
            bool: True if document was deleted, False otherwise
        """
        result = await self.collection.delete_one(query)
        return result.deleted_count > 0
    
    async def delete_many(self, query: Dict[str, Any]) -> int:
        """
        Delete multiple documents matching the query.
        
        Args:
            query: MongoDB query filter
            
        Returns:
            int: Number of documents deleted
        """
        result = await self.collection.delete_many(query)
        logger.info(f"Deleted {result.deleted_count} documents from {self.collection_name}")
        return result.deleted_count
    
    async def count(self, query: Dict[str, Any] = None) -> int:
        """
        Count documents matching the query.
        
        Args:
            query: MongoDB query filter (default: all documents)
            
        Returns:
            int: Number of matching documents
        """
        query = query or {}
        return await self.collection.count_documents(query)
    
    async def exists(self, query: Dict[str, Any]) -> bool:
        """
        Check if any document exists matching the query.
        
        Args:
            query: MongoDB query filter
            
        Returns:
            bool: True if at least one document exists
        """
        count = await self.collection.count_documents(query, limit=1)
        return count > 0
    
    async def aggregate(self, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Perform an aggregation query.
        
        Args:
            pipeline: MongoDB aggregation pipeline
            
        Returns:
            List of aggregation results
        """
        cursor = self.collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)
        
        # Convert ObjectId to string
        for result in results:
            if '_id' in result and isinstance(result['_id'], ObjectId):
                result['_id'] = str(result['_id'])
        
        return results
