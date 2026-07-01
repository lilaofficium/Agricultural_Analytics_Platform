import time
from silver.loader import run_silver_source
from silver.rules import SILVER_RULES
from utils.logger import get_logger

logger = get_logger("silver_pipeline")


def run_silver_pipeline(run_id: str | None = None) -> dict: 

    results = {}
    pipeline_start = time.perf_counter()

    for source_table in SILVER_RULES:
        try:
            result = run_silver_source(source_table, run_id=run_id)
            results[source_table] = result
        except Exception as e:
            logger.error(f"[{source_table}] Silver failed: {e}")
            results[source_table] = {
                "source": source_table, "status": "failed",
                "error": str(e), "seconds": 0.0
            }

    total = time.perf_counter() - pipeline_start
    results["__total_seconds__"] = round(total, 2)
    return results