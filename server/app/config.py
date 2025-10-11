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
    
    model_config = SettingsConfigDict(env_file=".env")


def get_settings() -> Settings:
    return Settings()     