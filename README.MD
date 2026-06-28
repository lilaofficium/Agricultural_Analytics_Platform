�
� Agricultural Analytics Platform
Overview
The Agricultural Analytics Platform is an end-to-end ELT data engineering project designed to consolidate
agricultural datasets from multiple independent sources into a unified analytical data warehouse.
The project simulates a real-world scenario where different departments publish data independently.
Production statistics, weather information, pesticide usage, and crop yield are stored in separate files with
different structures, making analytical reporting difficult.
This platform automates the ingestion, validation, transformation, and integration of these datasets into a
clean reporting model following the Medallion Architecture (Bronze → Silver → Gold).