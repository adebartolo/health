# Overview

This repository demonstrates an end-to-end healthcare analytics and machine learning workflows.

The project simulates enterprise healthcare data engineering and predictive analytics processes commonly used in:
- Population health
- Clinical risk stratification
- Care management
- Payer/provider analytics
- Early disease detection initiatives

---

# Objectives

- Integrate multi-domain healthcare data
- Normalize clinical coding systems
- Engineer patient-level features
- Train an XGBoost classification model
- Identify potentially undiagnosed Crohn’s patients
- Analyze feature importance and model explainability

---

# Data Domains Included

## Clinical Claims

- ICD-10-CM diagnosis codes
- CPT/HCPCS procedure codes
- Encounter-level claims

## Pharmacy Data

- RxNorm normalization
- NDC mappings
- Medication classifications
- Formulary reference enrichment

## Laboratory Data

- LOINC lab integration
- CRP inflammatory markers
- Hemoglobin measurements

## Provider Data

- NPI provider attribution
- Specialty provider analysis

---

# Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost

---

# Example Workflow

1. Load clinical claims data
2. Normalize diagnosis and medication terminology
3. Engineer patient features
4. Encode categorical variables
5. Train XGBoost model
6. Generate risk scores
7. Identify undiagnosed high-risk patients

---

# Example Healthcare Concepts Demonstrated

| Concept | Example |
|---|---|
| ICD-10 | K50.90 (Crohn's disease) |
| CPT | 45378 (Colonoscopy) |
| RxNorm | Adalimumab |
| NDC | 0074-4339-02 |
| LOINC | CRP Lab |
| NPI | Provider identifier |

---

# Example Use Cases

- Early disease intervention (i.e. for patients at high risk for certain diseases, using clinical claims and pharmacy data)
- Clinical decision support
- Utilization management
- Specialty drug analytics
- Population health monitoring
- Value-based care initiatives

---

# Machine Learning Approach

The project uses an XGBoost binary classification model to predict the probability that a patient may have Crohn’s disease based on:

- Diagnosis history
- Procedure utilization
- Medication patterns
- Lab abnormalities
- GI-related symptoms

---

# Output

The model generates:

- Patient risk scores
- High-risk patient cohorts
- Feature importance rankings
- Classification metrics

---

# Disclaimer

This repository uses synthetic demonstration data only.
No protected health information (PHI) or real patient data is included.
This project is intended for educational purposes.
