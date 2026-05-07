# =============================================================================
# CROHN'S DISEASE PREDICTION MODEL USING XGBOOST
# =============================================================================
#
# PURPOSE:
# This example demonstrates how a healthcare analytics team could build a
# machine learning model to identify patients at high risk for Crohn's disease
# using clinical claims data.
#
# BUSINESS VALUE:
# - Detect potentially undiagnosed patients earlier
# - Improve care management outreach
# - Reduce delays in diagnosis
# - Support population health analytics
#
# HEALTHCARE DATA DOMAINS USED:
# - ICD-10-CM diagnosis codes
# - CPT/HCPCS procedure codes
# - RxNorm / NDC medication data
# - LOINC laboratory data
# - Patient normalization and feature engineering
#
# MODEL:
# XGBoost binary classification model
#
# NOTE:
# This uses synthetic/sample data for demonstration purposes only.
# No PHI or real patient data is included.
#
# =============================================================================


# =============================================================================
# IMPORT REQUIRED LIBRARIES
# =============================================================================

# pandas -> data manipulation and tabular processing
import pandas as pd

# numpy -> numerical operations
import numpy as np

# XGBoost model used for prediction
from xgboost import XGBClassifier

# Train/test splitting utility
from sklearn.model_selection import train_test_split

# Model evaluation metrics
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    confusion_matrix
)

# Converts categorical text into machine-readable numeric values
from sklearn.preprocessing import LabelEncoder


# =============================================================================
# STEP 1 — LOAD / CREATE CLINICAL CLAIMS DATA
# =============================================================================
#
# In a real healthcare environment, this data could come from:
# - Claims warehouses
# - EHR systems
# - Snowflake / BigQuery / Redshift
# - FHIR APIs
# - HL7 integrations
#
# Each row below represents a patient encounter or aggregated patient profile.
#
# =============================================================================

claims_df = pd.DataFrame({

    # Unique patient identifier
    "patient_id": range(1, 21),

    # ICD-10 diagnosis codes
    # Examples:
    # K50 = Crohn's disease
    # R10 = abdominal pain
    # R19 = diarrhea symptoms
    "primary_icd10": [
        "K52.9", "R10.9", "K50.90", "R19.7", "K58.9",
        "R63.4", "K50.10", "K21.9", "R10.84", "K52.9",
        "K50.90", "R19.7", "K59.1", "R10.9", "K50.10",
        "R63.4", "K58.9", "K21.9", "R19.7", "K50.90"
    ],

    # CPT/HCPCS procedure codes
    # Examples:
    # 45378 = colonoscopy
    # 85025 = CBC lab test
    "procedure_code": [
        "45378", "99213", "74177", "45380", "99214",
        "85025", "45385", "99213", "80053", "45378",
        "74177", "85025", "99214", "80053", "45385",
        "45380", "99213", "85025", "74177", "45378"
    ],

    # Medication names that could be mapped from:
    # - RxNorm
    # - NDC
    # - pharmacy claims
    "medication": [
        "Prednisone", "Omeprazole", "Adalimumab", "Mesalamine",
        "Loperamide", "Prednisone", "Infliximab", "Omeprazole",
        "Dicyclomine", "Mesalamine", "Adalimumab", "Prednisone",
        "Loperamide", "Dicyclomine", "Infliximab", "Mesalamine",
        "Omeprazole", "Prednisone", "Mesalamine", "Adalimumab"
    ],

    # Example inflammatory marker (LOINC-based lab)
    # Elevated CRP is commonly associated with inflammation
    "crp_level": [
        1.2, 0.8, 8.5, 5.1, 0.9,
        4.2, 9.1, 0.5, 2.1, 3.5,
        7.8, 6.1, 1.0, 2.3, 8.7,
        5.9, 0.7, 3.1, 4.8, 9.4
    ],

    # Hemoglobin lab values
    # Low hemoglobin may indicate GI bleeding or chronic inflammation
    "hemoglobin": [
        14.2, 13.9, 10.5, 11.8, 14.1,
        12.2, 9.8, 15.1, 13.4, 12.8,
        10.1, 11.3, 14.5, 13.1, 9.7,
        11.0, 14.7, 12.5, 11.9, 10.2
    ],

    # Target variable
    # 1 = patient diagnosed with Crohn's disease
    # 0 = patient not diagnosed
    "crohns_diagnosis": [
        0, 0, 1, 1, 0,
        0, 1, 0, 0, 0,
        1, 1, 0, 0, 1,
        1, 0, 0, 1, 1
    ]
})


