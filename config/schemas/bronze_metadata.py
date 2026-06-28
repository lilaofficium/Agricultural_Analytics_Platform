BRONZE_METADATA_COLS = {
    "Production": [
        "Domain", "Area", "Element", "Item", "Year", "Unit", "Value"
    ],

    "Rainfall": [
        "Area", "Year", "average_rain_fall_mm_per_year"
    ],

    "Temperature": [
        "year", "country", "avg_temp"
    ],

    "Production_Coded": [           # ← Was "Pesticides"
        "Domain Code", "Domain", "Area Code", "Area",
        "Element Code", "Element", "Item Code", "Item",
        "Year Code", "Year", "Unit", "Value"
    ],

    "Crop_Analytics": [             # ← Was "Final_Dataset"
        "Area", "Item", "Year",
        "hg/ha_yield", "average_rain_fall_mm_per_year",
        "pesticides_tonnes", "avg_temp"
    ]
}