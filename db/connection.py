from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from config.settings import get_settings
from utils.logger import get_logger
from sqlalchemy.exc import SQLAlchemyError

logger   = get_logger("db_connection")
settings = get_settings()
 
_engine: Engine | None = None


def get_bronze_engine() -> Engine:
    global _engine
    if _engine is None:
        logger.info("Creating bronze engine (first call this process)")
        _engine = create_engine(
            settings.postgres_url_psycopg,
            pool_size=5,
            max_overflow=2,
            pool_pre_ping=True,
        )
    return _engine

def get_silver_engine() -> Engine:
    global _engine

    if _engine is None:
        logger.info("Creating Snowflake engine (first call this process)")

        try: 
            _engine = create_engine(
                settings.snowflake_url,
                pool_size=5,
                max_overflow=2,
                pool_pre_ping=True,
            )
 
            with _engine.connect() as conn:
                conn.execute(text("SELECT CURRENT_VERSION()"))

            logger.info("Successfully connected to Snowflake.")

        except SQLAlchemyError as e:
            logger.exception("Failed to connect to Snowflake.")
            raise

        except Exception as e:
            logger.exception("Unexpected error while creating Snowflake engine.")
            raise

    return _engine


def dispose_bronze_engine() -> None: 
    global _engine
    if _engine is not None:
        _engine.dispose()
        _engine = None
        logger.info("Bronze engine disposed")


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