# Display sample data
print("===== SAMPLE CLAIMS DATA =====")
print(claims_df.head())


# =============================================================================
# STEP 2 — CLINICAL DATA NORMALIZATION
# =============================================================================
#
# PURPOSE:
# Healthcare data is often messy and inconsistent.
#
# This section standardizes:
# - ICD-10 categories
# - medication classes
#
# This improves model interpretability and reduces noise.
#
# =============================================================================


# -----------------------------------------------------------------------------
# ICD-10 CATEGORY NORMALIZATION
# -----------------------------------------------------------------------------
#
# Groups diagnosis codes into broader symptom/disease categories.
#
# Example:
# K50.* -> Crohn's disease
# R10.* -> Abdominal pain
#
# -----------------------------------------------------------------------------

def categorize_icd10(code):

    # Crohn's disease ICD family
    if code.startswith("K50"):
        return "Crohns"

    # Abdominal pain symptoms
    elif code.startswith("R10"):
        return "Abdominal_Pain"

    # Diarrhea symptoms
    elif code.startswith("R19"):
        return "Diarrhea"

    # Everything else
    else:
        return "Other"


# Create normalized diagnosis category feature
claims_df["icd_category"] = claims_df["primary_icd10"].apply(
    categorize_icd10
)


# -----------------------------------------------------------------------------
# MEDICATION NORMALIZATION
# -----------------------------------------------------------------------------
#
# Groups medications into therapeutic classes.
#
# In production systems, this may come from:
# - RxNorm mappings
# - formulary reference tables
# - pharmacy data marts
#
# -----------------------------------------------------------------------------

med_map = {

    # Biologic therapies commonly used for Crohn's disease
    "Adalimumab": "Biologic",
    "Infliximab": "Biologic",

    # Steroid treatment
    "Prednisone": "Steroid",

    # GI anti-inflammatory medication
    "Mesalamine": "AntiInflammatory",

    # GI symptom management medications
    "Omeprazole": "GI",
    "Loperamide": "GI",
    "Dicyclomine": "GI"
}


# Create normalized medication class feature
claims_df["med_class"] = claims_df["medication"].map(med_map)


# =============================================================================
# STEP 3 — ENCODE CATEGORICAL FEATURES
# =============================================================================
#
# Machine learning models require numeric input.
#
# This converts text fields into numeric representations.
#
# Example:
# "Crohns" -> 0
# "Diarrhea" -> 1
#
# =============================================================================

categorical_cols = [
    "primary_icd10",
    "procedure_code",
    "medication",
    "icd_category",
    "med_class"
]

# Store encoders for future inference/prediction pipelines
label_encoders = {}

for col in categorical_cols:

    # Create encoder object
    le = LabelEncoder()

    # Convert text categories into numeric labels
    claims_df[col] = le.fit_transform(claims_df[col])

    # Save encoder
    label_encoders[col] = le


# =============================================================================
# STEP 4 — FEATURE SELECTION
# =============================================================================
#
# PURPOSE:
# Select which columns/features the ML model should use.
#
# FEATURES INCLUDE:
# - diagnosis patterns
# - procedures
# - medication utilization
# - inflammation lab markers
#
# TARGET:
# Whether patient has Crohn's disease
#
# =============================================================================

X = claims_df[[
    "primary_icd10",
    "procedure_code",
    "medication",
    "icd_category",
    "med_class",
    "crp_level",
    "hemoglobin"
]]

# Ground truth labels
y = claims_df["crohns_diagnosis"]


