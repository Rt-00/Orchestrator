from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "SSH Remote Execution API"
    APP_DESCRIPTION: str = "Execute scripts on multiple hosts via SSH"
    APP_VERSION: str = "1.0.0"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "info"

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    # SSH Settings
    SSH_DEFAULT_TIMEOUT: int = 300
    SSH_MAX_TIMEOUT: int = 3600
    SSH_CONNECTION_TIMEOUT: int = 30
    SSH_BANNER_TIMEOUT: int = 60
    SSH_AUTH_TIMEOUT: int = 30
    SSH_RETRY_COUNT: int = 3

    # Execution Settings
    MAX_CONCURRENT_DEFAULT: int = 5
    MAX_CONCURRENT_LIMIT: int = 50
    THREAD_POOL_SIZE: int = 50

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
