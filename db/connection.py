from sqlalchemy import create_engine, text
from config.settings import get_settings
from utils.logger import get_logger
 
logger   = get_logger("db_connection")
settings = get_settings()
 
 
def get_bronze_engine():
    engine = create_engine(
        settings.postgres_url_psycopg,
        pool_size=5,
        max_overflow=2,
        pool_pre_ping=True,
    )
    return engine
 
 
def ensure_bronze_schema(migration_file: str = "db/migrations/bronze_tables.sql") -> None:
    engine = get_bronze_engine()
    with open(migration_file, "r", encoding="utf-8") as f:
        sql_script = f.read()
    with engine.begin() as conn:
        conn.execute(text(sql_script))
    logger.info("Bronze schema ensured.")
 
 
def get_bronze_connection() -> bool:
    try:
        engine = get_bronze_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Bronze DB connected successfully")
        return True
    except Exception as e:
        logger.error(f"Bronze DB connection failed: {e}")
        return False