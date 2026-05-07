# =============================================================================
# PHARMACY DATA MART EXAMPLE
# =============================================================================
#
# PURPOSE:
# Centralized analytics-ready pharmacy dataset used for:
#
# - medication adherence tracking
# - refill analytics
# - utilization trends
# - specialty drug monitoring
# - payer analytics
#
# Typically built from:
# - PBM systems
# - pharmacy claims
# - NDC datasets
# - Rx dispensing feeds
#
# =============================================================================

pharmacy_data_mart = pd.DataFrame({

    "patient_id": [1001, 1002, 1003],

    "ndc_code": [
        "0074-4339-02",
        "57894-030-01",
        "0009-0056-01"
    ],

    "rxnorm_code": [
        "327361",
        "191831",
        "8640"
    ],

    "drug_name": [
        "Adalimumab",
        "Infliximab",
        "Prednisone"
    ],

    "fill_date": [
        "2026-01-12",
        "2026-01-15",
        "2026-01-18"
    ],

    "days_supply": [
        30,
        56,
        14
    ],

    "quantity_dispensed": [
        2,
        1,
        14
    ],

    "pharmacy_npi": [
        "1234567890",
        "2234567890",
        "3234567890"
    ]
})

print(pharmacy_data_mart)
