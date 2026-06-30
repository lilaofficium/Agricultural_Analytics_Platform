from pydantic_settings import BaseSettings
from enum import Enum
import os
from dotenv import load_dotenv

load_dotenv()  # ← was imported but never called


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING     = "staging"
    PRODUCTION  = "production"


class Settings(BaseSettings):
    env:               str = Environment.DEVELOPMENT
    log_level:         str = "DEBUG"
    api_timeout:       int = 10
    api_retry_count:   int = 3
    api_retry_backoff: int = 2

    postgres_user:     str = os.getenv("POSTGRES_USER",     "neondb_owner")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "")
    postgres_host:     str = os.getenv("POSTGRES_HOST",     "localhost")
    postgres_port:     str = os.getenv("POSTGRES_PORT",     "5432")
    postgres_db:       str = os.getenv("POSTGRES_DB",       "postgres")
    # postgres_sslmode:  str = os.getenv("POSTGRES_SSLMODE",  "require")

    class Config:
        env_file          = ".env"
        env_file_encoding = "utf-8"
        case_sensitive    = False

    # for bronze
    @property
    def postgres_url_psycopg(self) -> str:
        return (
                    f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
                    f"?sslmode=require"
                )

 
def get_settings() -> Settings:
    return Settings() 