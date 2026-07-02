import pandas as pd
from silver.validator import clean_dataframe,clean_dataframe_acc_column

from utils.logger import get_logger

logger = get_logger("silver.transformer.Rainfall")

def Transform_Rainfall(df: pd.DataFrame, rules: dict) -> tuple[pd.DataFrame, pd.DataFrame]:   
    logger.debug(f"Incoming columns: {list(df.columns)}")
    logger.debug(f"Incoming dtypes:\n{df.dtypes}")
    df=clean_dataframe(df)
    df=clean_dataframe_acc_column(df,'average_rain_fall_mm_per_year','..',None)
    required_columns = ["area", "year", "average_rain_fall_mm_per_year"] 
    df_valid = df[df[required_columns].notna().all(axis=1)].copy() 
    df_rejected = df[df[required_columns].isna().any(axis=1)].copy() 
    logger.debug(f"Split result — {len(df_valid)} valid / {len(df_rejected)} rejected")
    df_valid.columns = df_valid.columns.str.upper()   
    return df_valid,df_rejected

