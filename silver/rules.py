
SILVER_RULES = {
    "bronze.production": {
        "target_table": "SILVER.PRODUCTION",
        "reject_table": "silver.production_rejects",
        "dedup_keys":   ["domain", "area", "element", "item", "year"],
        "dtypes": {
            "domain": "str", "area": "str", "element": "str", "item": "str",
            "year": "int", "unit": "str", "value": "float",
        },
        "not_null": ["domain", "area", "element", "item", "year", "value"],
        "ranges": {
            "year": (1900, 2100),
            "value": (0, None),
        },
        "allowed_values": {},
    }
    ,

    "bronze.rainfall": {
        "target_table": "silver.rainfall",
        "reject_table": "silver.rainfall_rejects",
        "dedup_keys":   ["area", "year"],
        "dtypes": {
            "area": "str", "year": "int",
            "average_rain_fall_mm_per_year": "float",
        },
        "not_null": ["area", "year", "average_rain_fall_mm_per_year"],
        "ranges": {
            "year": (1900, 2100),
            "average_rain_fall_mm_per_year": (0, None),
        },
        "allowed_values": {},
    },

    "bronze.temperature": {
        "target_table": "silver.temperature",
        "reject_table": "silver.temperature_rejects",
        "dedup_keys":   ["country", "year"],
        "dtypes": {
            "year": "int", "country": "str", "avg_temp": "float",
        },
        "not_null": ["year", "country", "avg_temp"],
        "ranges": {
            "year": (1900, 2100),
            "avg_temp": (-90, 60),
        },
        "allowed_values": {},
    }, 
    "bronze.production_coded": {
        "target_table": "silver.production_coded",
        "reject_table": "silver.production_coded_rejects",
        "dedup_keys":   ["domain_code", "area_code", "element_code", "item_code", "year_code"],
        "dtypes": {
            "domain_code": "int", "domain": "str",
            "area_code": "int", "area": "str",
            "element_code": "int", "element": "str",
            "item_code": "int", "item": "str",
            "year_code": "int", "year": "int",
            "unit": "str", "value": "float",
        },
        "not_null": ["domain_code", "area_code", "item_code", "year", "value"],
        "ranges": {
            "year": (1900, 2100),
            "value": (0, None),
        },
        "allowed_values": {},
    }, 
    "bronze.crop_analytics": {
        "target_table": "silver.crop_analytics",
        "reject_table": "silver.crop_analytics_rejects",
        "dedup_keys":   ["area", "item", "year"],
        "dtypes": {
            "area": "str", "item": "str", "year": "int",
            "hg_per_ha_yield": "float",
            "average_rain_fall_mm_per_year": "float",
            "pesticides_tonnes": "float",
            "avg_temp": "float",
        },
        "not_null": ["area", "item", "year", "hg_per_ha_yield"],
        "ranges": {
            "year": (1900, 2100),
            "hg_per_ha_yield": (0, None),
            "average_rain_fall_mm_per_year": (0, None),
            "pesticides_tonnes": (0, None),
            "avg_temp": (-90, 60),
        },
        "allowed_values": {},
    }, 
}