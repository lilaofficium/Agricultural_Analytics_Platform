import pandas as pd
import numpy as np
from utils.logger import get_logger

logger = get_logger("silver.validator")


def _convert_type(series: pd.Series, dtype: str) -> tuple[pd.Series, pd.Series]: 
    original_null = series.isna()

    if dtype == "int":
        converted = pd.to_numeric(series, errors="coerce") 
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

