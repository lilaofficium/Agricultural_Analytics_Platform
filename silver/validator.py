import pandas as pd
import numpy as np
from datetime import datetime, timezone
from utils.logger import get_logger

logger = get_logger("silver.validator")


def _convert_type(series: pd.Series, dtype: str) -> tuple[pd.Series, pd.Series]:
   
    original_null = series.isna() 
    if dtype == "int":
        converted = pd.to_numeric(series, errors="coerce")
        # int needs whole numbers; non-integer floats are a conversion failure
        non_integer = converted.notna() & (converted % 1 != 0)
        converted = converted.where(~non_integer)
        converted = converted.astype("Int64")
    elif dtype == "float":
        converted = pd.to_numeric(series, errors="coerce")
    elif dtype == "str":
        converted = series.astype(str).str.strip()
        converted = converted.replace({"nan": np.nan, "None": np.nan, "": np.nan})
    elif dtype == "date":
        converted = pd.to_datetime(series, errors="coerce", utc=True)
    else:
        raise ValueError(f"Unsupported dtype '{dtype}' in rules config")

    failed_mask = converted.isna() & ~original_null
    return converted, failed_mask
 


def clean_dataframe(df): 
    try: 
        DEBUG_DUMP_INPUT = False
        if DEBUG_DUMP_INPUT:
            debug_path = f"Transform_Rainfall-{datetime.now().microsecond}.csv"
            # df.to_csv(debug_path, index=False)
            logger.debug(f"Wrote pre-clean debug dump to {debug_path}")
 
        task_array = ['nan', '']
 
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].replace(task_array, 0)
                df[col] = df[col].fillna(0)
            else:
                df[col] = df[col].replace(task_array, pd.NA)
 
        logger.debug(f"clean_dataframe: normalized {len(df.columns)} column(s), {len(df)} row(s)")
        return df
 
    except Exception as e:
        logger.error(f"clean_dataframe failed: {e}")
 
 
def clean_dataframe_acc_column(df, colname, toreplace, withreplace):
    
    try:
        df[colname] = df[colname].replace(toreplace, withreplace)
        logger.debug(f"clean_dataframe_acc_column: replaced values in '{colname}'")
    except Exception as e:
        logger.error(f"clean_dataframe_acc_column failed on column '{colname}': {e}")
    return df