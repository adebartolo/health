# =============================================================================
# FORMULARY REFERENCE TABLE EXAMPLE
# =============================================================================
#
# PURPOSE:
# Tracks whether medications are:
# - covered by insurance
# - preferred/non-preferred
# - require prior authorization
#
# Commonly joined into:
# - claims pipelines
# - pharmacy analytics
# - cost optimization dashboards
#
# =============================================================================

import pandas as pd

formulary_df = pd.DataFrame({

    "drug_name": [
        "Adalimumab",
        "Infliximab",
        "Mesalamine",
        "Prednisone"
    ],

    "tier": [
        4,
        4,
        2,
        1
    ],

    "preferred_status": [
        "Non-Preferred",
        "Preferred",
        "Preferred",
        "Preferred"
    ],

    "prior_authorization_required": [
        True,
        True,
        False,
        False
    ],

    "specialty_drug": [
        True,
        True,
        False,
        False
    ]
})

print(formulary_df)
