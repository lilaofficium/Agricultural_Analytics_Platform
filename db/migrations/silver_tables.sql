CREATE SCHEMA IF NOT EXISTS silver;
CREATE TABLE IF NOT EXISTS silver.production (
    id BIGINT IDENTITY(1, 1) PRIMARY KEY,
    domain TEXT NOT NULL,
    area TEXT NOT NULL,
    element TEXT NOT NULL,
    item TEXT NOT NULL,
    year INTEGER NOT NULL,
    unit TEXT,
    value NUMERIC,
    _source_file TEXT,
    _pipeline_run TEXT,
    _loaded_at TIMESTAMP_TZ,
    _silver_loaded_at TIMESTAMP_TZ
);
CREATE TABLE IF NOT EXISTS silver.production_rejects (
    id BIGINT IDENTITY(1, 1) PRIMARY KEY,
    domain TEXT,
    area TEXT,
    element TEXT,
    item TEXT,
    year INTEGER,
    unit TEXT,
    value NUMERIC,
    _source_file TEXT,
    _pipeline_run TEXT,
    _loaded_at TIMESTAMP_TZ,
    reject_reason TEXT,
    _silver_loaded_at TIMESTAMP_TZ
);
CREATE TABLE IF NOT EXISTS silver.rainfall (
    id BIGINT IDENTITY(1, 1) PRIMARY KEY,
    area TEXT NOT NULL,
    year INTEGER NOT NULL,
    average_rain_fall_mm_per_year NUMERIC,
    _source_file TEXT,
    _pipeline_run TEXT,
    _loaded_at TIMESTAMP_TZ,
    _silver_loaded_at TIMESTAMP_TZ
);
CREATE TABLE IF NOT EXISTS silver.rainfall_rejects (
    id BIGINT IDENTITY(1, 1) PRIMARY KEY,
    area TEXT,
    year INTEGER,
    average_rain_fall_mm_per_year NUMERIC,
    _source_file TEXT,
    _pipeline_run TEXT,
    _loaded_at TIMESTAMP_TZ,
    reject_reason TEXT,
    _silver_loaded_at TIMESTAMP_TZ
);
CREATE TABLE IF NOT EXISTS silver.temperature (
    id BIGINT IDENTITY(1, 1) PRIMARY KEY,
    year INTEGER NOT NULL,
    country TEXT NOT NULL,
    avg_temp NUMERIC,
    _source_file TEXT,
    _pipeline_run TEXT,
    _loaded_at TIMESTAMP_TZ,
    _silver_loaded_at TIMESTAMP_TZ
);
CREATE TABLE IF NOT EXISTS silver.temperature_rejects (
    id BIGINT IDENTITY(1, 1) PRIMARY KEY,
    year INTEGER,
    country TEXT,
    avg_temp NUMERIC,
    _source_file TEXT,
    _pipeline_run TEXT,
    _loaded_at TIMESTAMP_TZ,
    reject_reason TEXT,
    _silver_loaded_at TIMESTAMP_TZ
);
CREATE TABLE IF NOT EXISTS silver.production_coded (
    id BIGINT IDENTITY(1, 1) PRIMARY KEY,
    domain_code INTEGER,
    domain TEXT,
    area_code INTEGER,
    area TEXT,
    element_code INTEGER,
    element TEXT,
    item_code INTEGER,
    item TEXT,
    year_code INTEGER,
    year INTEGER NOT NULL,
    unit TEXT,
    value NUMERIC,
    _source_file TEXT,
    _pipeline_run TEXT,
    _loaded_at TIMESTAMP_TZ,
    _silver_loaded_at TIMESTAMP_TZ
);
CREATE TABLE IF NOT EXISTS silver.production_coded_rejects (
    id BIGINT IDENTITY(1, 1) PRIMARY KEY,
    domain_code INTEGER,
    domain TEXT,
    area_code INTEGER,
    area TEXT,
    element_code INTEGER,
    element TEXT,
    item_code INTEGER,
    item TEXT,
    year_code INTEGER,
    year INTEGER,
    unit TEXT,
    value NUMERIC,
    _source_file TEXT,
    _pipeline_run TEXT,
    _loaded_at TIMESTAMP_TZ,
    reject_reason TEXT,
    _silver_loaded_at TIMESTAMP_TZ
);
CREATE TABLE IF NOT EXISTS silver.crop_analytics (
    id BIGINT IDENTITY(1, 1) PRIMARY KEY,
    area TEXT NOT NULL,
    item TEXT NOT NULL,
    year INTEGER NOT NULL,
    hg_per_ha_yield NUMERIC,
    average_rain_fall_mm_per_year NUMERIC,
    pesticides_tonnes NUMERIC,
    avg_temp NUMERIC,
    _source_file TEXT,
    _pipeline_run TEXT,
    _loaded_at TIMESTAMP_TZ,
    _silver_loaded_at TIMESTAMP_TZ
);
CREATE TABLE IF NOT EXISTS silver.crop_analytics_rejects (
    id BIGINT IDENTITY(1, 1) PRIMARY KEY,
    area TEXT,
    item TEXT,
    year INTEGER,
    hg_per_ha_yield NUMERIC,
    average_rain_fall_mm_per_year NUMERIC,
    pesticides_tonnes NUMERIC,
    avg_temp NUMERIC,
    _source_file TEXT,
    _pipeline_run TEXT,
    _loaded_at TIMESTAMP_TZ,
    reject_reason TEXT,
    _silver_loaded_at TIMESTAMP_TZ
);