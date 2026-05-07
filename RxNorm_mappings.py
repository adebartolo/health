# =============================================================================
# RXNORM MAPPING EXAMPLE
# =============================================================================
#
# PURPOSE:
# Standardize medication names from multiple pharmacy systems into
# normalized clinical concepts.
#
# WHY THIS MATTERS:
# Different systems may store the same drug differently:
#
# "Humira"
# "adalimumab"
# "Adalimumab 40MG Pen"
#
# RxNorm allows all of these to map to one standardized identifier.
#
# =============================================================================

rxnorm_mapping = {

    # Brand name -> standardized RxNorm concept
    "Humira": {
        "rxnorm_code": "327361",
        "generic_name": "Adalimumab",
        "drug_class": "Biologic"
    },

    "Remicade": {
        "rxnorm_code": "191831",
        "generic_name": "Infliximab",
        "drug_class": "Biologic"
    },

    "Prednisone 10mg": {
        "rxnorm_code": "8640",
        "generic_name": "Prednisone",
        "drug_class": "Corticosteroid"
    },

    "Lialda": {
        "rxnorm_code": "238381",
        "generic_name": "Mesalamine",
        "drug_class": "GI Anti-Inflammatory"
    }
}

print(rxnorm_mapping["Humira"])
