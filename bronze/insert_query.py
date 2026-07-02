import io
import time
import csv
from db.connection import get_bronze_engine
from sqlalchemy import text 
from pathlib import Path
import pandas as pd
from utils.logger import get_logger
import numpy as np 
from datetime import datetime, timezone

logger = get_logger("bronze.insert_query")


def _prepare_production(df: pd.DataFrame):
    df.columns = df.columns.str.strip()
    df['domain'] = df['Domain'].astype(str)
    df['area'] = df['Area'].astype(str)
    df['element'] = df['Element'].astype(str)
    df['item'] = df['Item'].astype(str)
    df['year'] = df['Year'].astype(int)
    df['unit'] = df['Unit'].astype(str)
    df['value'] = pd.to_numeric(df['Value'], errors='coerce')
    df['_source_file']  = df['_source'].astype(str)
    df['_pipeline_run'] = df['_pipeline_run'].astype(str)
    df['_loaded_at']    = pd.to_datetime(df['_ingested_at'], utc=True)

    insert_cols = [
        'domain', 'area', 'element', 'item', 'year', 'unit', 'value',
        '_source_file', '_pipeline_run', '_loaded_at'
    ]

    sql = text('''INSERT INTO bronze.production (
            domain, area, element, item, year, unit, value,
            _source_file, _pipeline_run, _loaded_at
        ) VALUES (
            :domain, :area, :element, :item, :year, :unit, :value,
            :_source_file, :_pipeline_run, :_loaded_at
        )''')

    return df, insert_cols, sql


def _prepare_rainfall(df: pd.DataFrame): 
    df.columns = df.columns.str.strip()
    df['area'] = df['Area'].astype(str)
    df['year'] = df['Year'].astype(str)
    df['average_rain_fall_mm_per_year'] = df['average_rain_fall_mm_per_year'].astype(str)
    df['_source_file']  = df['_source'].astype(str)
    df['_pipeline_run'] = df['_pipeline_run'].astype(str)
    df['_loaded_at']    = pd.to_datetime(df['_ingested_at'], utc=True) 
    insert_cols = [
        'area', 'year', 'average_rain_fall_mm_per_year',
        '_source_file', '_pipeline_run', '_loaded_at'
    ] 
    sql = text('''INSERT INTO bronze.rainfall (
            area, year, average_rain_fall_mm_per_year,
            _source_file, _pipeline_run, _loaded_at
        ) VALUES (
            :area, :year, :average_rain_fall_mm_per_year,
            :_source_file, :_pipeline_run, :_loaded_at
        )''')

    return df, insert_cols, sql


def _prepare_temperature(df: pd.DataFrame):
    df.columns = df.columns.str.strip()
    df['year'] = df['year'].astype(int)
    df['country'] = df['country'].astype(str)
    df['avg_temp'] = pd.to_numeric(df['avg_temp'], errors='coerce')
    df['_source_file']  = df['_source'].astype(str)
    df['_pipeline_run'] = df['_pipeline_run'].astype(str)
    df['_loaded_at']    = pd.to_datetime(df['_ingested_at'], utc=True)

    insert_cols = [
        'year', 'country', 'avg_temp',
        '_source_file', '_pipeline_run', '_loaded_at'
    ]

    sql = text('''INSERT INTO bronze.temperature (
            year, country, avg_temp,
            _source_file, _pipeline_run, _loaded_at
        ) VALUES (
            :year, :country, :avg_temp,
            :_source_file, :_pipeline_run, :_loaded_at
        )''')

    return df, insert_cols, sql


