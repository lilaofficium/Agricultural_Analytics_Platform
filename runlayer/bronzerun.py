import uuid
import os
import sys 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
from bronze.pipeline import run_bronze_pipeline

os.environ["PIPELINE_RUN_ID"] = str(uuid.uuid4())

if __name__ == "__main__":
    results = run_bronze_pipeline()

    print("\n===== BRONZE PIPELINE SUMMARY =====")
    for source, info in results.items():
        status = info.get("status", "unknown")
        if status == "success":
            print(f"{source:<30} {info.get('rows', 0)} rows inserted")
        else:
            print(f"{source:<30} FAILED — {info.get('error', 'unknown error')}")
    print("====================================\n")