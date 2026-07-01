import os
import sys
import uuid
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("PIPELINE_RUN_ID", str(uuid.uuid4()))
run_id     = os.environ["PIPELINE_RUN_ID"]
stop_after = os.environ.get("STOP_AFTER", "gold").lower()

print(f"\nPIPELINE RUN: {run_id}")
print(f"STOP AFTER  : {stop_after}\n")

wall = time.perf_counter()

# ── Bronze ────────────────────────────────────────────────────────────────
from bronze.pipeline import run_bronze_pipeline
b_results = run_bronze_pipeline()
b_total = sum(v.get("seconds", 0) for v in b_results.values())
print("\n[Bronze] Done —", {k: v.get("status") for k, v in b_results.items()})

if stop_after == "bronze":
    sys.exit(0)

# ── Silver ────────────────────────────────────────────────────────────────
from silver.pipeline import run_silver_pipeline
s_results = run_silver_pipeline(run_id=run_id)
s_total   = s_results.pop("__total_seconds__", 0)
print("\n[Silver] Done —", {k: v.get("status") for k, v in s_results.items()})

if stop_after == "silver":
    sys.exit(0)

# ── Gold ──────────────────────────────────────────────────────────────────
from gold.pipeline import run_gold_pipeline
g_results = run_gold_pipeline()
g_total   = g_results["total_seconds"]
print(f"\n[Gold] Done — PDF: {g_results['reports'].get('pdf_path')}")

# ── Summary ───────────────────────────────────────────────────────────────
total = time.perf_counter() - wall
print(f"\n{'='*55}")
print(f"  Bronze : {b_total:>6.2f}s")
print(f"  Silver : {s_total:>6.2f}s")
print(f"  Gold   : {g_total:>6.2f}s")
print(f"  TOTAL  : {total:>6.2f}s")
print(f"{'='*55}\n")