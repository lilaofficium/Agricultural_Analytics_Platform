from db.connection import get_bronze_engine, get_bronze_connection
from sqlalchemy import text 
import json
import uuid
from pathlib import Path
import pandas as pd
from utils.logger import get_logger 
import numpy as np

logger = get_logger("bronze.insert_query")

def _prepare_production(df: pd.DataFrame):
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
    print(df.columns.tolist())
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
    df['domain_code'] = pd.to_numeric(df['Domain Code'], errors='coerce').astype('Int64')
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

    return df, insert_cols, sql


def _prepare_crop_analytics(df: pd.DataFrame):
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
    'bronze.crop_analytics'   : _prepare_crop_analytics 
}


def _get_table_config(table: str, df: pd.DataFrame):
    preparer = TABLE_PREPARERS.get(table)
    if preparer is None:
        raise ValueError(
            f"No preparer registered for table: '{table}'. "
            f"Available: {list(TABLE_PREPARERS.keys())}"
        ) 
    return preparer(df)
 

def insert_dataframe(df: pd.DataFrame, table: str) -> int:
    if df.empty:
        logger.info(f"[{table}] DataFrame is empty, skipping insert.")
        return 0
 
    try:
        df = df.copy()
        df, insert_cols, sql = _get_table_config(table, df)
 
        missing = [col for col in insert_cols if col not in df.columns]
        if missing:
            raise ValueError(f"[{table}] DataFrame missing required columns: {missing}") 
 
        records = (
            df[insert_cols]
            .where(pd.notna(df[insert_cols]), None)
            .to_dict(orient="records")
        )
        clean_records = []
        for rec in records:
            clean_rec = {}
            for k, v in rec.items():
                if isinstance(v, (np.integer, np.floating)):
                    clean_rec[k] = v.item() if not pd.isna(v) else None
                elif isinstance(v, float) and np.isnan(v):
                    clean_rec[k] = None
                else:
                    clean_rec[k] = v
            clean_records.append(clean_rec)
        # getting data upto here clean_records= 4000 above no it has only 7 column but executing this taking long time conn.execute(sql, clean_records)  want to trace the reason why it is hapenning
        engine = get_bronze_engine()
        with engine.begin() as conn:
            conn.execute(sql, clean_records)
 
        logger.info(f"[{table}] Inserted {len(records)} rows.")
        return len(records)
 
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
            (run_id, source_name, status, rows_inserted, error_message, started_at, finished_at)
        VALUES
            (:run_id, :source_name, :status, :rows_inserted, :error_message, :started_at, :finished_at)
    """)
 
    params = {
        "run_id"        : run_id,
        "source_name"   : source_name,
        "status"        : status,
        "rows_inserted" : rows_inserted,
        "error_message" : error_message,
        "started_at"    : started_at,
        "finished_at"   : finished_at,
    }
 
    try:
        with engine.begin() as conn:
            conn.execute(insert_sql, params)
        logger.info(f"[{source_name}] Logged pipeline run {run_id} ({status})")
    except Exception as e:
        logger.error(f"Failed to log pipeline run: {e}")