from pydantic_settings import BaseSettings
from enum import Enum 
import os 
from dotenv import load_dotenv 


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING     = "staging"      
    PRODUCTION  = "production"   


class Settings(BaseSettings): 
    env: str = Environment.DEVELOPMENT
    log_level: str = "DEBUG"
    api_timeout:       int = 10
    api_retry_count:   int = 3
    api_retry_backoff: int = 2

    postgres_user: str = os.getenv("POSTGRES_USER", "neondb_owner")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "")
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: str = os.getenv("POSTGRES_PORT", "5432")
    postgres_db: str = os.getenv("POSTGRES_DB", "postgres")
    postgres_sslmode: str = os.getenv("POSTGRES_SSLMODE", "require")



    class Config:
        env_file          = ".env"
        env_file_encoding = "utf-8"
        case_sensitive    = False

    @property
    def postgres_url_psycopg(self) -> str: 
        return (
            f"dbname={self.postgres_db} "
            f"user={self.postgres_user} "
            f"password={self.password} "
            f"host={self.postgres_host} "
            f"port={self.postgres_port} "
            f"sslmode={self.postgres_sslmode}"
        )