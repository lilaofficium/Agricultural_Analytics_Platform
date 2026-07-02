import time
from silver.loader import run_silver_source
from silver.rules import SILVER_RULES
from utils.logger import get_logger

logger = get_logger("silver_pipeline")


def run_silver_pipeline(run_id: str | None = None) -> dict:
  
    results = {}
    pipeline_start = time.perf_counter()

    logger.info(f"Silver pipeline starting — {len(SILVER_RULES)} source(s) to process")

    for source_table in SILVER_RULES:
        logger.info(f"[{source_table}] Starting silver processing")

        try:
            result = run_silver_source(source_table, run_id=run_id)
            results[source_table] = result
 
            logger.info(
                f"[{source_table}] Finished — "
                f"{result.get('clean_rows', 0)} clean / "
                f"{result.get('rejected_rows', 0)} rejected "
                f"in {result.get('seconds', 0.0):.2f}s"
            )

        except Exception as e: 
            logger.error(f"[{source_table}] Silver failed: {e}")
            results[source_table] = {
                "source": source_table,
                "status": "failed",
                "error": str(e),
                "seconds": 0.0,
                "clean_rows": 0,
                "rejected_rows": 0,
            }

    total = time.perf_counter() - pipeline_start
    results["__total_seconds__"] = round(total, 2)

    logger.info(f"Silver pipeline finished — total time {total:.2f}s")

    return results