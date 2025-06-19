from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App Settings
    app_name: str = "SmartInvest.ai"
    debug: bool = True
    port: int = 8000
    
    # API Keys
    news_api_key: Optional[str] = None
    friendli_api_key: Optional[str] = None
    weaviate_api_key: Optional[str] = None
    
    # Database
    database_url: str = "sqlite:///./finance_data.db"
    
    # Cache
    cache_duration: int = 300  # 5 minutes
    
    # Weaviate
    weaviate_url: str = "http://localhost:8080"
    
    # News API
    news_api_base_url: str = "https://newsapi.org/v2"
    
    # FriendliAI
    friendli_base_url: str = "https://inference.friendli.ai"
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"


settings = Settings() 