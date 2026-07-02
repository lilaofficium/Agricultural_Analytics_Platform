import time
import pandas as pd 
import sys
from pathlib import Path
from config.settings import get_settings
from utils.logger import get_logger 
from datetime import datetime, timezone

logger   = get_logger("bronze.extractor")
settings = get_settings()
  

def get_excel_data(cfg: dict) -> pd.DataFrame: 
    df = pd.read_csv(cfg["file_path"]) 
    return df    

 
EXTRACTOR_MAP = { 
    "csv": get_excel_data,
    # "csv":       get_csv_data,
    # "json_file": get_json_file_data,
    # "text":      get_text_data,
}