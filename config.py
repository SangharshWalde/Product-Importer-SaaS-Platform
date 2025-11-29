import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/product_importer"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 104857600  # 100MB in bytes
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:8000,http://127.0.0.1:8000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    @classmethod
    def _fix_redis_url(cls, url: str) -> str:
        if not url:
            return url
            
        # Clean up common copy-paste errors
        url = url.strip()
        if "redis-cli" in url:
            # Extract URL from redis-cli command
            # Example: redis-cli --tls -u redis://...
            import re
            match = re.search(r'(rediss?://\S+)', url)
            if match:
                url = match.group(1)
        
        # Handle Upstash REST URL (https://) -> rediss://
        # Note: This only works if the user included user:pass in the https URL, which is rare for REST.
        # But we can try to fix the scheme at least.
        if url.startswith("https://") and "upstash.io" in url:
            url = url.replace("https://", "rediss://", 1)

        # Force SSL for Upstash
        if "upstash.io" in url and url.startswith("redis://"):
            url = url.replace("redis://", "rediss://", 1)
            
        # Add ssl_cert_reqs=none if using SSL
        if url.startswith("rediss://") and "ssl_cert_reqs" not in url:
            separator = "&" if "?" in url else "?"
            return f"{url}{separator}ssl_cert_reqs=none"
            
        return url

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.REDIS_URL = self._fix_redis_url(self.REDIS_URL)
        self.CELERY_BROKER_URL = self._fix_redis_url(self.CELERY_BROKER_URL)
        self.CELERY_RESULT_BACKEND = self._fix_redis_url(self.CELERY_RESULT_BACKEND)


# Global settings instance
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
