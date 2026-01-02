from typing import List, Dict, Any, Optional
from pinecone import PineconeAsyncio, ServerlessSpec
import logging
from app.config import Settings
from app.core.exceptions import VectorStoreError

logger = logging.getLogger(__name__)

class PineconeService:
    def __init__(self):
        self.settings = Settings()
        self._client = None
        self._index = None
        self._index_host = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
    
    async def __aexit__(self):
        """Async context manager exit"""
        await self.disconnect()
        return False
    
    async def connect(self):
        """Connect to Pinecone using async context manager pattern"""
        try:
            # Use async context manager for PineconeAsyncio
            self._client = PineconeAsyncio(api_key=self.settings.pinecone_api_key)
            
            # Ensure index exists
            await self._ensure_index()
            
            # Get the index host URL
            index_description = await self._client.describe_index(self.settings.pinecone_index_name)
            self._index_host = index_description.host
            
            # Create async index connection using host
            self._index = self._client.IndexAsyncio(host=self._index_host)
            
            logger.info(f"Connected to Pinecone index: {self.settings.pinecone_index_name}")
        
        except Exception as e:
            logger.error(f"Failed to connect to Pinecone: {str(e)}")
            # Clean up on connection failure
            await self._cleanup()
            raise VectorStoreError(f"Failed to connect to vector store: {str(e)}")     
    
    async def disconnect(self):
        """Close Pinecone connection"""
        await self._cleanup()
        logger.info("Disconnected from Pinecone")    
    
    async def _cleanup(self):
        """Internal cleanup method"""
        if self._index:
            # IndexAsyncio doesn't have a close method, just set to None
            self._index = None
        if self._client:
            await self._client.close()
            self._client = None
        self._index_host = None
            
    async def _ensure_index(self):
        """Ensure the Pinecone index exists"""
        try:
            logger.info(f"Checking Pinecone index: {self.settings.pinecone_index_name}")
            
            # Check if index exists
            if not await self._client.has_index(self.settings.pinecone_index_name):
                logger.info(f"Creating Pinecone index: {self.settings.pinecone_index_name}")
                
                # Create index if it doesn't exist
                await self._client.create_index(
                    name=self.settings.pinecone_index_name,
                    dimension=768,
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region=self.settings.pinecone_environment
                    )
                )
                
                logger.info(f"Created Pinecone index: {self.settings.pinecone_index_name}")
            else:
                logger.info(f"Pinecone index already exists: {self.settings.pinecone_index_name}")
        
        except Exception as e:
            logger.error(f"Error ensuring Pinecone index: {str(e)}")
            raise VectorStoreError(f"Failed to ensure index exists: {str(e)}")       
    
    async def upsert_embeddings(self, vectors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Upsert embeddings to Pinecone"""
        if not self._index:
            raise VectorStoreError("Vector store not connected")
        
        try:
            # Prepare vectors for upsert
            all_vectors = [
                {
                    "id": vec["embedding_id"],
                    "values": vec["embedding"]
                }
                for vec in vectors
            ]
          
            result = await self._index.upsert(vectors=all_vectors)
            
            logger.info(f"Upserted {result.upserted_count} vectors to Pinecone")
            
            return {"upserted_count": result.upserted_count}
        except Exception as e:
            logger.error(f"Pinecone upsert failed: {str(e)}")
            raise VectorStoreError(f"Failed to upsert embeddings: {str(e)}")
    
    async def query_similar(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter: Optional[Dict[str, Any]] = None,
        include_metadata: bool = False, 
        include_values: bool = False   
    ) -> List[Dict[str, Any]]:
        """Query similar vectors"""
        if not self._index:
            raise VectorStoreError("Vector store not connected")
        
        try:
            result = await self._index.query(
                vector=query_vector,
                top_k=top_k,
                filter=filter,
                include_values=include_values,
                include_metadata=include_metadata,
            )
            
            matches = []
            for match in result.matches:
                match_data = {
                    "id": match.id,
                    "score": match.score,
                    # Safely access metadata and values if they exist
                    # "metadata": match.metadata if match.metadata else {},
                    # "values": match.values if match.values else [] 
                }
                matches.append(match_data)
            
            return matches
        except Exception as e:
            logger.error(f"Pinecone query failed: {str(e)}")
            raise VectorStoreError(f"Query failed: {str(e)}")
    
    async def delete_vectors(self, ids: List[str]) -> Dict[str, Any]:
        """Delete vectors by IDs"""
        if not self._index:
            raise VectorStoreError("Vector store not connected")
        
        try:
            await self._index.delete(ids=ids)
            logger.info(f"Deleted vectors: {ids}")
            return {"deleted_count": len(ids)}
        except Exception as e:
            logger.error(f"Pinecone delete failed: {str(e)}")
            raise VectorStoreError(f"Failed to delete vectors: {str(e)}")

