import pandas as pd
from utils.logger import get_logger

logger = get_logger("silver.transformer.production")


def Transform_Production(df: pd.DataFrame, rules: dict) -> tuple[pd.DataFrame, pd.DataFrame]: 
    logger.debug(f"Incoming columns: {list(df.columns)}")
    logger.debug(f"Incoming dtypes:\n{df.dtypes}")
 
    df = df.drop(columns=["_id"])
    df = df.drop(columns=["_loaded_at"])

    required_columns = ["domain", "area", "element", "item", "year", "value"]
 
    df_valid = df[df[required_columns].notna().all(axis=1)].copy()
    df_rejected = df[df[required_columns].isna().any(axis=1)].copy()

    logger.debug(f"Split result — {len(df_valid)} valid / {len(df_rejected)} rejected")
 
    df_valid.columns = df_valid.columns.str.upper()
    df_valid["DOMAIN"] = df_valid["DOMAIN"].str.upper()
    df_valid["AREA"] = df_valid["AREA"].str.upper()
    df_valid["ELEMENT"] = df_valid["ELEMENT"].str.upper()
    df_valid["ITEM"] = df_valid["ITEM"].str.upper()
    df_valid["UNIT"] = df_valid["UNIT"].str.upper()

    df_rejected.columns = df_rejected.columns.str.upper()
    df_rejected["DOMAIN"] = df_rejected["DOMAIN"].str.upper()
    df_rejected["AREA"] = df_rejected["AREA"].str.upper()
    df_rejected["ELEMENT"] = df_rejected["ELEMENT"].str.upper()
    df_rejected["ITEM"] = df_rejected["ITEM"].str.upper()
    df_rejected["UNIT"] = df_rejected["UNIT"].str.upper()

    return df_valid, df_rejected