def _prepare_production_coded(df: pd.DataFrame):
    df.columns = df.columns.str.strip()
    df['domain_code'] =  df['Domain Code'].astype(str) 
    df['domain'] = df['Domain'].astype(str)
    df['area_code'] = pd.to_numeric(df['Area Code'], errors='coerce').astype('Int64')
    df['area'] = df['Area'].astype(str)
    df['element_code'] = pd.to_numeric(df['Element Code'], errors='coerce').astype('Int64')
    df['element'] = df['Element'].astype(str)
    df['item_code'] = pd.to_numeric(df['Item Code'], errors='coerce').astype('Int64')
    df['item'] = df['Item'].astype(str)
    df['year_code'] = pd.to_numeric(df['Year Code'], errors='coerce').astype('Int64')
    df['year'] = df['Year'].astype(int)
    df['unit'] = df['Unit'].astype(str)
    df['value'] = pd.to_numeric(df['Value'], errors='coerce')
    df['_source_file']  = df['_source'].astype(str)
    df['_pipeline_run'] = df['_pipeline_run'].astype(str)
    df['_loaded_at']    = pd.to_datetime(df['_ingested_at'], utc=True)

    insert_cols = [
        'domain_code', 'domain', 'area_code', 'area',
        'element_code', 'element', 'item_code', 'item',
        'year_code', 'year', 'unit', 'value',
        '_source_file', '_pipeline_run', '_loaded_at'
    ]

    sql = text('''INSERT INTO bronze.production_coded (
            domain_code, domain, area_code, area,
            element_code, element, item_code, item,
            year_code, year, unit, value,
            _source_file, _pipeline_run, _loaded_at
        ) VALUES (
            :domain_code, :domain, :area_code, :area,
            :element_code, :element, :item_code, :item,
            :year_code, :year, :unit, :value,
            :_source_file, :_pipeline_run, :_loaded_at
        )''')
    # df.to_csv(
    #             f"1111-{datetime.now().microsecond}csv_11.csv",
    #             index=False
    #         )
    return df, insert_cols, sql


def _prepare_crop_analytics(df: pd.DataFrame):
    df.columns = df.columns.str.strip()
    df['area'] = df['Area'].astype(str)
    df['item'] = df['Item'].astype(str)
    df['year'] = df['Year'].astype(int)
    df['hg_per_ha_yield'] = pd.to_numeric(df['hg/ha_yield'], errors='coerce')
    df['average_rain_fall_mm_per_year'] = pd.to_numeric(df['average_rain_fall_mm_per_year'], errors='coerce')
    df['pesticides_tonnes'] = pd.to_numeric(df['pesticides_tonnes'], errors='coerce')
    df['avg_temp'] = pd.to_numeric(df['avg_temp'], errors='coerce')
    df['_source_file']  = df['_source'].astype(str)
    df['_pipeline_run'] = df['_pipeline_run'].astype(str)
    df['_loaded_at']    = pd.to_datetime(df['_ingested_at'], utc=True)

    insert_cols = [
        'area', 'item', 'year', 'hg_per_ha_yield',
        'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp',
        '_source_file', '_pipeline_run', '_loaded_at'
    ]

    sql = text('''INSERT INTO bronze.crop_analytics (
            area, item, year, hg_per_ha_yield,
            average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp,
            _source_file, _pipeline_run, _loaded_at
        ) VALUES (
            :area, :item, :year, :hg_per_ha_yield,
            :average_rain_fall_mm_per_year, :pesticides_tonnes, :avg_temp,
            :_source_file, :_pipeline_run, :_loaded_at
        )''')

    return df, insert_cols, sql


TABLE_PREPARERS = {
    'bronze.production'       : _prepare_production,
    'bronze.rainfall'         : _prepare_rainfall,
    'bronze.temperature'      : _prepare_temperature,
    'bronze.production_coded' : _prepare_production_coded,
    'bronze.crop_analytics'   : _prepare_crop_analytics,
}


def _get_table_config(table: str, df: pd.DataFrame):
    preparer = TABLE_PREPARERS.get(table)
    if preparer is None:
        raise ValueError(
            f"No preparer registered for table: '{table}'. "
            f"Available: {list(TABLE_PREPARERS.keys())}"
        )
    return preparer(df) 

COPY_THRESHOLD_ROWS = 2000


