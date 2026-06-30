CREATE SCHEMA IF NOT EXISTS bronze;
CREATE TABLE IF NOT EXISTS bronze.production (
    domain TEXT,
    area TEXT,
    element TEXT,
    item TEXT,
    year INTEGER,
    unit TEXT,
    value NUMERIC(18, 6),
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _source_file TEXT,
    _id SERIAL PRIMARY KEY,
    _pipeline_run TEXT
);
CREATE TABLE IF NOT EXISTS bronze.rainfall (
    area TEXT,
    year TEXT,
    average_rain_fall_mm_per_year TEXT,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _source_file TEXT,
    _id SERIAL PRIMARY KEY,
    _pipeline_run TEXT
);
CREATE TABLE IF NOT EXISTS bronze.temperature (
    year INTEGER,
    country TEXT,
    avg_temp NUMERIC(18, 6),
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _source_file TEXT,
    _id SERIAL PRIMARY KEY,
    _pipeline_run TEXT
);
CREATE TABLE IF NOT EXISTS bronze.production_coded (
    domain_code TEXT,
    domain TEXT,
    area_code TEXT,
    area TEXT,
    element_code TEXT,
    element TEXT,
    item_code TEXT,
    item TEXT,
    year_code TEXT,
    year TEXT,
    unit TEXT,
    value TEXT,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _source_file TEXT,
    _id SERIAL PRIMARY KEY,
    _pipeline_run TEXT
);
CREATE TABLE IF NOT EXISTS bronze.crop_analytics (
    area TEXT,
    item TEXT,
    year TEXT,
    hg_per_ha_yield TEXT,
    average_rain_fall_mm_per_year TEXT,
    pesticides_tonnes TEXT,
    avg_temp TEXT,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _source_file TEXT,
    _id SERIAL PRIMARY KEY,
    _pipeline_run TEXT
);
CREATE TABLE IF NOT EXISTS bronze.pipeline_run_log (
    run_id VARCHAR(50),
    source_name VARCHAR(100),
    status VARCHAR(20),
    -- success | failed
    rows_inserted INTEGER,
    error_message TEXT,
    started_at TIMESTAMP WITH TIME ZONE,
    finished_at TIMESTAMP WITH TIME ZONE
);
CREATE INDEX IF NOT EXISTS idx_production_area ON bronze.production(area);
CREATE INDEX IF NOT EXISTS idx_production_item ON bronze.production(item);
CREATE INDEX IF NOT EXISTS idx_production_year ON bronze.production(year);
CREATE INDEX IF NOT EXISTS idx_rainfall_area ON bronze.rainfall(area);
CREATE INDEX IF NOT EXISTS idx_rainfall_year ON bronze.rainfall(year);
CREATE INDEX IF NOT EXISTS idx_temperature_country ON bronze.temperature(country);
CREATE INDEX IF NOT EXISTS idx_temperature_year ON bronze.temperature(year);
CREATE INDEX IF NOT EXISTS idx_production_coded_area_code ON bronze.production_coded(area_code);
CREATE INDEX IF NOT EXISTS idx_production_coded_item_code ON bronze.production_coded(item_code);
CREATE INDEX IF NOT EXISTS idx_production_coded_year ON bronze.production_coded(year);
CREATE INDEX IF NOT EXISTS idx_crop_analytics_area ON bronze.crop_analytics(area);
CREATE INDEX IF NOT EXISTS idx_crop_analytics_item ON bronze.crop_analytics(item);
CREATE INDEX IF NOT EXISTS idx_crop_analytics_year ON bronze.crop_analytics(year);