# =============================================================================
# STEP 5 — TRAIN / TEST SPLIT
# =============================================================================
#
# PURPOSE:
# Separate data into:
#
# TRAINING DATA:
# Used to teach model patterns
#
# TEST DATA:
# Used to evaluate model performance on unseen patients
#
# =============================================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    # 30% reserved for testing
    test_size=0.30,

    # Ensures reproducibility
    random_state=42,

    # Maintains balanced class distribution
    stratify=y
)


# =============================================================================
# STEP 6 — BUILD XGBOOST MODEL
# =============================================================================
#
# XGBoost is commonly used because it:
# - handles structured healthcare data well
# - captures nonlinear relationships
# - performs well on claims data
# - manages missingness effectively
#
# =============================================================================

model = XGBClassifier(

    # Number of decision trees
    n_estimators=100,

    # Tree depth complexity
    max_depth=4,

    # Learning speed
    learning_rate=0.05,

    # Binary classification objective
    objective="binary:logistic",

    # Evaluation metric
    eval_metric="logloss",

    random_state=42
)


# Train the model
model.fit(X_train, y_train)


# =============================================================================
# STEP 7 — MODEL EVALUATION
# =============================================================================
#
# PURPOSE:
# Evaluate how accurately the model predicts Crohn's disease.
#
# METRICS:
# - Precision
# - Recall
# - F1-score
# - ROC-AUC
#
# =============================================================================

# Generate binary predictions
y_pred = model.predict(X_test)

# Generate probability scores
y_prob = model.predict_proba(X_test)[:, 1]


print("\n===== CLASSIFICATION REPORT =====")
print(classification_report(y_test, y_pred))


print("===== ROC-AUC SCORE =====")

# ROC-AUC measures model discrimination ability
# Higher = better
print(round(roc_auc_score(y_test, y_prob), 3))


print("\n===== CONFUSION MATRIX =====")

# Shows:
# True positives
# False positives
# True negatives
# False negatives
print(confusion_matrix(y_test, y_pred))


# =============================================================================
# STEP 8 — IDENTIFY HIGH-RISK UNDIAGNOSED PATIENTS
# =============================================================================
#
# REAL BUSINESS USE CASE:
#
# The most valuable output is identifying patients who:
# - are NOT officially diagnosed
# - BUT show strong clinical patterns consistent with Crohn's disease
#
# These patients can be flagged for:
# - physician review
# - outreach programs
# - earlier GI referrals
#
# =============================================================================

# Generate prediction probabilities for all patients
claims_df["predicted_risk_score"] = model.predict_proba(X)[:, 1]


# Filter:
# - no official diagnosis
# - high model risk score
high_risk_patients = claims_df[
    (claims_df["crohns_diagnosis"] == 0) &
    (claims_df["predicted_risk_score"] >= 0.70)
]


print("\n===== POTENTIAL UNDIAGNOSED PATIENTS =====")

print(
    high_risk_patients[
        ["patient_id", "predicted_risk_score"]
    ].sort_values(
        by="predicted_risk_score",
        ascending=False
    )
)


# =============================================================================
# STEP 9 — FEATURE IMPORTANCE ANALYSIS
# =============================================================================
#
# PURPOSE:
# Understand which features contributed most to predictions.
#
# IMPORTANT FOR:
# - explainability
# - provider trust
# - healthcare compliance
# - model governance
#
# =============================================================================

feature_importance = pd.DataFrame({

    "feature": X.columns,

    # Relative predictive importance
    "importance": model.feature_importances_

}).sort_values(by="importance", ascending=False)


print("\n===== TOP PREDICTIVE FEATURES =====")
print(feature_importance)


# =============================================================================
# ENTERPRISE HEALTHCARE ANALYTICS CAPABILITIES DEMONSTRATED
# =============================================================================
#
# Clinical claims integration
# Patient-level normalization
# ICD-10-CM/PCS processing
# CPT/HCPCS enrichment
# RxNorm / NDC medication mapping
# LOINC laboratory integration
# Predictive healthcare analytics
# Risk stratification modeling
# Population health analytics
# Identification of undiagnosed patient cohorts
# Explainable ML modeling using XGBoost
