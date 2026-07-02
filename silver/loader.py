
import io
import csv
import time
import pandas as pd
from datetime import datetime, timezone
from sqlalchemy import text
from db.connection import get_bronze_engine, get_silver_engine
from silver.rules import SILVER_RULES
from utils.logger import get_logger
from silver.transformer.t_production import Transform_Production
from silver.transformer.t_crop_analytics import Transform_Crop_Analytics
from silver.transformer.t_production_coded import Transform_Production_Coded
from silver.transformer.t_rainfall import Transform_Rainfall
from silver.transformer.t_temperature import Transform_Temperature
import traceback
from snowflake.connector.pandas_tools import write_pandas

logger = get_logger("silver.loader")

# Cache of tables we've already confirmed exist, so _ensure_table() only
# hits information_schema once per table per process instead of on every call.
_VERIFIED_TABLES: set[str] = set()


def _ensure_table(full_table_name: str, engine) -> None:
    """
    Verify a target silver table exists before we try to write to it.
    Raises RuntimeError with a clear "run the migration" message if not.
    """
    if full_table_name in _VERIFIED_TABLES:
        logger.debug(f"[{full_table_name}] Already verified this run, skipping check")
        return

    schema, table = full_table_name.strip().lower().split(".", 1)
    logger.debug(f"[{full_table_name}] Verifying table exists in information_schema")

    with engine.begin() as conn:
        exists = conn.execute(text("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_schema = :s AND table_name = :t
            )
        """), {"s": schema, "t": table}).scalar()

        if not exists:
            logger.warning(f"[{full_table_name}] Table not found — creating schema '{schema}' and raising")
            conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
            raise RuntimeError(
                f"Table '{full_table_name}' not found. "
                f"Run the silver migration first: db/migrations/silver_tables.sql"
            )

    logger.debug(f"[{full_table_name}] Table verified OK")
    _VERIFIED_TABLES.add(full_table_name)


def _read_bronze(source_table: str, run_id: str | None = None) -> pd.DataFrame:
    """Pull the raw rows for one bronze source table, optionally scoped to a single run_id."""
    engine = get_bronze_engine()
    schema, table = source_table.strip().split(".", 1)

    if run_id:
        logger.debug(f"[{source_table}] Reading bronze scoped to run_id={run_id}")
        query = text(f'SELECT * FROM "{schema}"."{table}" WHERE "_pipeline_run" = :run_id')
        params = {"run_id": run_id}
    else:
        logger.debug(f"[{source_table}] Reading full bronze table (no run_id filter)")
        query = text(f'SELECT * FROM "{schema}"."{table}"')
        params = {}

    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params=params)

    logger.info(f"[{source_table}] Read {len(df)} rows from bronze")
    return df


def _bulk_write(df: pd.DataFrame, full_table_name: str, engine, extra_cols: list[str] = None) -> int:
    """
    Write a clean/reject frame into silver.

    - Small frames (< COPY_THRESHOLD rows) go through pandas.to_sql (multi-row INSERT).
    - Large frames use Snowflake's write_pandas bulk COPY, which is much faster
      for high row counts.
    """
    try:
        if df.empty:
            logger.debug(f"[{full_table_name}] Nothing to write (empty frame)")
            return 0

        schema, table = full_table_name.strip().split(".", 1)
        COPY_THRESHOLD = 2000

        if len(df) >= COPY_THRESHOLD:
            logger.debug(f"[{full_table_name}] {len(df)} rows >= {COPY_THRESHOLD}, using write_pandas bulk COPY")
            conn = engine.raw_connection()

            try:
                sf_conn = conn.connection if hasattr(conn, "connection") else conn

                # Only keep columns that actually exist on the target table —
                # protects against extra/renamed columns in the dataframe
                # blowing up the COPY.
                table_cols = get_table_columns(engine, table, schema)
                logger.debug(f"[{full_table_name}] Target table columns: {table_cols}")
                df = df[[col for col in df.columns if col.upper() in [c.upper() for c in table_cols]]]

                # NOTE: kept here (disabled) as a quick manual-debug escape
                # hatch — uncomment locally if you need to inspect exactly
                # what's about to be written, don't leave it on in normal runs.
                # df.to_csv(f"{table}-{datetime.now().microsecond}csv_11.csv", index=False)

                success, nchunks, nrows, output = write_pandas(
                    sf_conn,
                    df,
                    table_name=table.upper(),
                    schema=schema.upper()
                )
                conn.commit()

                if not success:
                    raise RuntimeError(f"write_pandas failed: {output}")

                logger.debug(f"[{full_table_name}] write_pandas OK — {nrows} rows in {nchunks} chunk(s)")

            except Exception as e:
                # Log full context before re-raising so the pipeline-level
                # catch in pipeline.py has already captured everything it needs.
                logger.error(f"[{full_table_name}] Bulk write failed — {type(e).__name__}: {e}")
                logger.error(traceback.format_exc())
                raise

            finally:
                conn.close()

        else:
            logger.debug(f"[{full_table_name}] {len(df)} rows < {COPY_THRESHOLD}, using to_sql multi-insert")
            df.to_sql(
                name=table,
                schema=schema,
                con=engine,
                if_exists='append',
                index=False,
                method='multi',
                chunksize=500
            )

        return len(df)

    except Exception as e:
        # Keep this write "soft-fail" (returns None instead of raising) to match
        # existing behavior, but make sure it's actually logged instead of print().
        logger.error(f"[{full_table_name}] _bulk_write failed: {e}")


def get_table_columns(engine, table_name: str, schema: str = None) -> list[str]:
    """Fetch the ordered column list for a table, used to filter frames before a bulk write."""
    query = f"""
    SELECT LISTAGG(COLUMN_NAME, ', ') WITHIN GROUP (ORDER BY ORDINAL_POSITION) as cols
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = '{table_name.upper()}'
    """
    if schema:
        query += f" AND TABLE_SCHEMA = '{schema.upper()}'"

    result = pd.read_sql(query, engine)
    cols = result["cols"][0].split(", ") if not result.empty else []
    logger.debug(f"[{schema}.{table_name}] Fetched {len(cols)} column(s) from information_schema")
    return cols


def run_silver_source(source_table: str, run_id: str | None = None) -> dict:
    """
    Run one bronze source table all the way through to silver:
    read -> transform -> tag load timestamp -> bulk write clean + reject frames.

    Returns a result dict consumed by pipeline.py / silverrun.py to build
    the final summary banner:
        {
            "source": str,
            "status": "success" | "failed",
            "rows_in": int,
            "clean_rows": int,
            "rejected_rows": int,
            "seconds": float,
            "reasons": dict,
        }
    """
    rules = SILVER_RULES.get(source_table)
    silver_engine = get_silver_engine()
    target = rules["target_table"]
    rejects = rules["reject_table"]
    clean_df = []
    reject_df = []
    t0 = time.perf_counter()

    raw = _read_bronze(source_table, run_id)

    # Dispatch to the correct transformer for this source table.
    logger.debug(f"[{source_table}] Dispatching to transformer")
    match source_table:
        case 'bronze.production':
            clean_df, reject_df = Transform_Production(raw, rules)
        case 'bronze.rainfall':
            clean_df, reject_df = Transform_Rainfall(raw, rules)
        case 'bronze.temperature':
            clean_df, reject_df = Transform_Temperature(raw, rules)
        case 'bronze.production_coded':
            clean_df, reject_df = Transform_Production_Coded(raw, rules)
        case 'bronze.crop_analytics':
            clean_df, reject_df = Transform_Crop_Analytics(raw, rules)
        case _:
            # Unknown source table — nothing to transform, log loudly since
            # this usually means SILVER_RULES and the match statement are
            # out of sync.
            logger.warning(f"[{source_table}] No transformer registered for this source — skipping")

    # Stamp both frames with the silver load time.
    now = datetime.now(timezone.utc).isoformat()
    for frame in [clean_df, reject_df]:
        if not frame.empty:
            frame["_SILVER_LOADED_AT"] = now
    logger.debug(f"[{source_table}] Tagged frames with _SILVER_LOADED_AT={now}")

    clean_rows = _bulk_write(clean_df, target, silver_engine)
    rejected_rows = _bulk_write(reject_df, rejects, silver_engine)
    elapsed = time.perf_counter() - t0

    # Tally up why rows were rejected, e.g. {"missing value": 12, "bad unit": 3}
    reason_counts = {}
    if not reject_df.empty and "reject_reason" in reject_df.columns:
        for reasons in reject_df["reject_reason"]:
            for r in str(reasons).split(";"):
                r = r.strip()
                reason_counts[r] = reason_counts.get(r, 0) + 1

    logger.info(
        f"[{source_table}] Silver done in {elapsed:.2f}s — "
        f"{len(raw)} in | {clean_rows} clean | {rejected_rows} rejected | "
        f"reasons: {reason_counts}"
    )

    return {
        "source": source_table,
        "status": "success",
        "rows_in": len(raw),
        "clean_rows": clean_rows or 0,
        "rejected_rows": rejected_rows or 0,
        "seconds": round(elapsed, 2),
        "reasons": reason_counts,
    }