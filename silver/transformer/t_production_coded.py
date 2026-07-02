import pandas as pd
from silver.validator import clean_dataframe_acc_column 
from utils.logger import get_logger

logger = get_logger("silver.transformer.Production_Coded")
def Transform_Production_Coded(df: pd.DataFrame, rules: dict) -> tuple[pd.DataFrame, pd.DataFrame]: 
    try : 
        logger.debug(f"Incoming columns: {list(df.columns)}")
        logger.debug(f"Incoming dtypes:\n{df.dtypes}")
        df=clean_dataframe_acc_column(df,'domain_code','<NA>',None)
        required_columns = ["domain_code", "area_code", "element_code", "item_code", "year_code"] 
        df_valid = df[df[required_columns].notna().all(axis=1)].copy() 
        df_rejected = df[df[required_columns].isna().any(axis=1)].copy() 
        logger.debug(f"Split result — {len(df_valid)} valid / {len(df_rejected)} rejected")
        df_valid.columns = df_valid.columns.str.upper()  
        df_rejected.columns = df_rejected.columns.str.upper()
        return df_valid,df_rejected
    except Exception as e :
        logger.error(f"{e}")
       
