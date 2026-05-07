# =============================================================================
# PHARMACY DATA MART EXAMPLE
# =============================================================================
#
# DEFINITION:
# A pharmacy data mart is a centralized, analytics-ready dataset that stores
# normalized pharmacy and medication-related information for reporting,
# operational analytics, and machine learning use cases.
#
# BUSINESS PURPOSE:
# Used by healthcare organizations, payers, PBMs, and analytics teams for:
#
# - medication adherence tracking
# - refill analytics
# - specialty drug monitoring
# - utilization trend analysis
# - formulary optimization
# - risk stratification
# - population health analytics
#
# COMMON SOURCE SYSTEMS:
#
# PBM Systems (Pharmacy Benefit Managers)
# -> organizations that manage prescription drug benefits
# -> examples: CVS Caremark, Express Scripts, OptumRx
#
# Pharmacy Claims
# -> records generated when prescriptions are billed through insurance
#
# NDC Datasets
# -> National Drug Code reference datasets for drug identification
#
# Rx Dispensing Feeds
# -> pharmacy transaction feeds showing medication fills/refills
#
# =============================================================================

import pandas as pd


# =============================================================================
# CREATE SAMPLE PHARMACY DATA MART
# =============================================================================

pharmacy_data_mart = pd.DataFrame({

    # -------------------------------------------------------------------------
    # patient_id
    # -------------------------------------------------------------------------
    #
    # Unique patient identifier used to link records across:
    # - claims systems
    # - EHRs
    # - pharmacy systems
    # - care management platforms
    #
    # Typically de-identified in analytics environments.
    #
    # -------------------------------------------------------------------------
    "patient_id": [1001, 1002, 1003],


    # -------------------------------------------------------------------------
    # ndc_code
    # -------------------------------------------------------------------------
    #
    # National Drug Code (NDC)
    #
    # Standardized FDA drug identifier used to uniquely identify:
    # - manufacturer
    # - product
    # - package size
    #
    # Example:
    # 0074-4339-02
    #
    # Structure:
    # - Labeler code
    # - Product code
    # - Package code
    #
    # Used heavily in:
    # - pharmacy claims
    # - reimbursement systems
    # - formulary management
    #
    # -------------------------------------------------------------------------
    "ndc_code": [
        "0074-4339-02",
        "57894-030-01",
        "0009-0056-01"
    ],


    # -------------------------------------------------------------------------
    # rxnorm_code
    # -------------------------------------------------------------------------
    #
    # RxNorm normalized medication identifier
    #
    # Developed by:
    # National Library of Medicine (NLM)
    #
    # Purpose:
    # Standardizes medication names across different healthcare systems.
    #
    # Example:
    # Multiple versions of:
    # - Humira
    # - Adalimumab
    # - Adalimumab Pen Injector
    #
    # can all map to a single RxNorm concept.
    #
    # Used for:
    # - interoperability
    # - clinical decision support
    # - medication normalization
    #
    # -------------------------------------------------------------------------
    "rxnorm_code": [
        "327361",
        "191831",
        "8640"
    ],


    # -------------------------------------------------------------------------
    # drug_name
    # -------------------------------------------------------------------------
    #
    # Human-readable medication name.
    #
    # Examples:
    # - Adalimumab
    # - Prednisone
    # - Infliximab
    #
    # Often derived from:
    # - RxNorm mappings
    # - NDC reference tables
    #
    # Used for:
    # - reporting
    # - dashboards
    # - provider-facing analytics
    #
    # -------------------------------------------------------------------------
    "drug_name": [
        "Adalimumab",
        "Infliximab",
        "Prednisone"
    ],


    # -------------------------------------------------------------------------
    # fill_date
    # -------------------------------------------------------------------------
    #
    # Date medication prescription was filled by pharmacy.
    #
    # Important for:
    # - adherence tracking
    # - refill gap analysis
    # - longitudinal medication history
    #
    # Example use case:
    # Detecting patients overdue for biologic therapy refills.
    #
    # -------------------------------------------------------------------------
    "fill_date": [
        "2026-01-12",
        "2026-01-15",
        "2026-01-18"
    ],


    # -------------------------------------------------------------------------
    # days_supply
    # -------------------------------------------------------------------------
    #
    # Number of days medication is expected to last.
    #
    # Examples:
    # - 30-day supply
    # - 90-day supply
    #
    # Used heavily in:
    # - medication adherence metrics
    # - proportion of days covered (PDC)
    # - refill compliance analysis
    #
    # Example:
    # 30 = prescription should last approximately 30 days
    #
    # -------------------------------------------------------------------------
    "days_supply": [
        30,
        56,
        14
    ],


    # -------------------------------------------------------------------------
    # quantity_dispensed
    # -------------------------------------------------------------------------
    #
    # Amount of medication dispensed to patient.
    #
    # Depends on medication type:
    # - tablet count
    # - injection pens
    # - vials
    #
    # Used for:
    # - utilization analysis
    # - specialty drug monitoring
    # - inventory analytics
    #
    # Example:
    # 14 tablets
    # 2 injection pens
    #
    # -------------------------------------------------------------------------
    "quantity_dispensed": [
        2,
        1,
        14
    ],


    # -------------------------------------------------------------------------
    # pharmacy_npi
    # -------------------------------------------------------------------------
    #
    # National Provider Identifier (NPI)
    #
    # Unique identifier assigned to healthcare providers and organizations.
    #
    # In pharmacy datasets:
    # identifies dispensing pharmacy/provider.
    #
    # Used for:
    # - provider attribution
    # - network analytics
    # - pharmacy performance analysis
    #
    # -------------------------------------------------------------------------
    "pharmacy_npi": [
        "1234567890",
        "2234567890",
        "3234567890"
    ]
})


# =============================================================================
# DISPLAY DATA MART
# =============================================================================

print(pharmacy_data_mart)
