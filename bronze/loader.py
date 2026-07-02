import pandas as pd
from sqlalchemy import text
from utils.logger import get_logger
from datetime import datetime, timezone
from bronze.insert_query import insert_dataframe
from db.connection import get_bronze_engine
from pathlib import Path

logger = get_logger("bronze.loader")

TABLE_MAP = {
    "production"        : "bronze.production",
    "rainfall"           : "bronze.rainfall",
    "temperature"        : "bronze.temperature",
    "production_coded"   : "bronze.production_coded",
    "crop_analytics"     : "bronze.crop_analytics",
}
 
_VERIFIED_TABLES: set[str] = set()


def ensure_table_exists(full_table_name: str, force: bool = False) -> bool:
   
    full_table_name = full_table_name.strip().lower()

    if not force and full_table_name in _VERIFIED_TABLES:
        return True

    engine = get_bronze_engine()

    if "." not in full_table_name:
        raise ValueError("Table must be in format 'schema.table'")

    schema, table = full_table_name.split(".", 1)

    def check_schema_exists(conn) -> bool:
        query = text("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.schemata
                WHERE schema_name = :schema
            );
        """)
        return conn.execute(query, {"schema": schema}).scalar()

    def check_table_exists(conn) -> bool:
        query = text("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_schema = :schema
                  AND table_name   = :table
            );
        """)
        return conn.execute(query, {"schema": schema, "table": table}).scalar()

    base_dir       = Path(__file__).resolve().parent
    migration_file = base_dir.parent / "db" / "migrations" / "bronze_tables.sql"

    with engine.begin() as conn:
        if not check_schema_exists(conn):
            logger.info(f"Schema '{schema}' not found — creating...")
            conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))

        if check_table_exists(conn):
            logger.info(f"Table '{schema}.{table}' already exists.")
            _VERIFIED_TABLES.add(full_table_name)
            return True

        logger.info(f"Table '{schema}.{table}' not found — running migration...")

        if not migration_file.exists():
            raise FileNotFoundError(f"Migration file not found: {migration_file}")

        with open(migration_file, "r", encoding="utf-8") as f:
            sql_script = f.read()

        conn.execute(text(sql_script))
        logger.info(f"Migration executed from: {migration_file}")

        created = check_table_exists(conn)
        if not created:
            raise RuntimeError(
                f"Migration ran but '{schema}.{table}' still not found. "
                f"Check that {migration_file.name} creates this table."
            )

        logger.info(f"Table '{schema}.{table}' created successfully.")
        _VERIFIED_TABLES.add(full_table_name)
        return True


def save_to_bronze(df: pd.DataFrame, source_name: str, run_id: str) -> int:
    table = TABLE_MAP.get(source_name)
    if not table:
        raise ValueError(f"No table mapped for source: {source_name}")
    table_ready = ensure_table_exists(table)
    if not table_ready:
        raise RuntimeError(f"Table {table} could not be created or verified. Aborting insert.")
    rows_inserted = insert_dataframe(df, table)
    logger.info(f"[{source_name}] Saved {rows_inserted} rows to {table}")
    return rows_inserted


def add_metadata(df: pd.DataFrame, source_name: str, run_id: str) -> pd.DataFrame:
    ingestion_time = datetime.now(timezone.utc).isoformat()
    df = df.copy()
    df["_source"]       = source_name
    df["_ingested_at"]  = ingestion_time
    df["_pipeline_run"] = run_id
    return df