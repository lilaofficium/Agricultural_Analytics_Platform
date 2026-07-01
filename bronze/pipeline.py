import time
import yaml
import os
from datetime import datetime, timezone
from bronze.extractor import get_excel_data, EXTRACTOR_MAP
from bronze.loader import add_metadata, save_to_bronze
from bronze.insert_query import log_pipeline_run
from utils.logger import get_logger

logger = get_logger("bronze_pipeline")


def run_bronze_pipeline(config_path: str = "config/sources.yaml") -> dict:
    with open(config_path) as f:
        config = yaml.safe_load(f)

    run_id         = os.getenv("PIPELINE_RUN_ID", "local")
    default_format = config.get("default_format", "api")
    results        = {}

    for source_name, cfg in config["sources"].items():
        started_at  = datetime.now(timezone.utc)
        t0          = time.perf_counter()
        try:
            logger.info(f"[{source_name}] Starting ingestion")

            fmt = cfg.get("format", default_format)
            extractor_fn = EXTRACTOR_MAP.get(fmt)
            if extractor_fn is None:
                raise ValueError(
                    f"[{source_name}] Unsupported format: '{fmt}'. "
                    f"Available formats: {list(EXTRACTOR_MAP.keys())}"
                )

            raw_records = extractor_fn(cfg)
            enriched    = add_metadata(raw_records, source_name, run_id)
 
            rows        = save_to_bronze(enriched, source_name, run_id)
            finished_at = datetime.now(timezone.utc)
            elapsed     = time.perf_counter() - t0

            log_pipeline_run(
                run_id=run_id, source_name=source_name, status="success",
                rows_inserted=rows, started_at=started_at, finished_at=finished_at,
            )
            results[source_name] = {"status": "success", "rows": rows, "seconds": round(elapsed, 2)}
            logger.info(f"[{source_name}] Done — {rows} rows inserted in {elapsed:.2f}s")

        except Exception as e:
            finished_at = datetime.now(timezone.utc)
            elapsed     = time.perf_counter() - t0
            logger.error(f"[{source_name}] Failed after {elapsed:.2f}s: {e}")

            log_pipeline_run(
                run_id=run_id, source_name=source_name, status="failed",
                rows_inserted=0, error_message=str(e),
                started_at=started_at, finished_at=finished_at,
            )
            results[source_name] = {"status": "failed", "error": str(e), "seconds": round(elapsed, 2)}

    return results