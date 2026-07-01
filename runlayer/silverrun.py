import os
import sys
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from silver.pipeline import run_silver_pipeline
 
run_id = os.environ.get("PIPELINE_RUN_ID", None)

if __name__ == "__main__":
    results = run_silver_pipeline(run_id=run_id)
    total   = results.pop("__total_seconds__", 0)

    print("\n===== SILVER PIPELINE SUMMARY =====")
    for source, info in results.items():
        status  = info.get("status", "unknown")
        elapsed = info.get("seconds", 0)
        if status == "success":
            print(
                f"{source:<35} "
                f"in={info['rows_in']:<8} "
                f"clean={info['rows_clean']:<8} "
                f"rejected={info['rows_rejected']:<6} "
                f"{elapsed:>6.2f}s"
            )
            for reason, count in info.get("reject_reasons", {}).items():
                print(f"    └─ {reason}: {count}")
        elif status == "skipped":
            print(f"{source:<35} SKIPPED (no rows)")
        else:
            print(f"{source:<35} FAILED — {info.get('error', '?')}  {elapsed:.2f}s")
    print("-" * 75)
    print(f"{'TOTAL':<35} {total:>6.2f}s")
    print("====================================\n")