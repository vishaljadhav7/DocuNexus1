from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = False
    secret_key: str   
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    database_url : str
    redis_url : str
    redis_prefix:str
    
    cloudinary_cloud_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str
    
    chunk_size:int 
    chunk_overlap:int
    
    gemini_api_key : str
    gemini_model : str = "gemini-2.5-flash-lite"
    gemini_embedding_model: str = "models/text-embedding-004"
    
    pinecone_api_key : str
    pinecone_index_name : str
    pinecone_environment : str
    
    redis_prefix_celery : str
    celery_broker_url : str
    celery_result_backend : str
    
    class Config:
        env_file = ".env"
        extra = 'ignore'


def get_settings() -> Settings:
    return Settings()     