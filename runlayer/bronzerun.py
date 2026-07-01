import uuid
import os
import sys
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bronze.pipeline import run_bronze_pipeline

os.environ["PIPELINE_RUN_ID"] = str(uuid.uuid4())

if __name__ == "__main__":
    pipeline_start = time.perf_counter()
    results = run_bronze_pipeline()
    total_elapsed = time.perf_counter() - pipeline_start

    print("\n===== BRONZE PIPELINE SUMMARY =====")
    for source, info in results.items():
        status   = info.get("status", "unknown")
        duration = info.get("seconds", 0)
        if status == "success":
            print(f"{source:<30} {info.get('rows', 0):>8} rows   {duration:>6.2f}s")
        else:
            print(f"{source:<30} FAILED — {info.get('error', 'unknown error')}   {duration:>6.2f}s")
    print("-" * 60)
    print(f"{'TOTAL':<30} {'':>8}        {total_elapsed:>6.2f}s")
    print("====================================\n")