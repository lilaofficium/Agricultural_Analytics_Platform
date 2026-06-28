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
 