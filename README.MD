# Agricultural Analytics Platform

> An end-to-end ELT data engineering project that consolidates agricultural datasets from multiple independent sources into a unified analytical data warehouse following the Medallion Architecture.

---

## Table of Contents

- [Business Problem](#business-problem)
- [Business Questions Answered](#business-questions-answered)
- [Architecture](#architecture)
- [Medallion Layers](#medallion-layers)
- [Technologies](#technologies)
- [Data Sources](#data-sources)
- [Project Structure](#project-structure)
- [Actual Bronze Execution Flow](#actual-bronze-execution-flow)
- [Data Quality Checks](#data-quality-checks)
- [Development Progress](#development-progress)
- [Future Improvements](#future-improvements)
- [Learning Outcomes](#learning-outcomes)

---

## Business Problem

Agricultural organizations collect data from multiple independent agencies. Crop production statistics, rainfall measurements, temperature records, pesticide usage, and crop yield are stored in separate files with different structures — making analytical reporting difficult.

Without a centralized pipeline, analysts must manually clean and combine these datasets every time a report is needed.

This platform automates the ingestion, validation, transformation, and integration of these datasets into a clean reporting model — eliminating manual effort and enabling consistent, repeatable analysis.

---

## Business Questions Answered

- Which country has the highest crop yield?
- Does rainfall influence crop production?
- Does pesticide usage correlate with yield?
- Which crops perform consistently across years?
- Which regions show declining productivity?
- Which crops perform better under different weather conditions?

---

## Architecture

```
Raw CSV Files (Kaggle)
        ↓
  Bronze Layer          ← Raw ingestion, no transformations
        ↓
  Data Validation       ← Quality checks, integrity validation
        ↓
  Silver Layer          ← Cleaned, standardized, deduplicated
        ↓
Business Transformations
        ↓
   Gold Layer           ← Unified analytical model
        ↓
 Power BI Dashboard     ← Business insights & reporting
```

---

## Medallion Layers

### 🥉 Bronze — Raw Ingestion
Stores raw source data exactly as received from the source files.

- No business transformations applied
- Preserves original source data
- Captures load metadata and timestamps
- Tracks pipeline execution

### 🥈 Silver — Cleaned & Standardized
Applies cleaning and standardization rules to prepare data for analysis.

- Standardizing column names
- Removing duplicate records
- Handling missing values
- Data type conversion
- Data validation and referential integrity checks

### 🥇 Gold — Business-Ready Analytics
Produces the final unified analytical model by joining all five datasets:

| Source | Description |
|--------|-------------|
| Production | Agricultural production statistics |
| Rainfall | Average annual rainfall measurements |
| Temperature | Average yearly temperature |
| Pesticides | Pesticide usage by country |
| Crop Yield | Final analytical measurements |

---

## Technologies

| Category | Tool / Library |
|----------|---------------|
| Language | Python |
| Database | PostgreSQL |
| ORM / DB Driver | SQLAlchemy, psycopg2 |
| Data Processing | Pandas |
| Data Validation | Pydantic |
| Pipeline Pattern | ELT + Medallion Architecture |
| Version Control | Git + GitHub |
| CI/CD | GitHub Actions |
| Visualization *(upcoming)* | Power BI |
| Cloud *(future)* | Databricks, Snowflake |

---

## Data Sources

Datasets sourced from [Kaggle](https://www.kaggle.com/):

| File | Description |
|------|-------------|
| `pesticides.csv` | Pesticide usage by country |
| `rainfall.csv` | Average annual rainfall measurements |
| `temp.csv` | Average yearly temperature |
| `yield.csv` / `yield_df.csv` | Crop yield data |
| *(Production)* | Ingestor exists — file not yet in `storage/bronze/` |

---

## Project Structure

```
agriculture-analytics-platform/
│
├── .github/
│   └── workflow/
│       └── ci.yml                    # GitHub Actions CI pipeline
│
├── .vscode/
│   └── launch.json                   # VS Code debug configuration
│
├── bronze/                           # Bronze layer: raw data ingestion
│   ├── ingestors/                    # Per-source ingestion scripts
│   │   ├── Final_Dataset.py
│   │   ├── Pesticides.py
│   │   ├── Production.py
│   │   ├── Rainfall.py
│   │   └── Temperature.py
│   ├── insert_query.py               # SQL insert utilities
│   └── pipeline.py                   # Bronze pipeline orchestrator
│
├── config/                           # Configuration & schemas
│   ├── schemas/
│   │   └── bronze_metadata.py        # Bronze layer column definitions
│   └── settings.py                   # Project settings (DB credentials, paths, etc.)
│
├── db/
│   └── migrations/
│       └── bronze_tables.sql         # Bronze layer table definitions
│
├── gold/                             # Gold layer (business-ready datasets) — upcoming
│
├── runlayer/                         # Layer execution entry points
│   └── bronzerun.py                  # Bronze layer runner script
│
├── silver/                           # Silver layer (cleaned & standardized) — upcoming
│
├── storage/
│   └── bronze/                       # Raw CSV files (Bronze source data)
│       ├── pesticides.csv
│       ├── rainfall.csv
│       ├── temp.csv
│       ├── yield.csv
│       └── yield_df.csv
│
├── main.py                           # Main application entry point
├── Requirements.txt                  # Python dependencies
├── .gitignore
└── README.md
```
---

## Actual Bronze Execution Flow

This is the verified, code-level trace of what happens on every bronze run, file by file.

1. Entry point — runlayer/bronzerun.py
A PIPELINE_RUN_ID is generated with uuid.uuid4() and set as an environment variable before the pipeline is invoked. It is read by the pipeline, not created inside it. Wall-clock timing starts here via time.perf_counter(), and a per-source summary table is printed after the run completes.
2. bronze/pipeline.py → run_bronze_pipeline()

Opens and parses config/sources.yaml
Reads run_id from the environment (defaults to "local" if unset — e.g. if the function is imported and called directly)
Loops over every entry under sources: in the YAML
For each source, wrapped in try/except:

Resolves the source's format (cfg.get("format", default_format)) and looks up the matching extractor in EXTRACTOR_MAP; raises immediately if the format isn't registered
extractor_fn(cfg) → raw DataFrame
add_metadata(raw_records, source_name, run_id)
save_to_bronze(enriched, source_name, run_id)
log_pipeline_run(...) — recorded on both success and failure, with started_at/finished_at/duration_seconds tracked per source



3. bronze/extractor.py → get_excel_data()

Currently a thin CSV reader: pd.read_csv(cfg["file_path"])
Registered in EXTRACTOR_MAP under the key "csv" — only one format implemented so far; json_file/text extractors are stubbed but commented out
No retry/backoff logic and no pagination handling at this stage (unlike the retail project's API-based extractor) — this pipeline reads flat files, not paginated APIs

4. bronze/loader.py → add_metadata()
Stamps three audit columns onto every row:

_source — the source name from config
_ingested_at — UTC ISO timestamp of ingestion
_pipeline_run — the run_id

5. bronze/loader.py → save_to_bronze()

Resolves the target table from a static TABLE_MAP dict (e.g. rainfall → bronze.rainfall)
Calls ensure_table_exists(table); only proceeds to insert if it returns True
Calls insert_dataframe(df, table) and returns the row count

6. bronze/loader.py → ensure_table_exists()

Checks an in-process _VERIFIED_TABLES cache first — if the table was already confirmed this run/process, returns True immediately without hitting the DB (a force=True flag bypasses this cache)
Checks information_schema.schemata for the schema, creates it with CREATE SCHEMA IF NOT EXISTS if missing
Checks information_schema.tables for the table
If missing, runs the entire db/migrations/bronze_tables.sql migration file (not a single-table CREATE), then re-verifies the table now exists, raising RuntimeError if the migration didn't produce it

7. bronze/insert_query.py → insert_dataframe()

Calls _get_table_config(table, df), which dispatches to a per-table "preparer" function via the TABLE_PREPARERS dict (one function per source: _prepare_production, _prepare_rainfall, _prepare_temperature, _prepare_production_coded, _prepare_crop_analytics)
Each preparer: strips column whitespace, casts/coerces types (pd.to_numeric(..., errors='coerce') for numeric fields, astype(str) for text fields), defines the exact insert_cols list, and builds the parameterized INSERT SQL statement (used only for fallback row-level inserts, not for COPY)
Back in insert_dataframe: validates all insert_cols exist in the DataFrame, replaces NaN with None via .where(pd.notna(...), None)
Branches on row count (COPY_THRESHOLD_ROWS = 2000):

≥2000 rows → _copy_insert(): writes the DataFrame to an in-memory CSV buffer (io.StringIO + csv.writer), then streams it via psycopg2's cur.copy_expert("COPY ... FROM STDIN WITH (FORMAT csv, NULL '')") on a raw connection — explicit commit/rollback/close handled manually, not via engine.begin()
<2000 rows → records_df.to_sql(..., method='multi', chunksize=500) — batched multi-row INSERT, not the parameterized sql object the preparer built (that SQL is currently unused dead code in the hot path, kept for potential row-by-row fallback)


Logs rows/sec throughput for both paths

8. Run logging
Every source's outcome (success or failure) is written to bronze.pipeline_run_log via log_pipeline_run(), including run_id, started_at, finished_at, duration_seconds, row count, and error message if applicable.

config/sources.yaml
        │
        ▼
run_bronze_pipeline()  ──loop per source──▶ get_excel_data()  ──▶  add_metadata()
        │                                                              │
        │                                                              ▼
        │                                                      save_to_bronze()
        │                                                              │
        │                                            ┌─────────────────┴─────────────────┐
        │                                            ▼                                    ▼
        │                                  ensure_table_exists()                 insert_dataframe()
        │                                  (cached in _VERIFIED_TABLES)                    │
        │                                                                                  ▼
        │                                                                       _get_table_config()
        │                                                                        (per-table preparer)
        │                                                                                  │
        │                                                                  ┌───────────────┴───────────────┐
        │                                                                  ▼                                ▼
        │                                                        rows ≥ 2000                       rows < 2000
        │                                                        _copy_insert() (psycopg2 COPY)     to_sql(method='multi')
        ▼
log_pipeline_run()  ◀── success or failure, every source

===== BRONZE PIPELINE SUMMARY =====
production                         4349 rows     8.73s
rainfall                           6727 rows     3.27s
temperature                       71311 rows     6.75s
production_coded                  56717 rows     7.30s
crop_analytics                    28242 rows     4.51s
------------------------------------------------------------
TOTAL                                           36.36s
====================================

---

## Data Quality Checks

The pipeline validates the following at the Silver layer:

- Missing values
- Duplicate records
- Invalid data types
- Primary key uniqueness
- Join consistency across datasets
- Row count validation
- Pipeline execution logs

---

## Development Progress

### ✅ Completed

| Component | Status | Details |
|-----------|--------|---------|
| Data Sourcing | ✅ Done | 5 datasets from Kaggle |
| Project Structure | ✅ Done | Modular folder layout with Bronze/Silver/Gold separation |
| Bronze Pipeline | ✅ Done | `pipeline.py` + `bronzerun.py` runner |
| Bronze Metadata | ✅ Done | `config/schemas/bronze_metadata.py` |
| DB Migrations | ✅ Done | `bronze_tables.sql` for PostgreSQL schema |
| Config Management | ✅ Done | `config/settings.py` for centralized configuration | 
 
