import pandas as pd
from utils.logger import get_logger

logger = get_logger("silver.transformer.Crop_Analytics")
 

def Transform_Crop_Analytics(df: pd.DataFrame, rules: dict) -> tuple[pd.DataFrame, pd.DataFrame]:  
    logger.debug(f"Incoming columns: {list(df.columns)}")
    logger.debug(f"Incoming dtypes:\n{df.dtypes}")

    df = df.drop(columns=["_id"]) 
    df = df.drop(columns=["_loaded_at"])  
    required_columns = ["area", "item", "year", "hg_per_ha_yield"] 
    df_valid = df[df[required_columns].notna().all(axis=1)].copy() 
    df_rejected = df[df[required_columns].isna().any(axis=1)].copy() 
    logger.debug(f"Split result — {len(df_valid)} valid / {len(df_rejected)} rejected")
    df_valid.columns = df_valid.columns.str.upper()   
    return df_valid,df_rejected