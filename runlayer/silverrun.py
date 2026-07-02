import os
import sys
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from silver.pipeline import run_silver_pipeline
from utils.logger import get_logger

logger = get_logger("silver_run")
 
run_id = os.environ.get("PIPELINE_RUN_ID", None)


def _print_summary(results: dict, total: float) -> None: 
    print("===== SILVER PIPELINE SUMMARY =====")

    for source_table, result in results.items(): 
        if source_table == "__total_seconds__":
            continue
 
        display_name = source_table.split(".", 1)[-1]

        status = result.get("status", "unknown")

        if status == "failed": 
            print(f"{display_name:<35}{'FAILED':>10}    {result.get('error', '')}")
            continue

        rows = result.get("clean_rows", 0)
        seconds = result.get("seconds", 0.0)
        print(f"{display_name:<35}{rows:>6} rows{seconds:>8.2f}s")

    print("-" * 60)
    print(f"{'TOTAL':<49}{total:>8.2f}s")
    print("====================================\n")


if __name__ == "__main__":
    logger.info(f"Starting silver pipeline run (run_id={run_id})")

    results = run_silver_pipeline(run_id=run_id)
 
    total = results.pop("__total_seconds__", 0)

    _print_summary(results, total)

    logger.info(f"Silver pipeline run complete in {total:.2f}s")