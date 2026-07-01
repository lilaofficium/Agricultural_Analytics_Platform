import io
import csv
import time
import pandas as pd
from datetime import datetime, timezone
from sqlalchemy import text
from db.connection import get_bronze_engine, get_silver_engine
from silver.validator import validate_dataframe
from silver.rules import SILVER_RULES
from utils.logger import get_logger

logger = get_logger("silver.loader")

_VERIFIED_TABLES: set[str] = set()


def _ensure_table(full_table_name: str, engine) -> None:
    if full_table_name in _VERIFIED_TABLES:
        return
    schema, table = full_table_name.strip().lower().split(".", 1)
    with engine.begin() as conn:
        exists = conn.execute(text("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_schema = :s AND table_name = :t
            )
        """), {"s": schema, "t": table}).scalar()
        if not exists:
            conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
            raise RuntimeError(
                f"Table '{full_table_name}' not found. "
                f"Run the silver migration first: db/migrations/silver_tables.sql"
            )
    _VERIFIED_TABLES.add(full_table_name)


def _read_bronze(source_table: str, run_id: str | None = None) -> pd.DataFrame: 

    ### diffrent case which will call diffrent funtion where bronze table 
    engine = get_bronze_engine()
    schema, table = source_table.strip().split(".", 1)
    if run_id:
        query = text(f'SELECT * FROM "{schema}"."{table}" WHERE "_pipeline_run" = :run_id')
        params = {"run_id": run_id}
    else:
        query = text(f'SELECT * FROM "{schema}"."{table}"')
        params = {}
    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params=params)
    logger.info(f"[{source_table}] Read {len(df)} rows from bronze")
    return df


def _bulk_write(df: pd.DataFrame, full_table_name: str, engine, extra_cols: list[str] = None) -> int: 
    if df.empty:
        return 0

    schema, table = full_table_name.strip().split(".", 1)
    cols = [c for c in df.columns]
    COPY_THRESHOLD = 2000

    if len(df) >= COPY_THRESHOLD:
        buf = io.StringIO()
        writer = csv.writer(buf)
        for row in df[cols].itertuples(index=False, name=None):
            writer.writerow(['' if (v is None or (isinstance(v, float) and pd.isna(v))) else v for v in row])
        buf.seek(0)
        raw = engine.raw_connection()
        try:
            cur = raw.cursor()
            cols_sql = ", ".join(f'"{c}"' for c in cols)
            cur.copy_expert(
                f'COPY "{schema}"."{table}" ({cols_sql}) FROM STDIN WITH (FORMAT csv, NULL \'\')',
                buf
            )
            raw.commit()
            cur.close()
        except Exception:
            raw.rollback()
            raise
        finally:
            raw.close()
    else:
        df.to_sql(
            name=table, schema=schema, con=engine,
            if_exists='append', index=False,
            method='multi', chunksize=500
        )
    return len(df)


def run_silver_source(source_table: str, run_id: str | None = None) -> dict: 
    rules = SILVER_RULES.get(source_table)
    silver_engine = get_silver_engine()
    target  = rules["target_table"]
    rejects = rules["reject_table"]
    clean_df=[]
    reject_df=[]
    match source_table:
        case 'bronze.production':
             print('') 
             t0  = time.perf_counter()
             raw = _read_bronze(source_table, run_id)
             ##call Transformer filedr for each table clean_df, reject_df = validate_dataframe(raw, rules)
        case 'bronze.rainfall':
            print('')
        case 'bronze.temperature':
            print('')
        case _:
            print('')  

     
    now = datetime.now(timezone.utc).isoformat()
    for frame in [clean_df, reject_df]:
        if not frame.empty:
            frame["_silver_loaded_at"] = now

    clean_rows    = _bulk_write(clean_df,  target,  silver_engine)
    rejected_rows = _bulk_write(reject_df, rejects, silver_engine)
    elapsed = time.perf_counter() - t0
 
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

    # return {
    #     "source":        source_table,
    #     "status":        "success",
    #     "rows_in":       len(raw),
    #     "rows_clean":    clean_rows,
    #     "rows_rejected": rejected_rows,
    #     "reject_reasons": reason_counts,
    #     "seconds":       round(elapsed, 2),
    # }