def _copy_insert(df: pd.DataFrame, table: str, insert_cols: list[str], engine) -> int:
 
    buf = io.StringIO()
    writer = csv.writer(buf)
    for row in df[insert_cols].itertuples(index=False, name=None):
        writer.writerow(['' if v is None else v for v in row])
    buf.seek(0)

    schema, table_name = table.split(".", 1)
    cols_sql = ", ".join(insert_cols)

    raw_conn = engine.raw_connection()
    try:
        cur = raw_conn.cursor()
        copy_sql = (
            f'COPY "{schema}"."{table_name}" ({cols_sql}) '
            f"FROM STDIN WITH (FORMAT csv, NULL '')"
        )
        cur.copy_expert(copy_sql, buf)
        raw_conn.commit()
        cur.close()
        return len(df)
    except Exception:
        raw_conn.rollback()
        raise
    finally:
        raw_conn.close()


def insert_dataframe(df: pd.DataFrame, table: str) -> int:
    if df.empty:
        logger.info(f"[{table}] DataFrame is empty, skipping insert.")
        return 0

    start = time.perf_counter()
    try:
        df = df.copy()
        df, insert_cols, sql = _get_table_config(table, df)

        missing = [col for col in insert_cols if col not in df.columns]
        if missing:
            raise ValueError(f"[{table}] DataFrame missing required columns: {missing}")
 
        engine = get_bronze_engine()
        row_count = len(df)
        # df.to_csv(
        #         f"Transform_Rainfall-{datetime.now().microsecond}csv_11.csv",
        #         index=False
        #     )
        if row_count >= COPY_THRESHOLD_ROWS:
            inserted = _copy_insert(df, table, insert_cols, engine)
            method = "COPY"
        else:
            df.to_sql(
                name=table.split(".", 1)[1],
                schema=table.split(".", 1)[0],
                con=engine,
                if_exists='append',
                index=False,
                method='multi',
                chunksize=500,
            )
            inserted = row_count
            method = "to_sql/multi"

        elapsed = time.perf_counter() - start
        logger.info(
            f"[{table}] Inserted {inserted} rows via {method} in {elapsed:.2f}s "
            f"({inserted / elapsed:.0f} rows/sec)" if elapsed > 0 else
            f"[{table}] Inserted {inserted} rows via {method}"
        )
        return inserted

    except ValueError as ve:
        logger.error(f"[insert_dataframe] Validation error: {ve}")
        raise

    except Exception as e:
        logger.error(f"[insert_dataframe] Failed to insert into {table}: {e}")
        raise


def log_pipeline_run(
    run_id: str,
    source_name: str,
    status: str,
    rows_inserted: int | None = None,
    error_message: str | None = None,
    started_at=None,
    finished_at=None,
) -> None:
    engine = get_bronze_engine()

    insert_sql = text("""
        INSERT INTO bronze.pipeline_run_log
            (run_id, source_name, status, rows_inserted, error_message, started_at, finished_at, duration_seconds)
        VALUES
            (:run_id, :source_name, :status, :rows_inserted, :error_message, :started_at, :finished_at, :duration_seconds)
    """)

    duration_seconds = None
    if started_at is not None and finished_at is not None:
        duration_seconds = (finished_at - started_at).total_seconds()

    params = {
        "run_id"           : run_id,
        "source_name"      : source_name,
        "status"           : status,
        "rows_inserted"    : rows_inserted,
        "error_message"    : error_message,
        "started_at"       : started_at,
        "finished_at"      : finished_at,
        "duration_seconds" : duration_seconds,
    }

    try:
        with engine.begin() as conn:
            conn.execute(insert_sql, params)
        logger.info(
            f"[{source_name}] Logged pipeline run {run_id} ({status}) "
            f"in {duration_seconds:.2f}s" if duration_seconds is not None else
            f"[{source_name}] Logged pipeline run {run_id} ({status})"
        )
    except Exception as e:
        logger.error(f"Failed to log pipeline run: {e}")