from typing import Optional
from redis.asyncio import Redis
from app.config import get_settings
import logging

settings = get_settings()

logger = logging.getLogger(__name__)

class RedisConnectionError(Exception):
    """Redis connection error"""
    pass


class RedisOperationError(Exception):
    """Redis operation error"""
    pass

class RedisClient:
    """Redis client for token blacklisting and caching"""
    
    def __init__(self):
        self._redis: Optional[Redis] = None
        self._connection_pool = None
        
    async def connect(self, redis_url:str, **kwargs):
        """Connect to Redis with connection pooling"""
        
        try:
            # Default connection settings
            connection_kwargs = {
                "encoding": "utf-8",
                "decode_responses": True,
                "max_connections": 10,
                "socket_timeout": 5,
                "socket_connect_timeout": 5,
                "health_check_interval": 30,
                **kwargs  # Allow override of defaults
            }
            
            self._redis = Redis.from_url(
                redis_url,
                **connection_kwargs
            )
            
            # Test connection
            await self._redis.ping()
        
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise RedisConnectionError(f"Failed to connect to Redis: {e}")   

    async def disconnect(self):
        """Disconnect from Redis"""
        if self._redis:
            try:
                await self._redis.aclose()
                logger.info("Disconnected from Redis")
            except Exception as e:
                logger.error(f"Error disconnecting from Redis: {e}")
            finally:
                self._redis = None        
       
    async def blacklist_access_token_jti(self, jti: str, ttl_seconds: int):
        """Add token to blacklist with expiration"""
        
        if ttl_seconds <= 0:
            return  # Token already expired, no need to blacklist
        
        try:
            key = f"{settings.redis_prefix}blacklist:{jti}"
            await self._redis.setex(key, ttl_seconds, "1")
            logger.debug(f"Blacklisted access token JTI: {jti}")
        except Exception as e:
             logger.error(f"Failed to blacklist token: {e}")
             raise RedisOperationError(f"Failed to blacklist token: {e}")    
       
    async def is_access_token_blacklisted(self, jti: str) -> bool:
        """Check if token is blacklisted"""
        try:      
             key = f"{settings.redis_prefix}blacklist:{jti}"
             result = await self._redis.exists(key)
             return result > 0
        except Exception as e:
            logger.error(f"Failed to check token blacklist status: {e}")
            # Fail secure - consider token blacklisted on Redis error
            return False
               
    async def store_refresh_token_jti(self, user_id: str, jti: str, ttl_seconds: int):
        """Store refresh token for user"""
        try:
            key = f"{settings.redis_prefix}refresh:{user_id}"
            await self._redis.setex(key, ttl_seconds, jti)
            logger.debug(f"Refresh token stored for user: {user_id}")
        except Exception as e:
            logger.error(f"Failed to store refresh token: {e}")
            raise RedisOperationError(f"Failed to store refresh token: {e}")
        
    async def get_refresh_token_jti(self, user_id: str) -> Optional[str]:
        """Get refresh token for user"""
        try:
            key = f"{settings.redis_prefix}refresh:{user_id}"
            return await self._redis.get(key)
        except Exception as e:
            logger.error(f"Failed to get refresh token: {e}")
            return None
    
    async def delete_refresh_token_jti(self, user_id: str) -> bool:
        """Delete refresh token for user"""
        try:
            key = f"{settings.redis_prefix}refresh:{user_id}"
            result = await self._redis.delete(key)
            logger.debug(f"Refresh token deleted for user: {user_id}, deleted: {result}")
        except Exception as e:
            logger.error(f"Failed to delete refresh token: {e}")
            raise RedisOperationError(f"Failed to delete refresh token: {e}")          
     
    @property
    def redis(self) -> Redis:
        """Get Redis client instance"""
        if not self._redis:
            raise RuntimeError("Redis client not connected. Call connect() first.")
        return self._redis
    
redis_client = RedisClient()    