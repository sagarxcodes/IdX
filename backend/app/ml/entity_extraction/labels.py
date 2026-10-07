ENTITY_LABELS = [
    "O",

    "B-PERSON",
    "I-PERSON",

    "B-ORG",
    "I-ORG",

    "B-COMPANY",
    "I-COMPANY",

    "B-PRODUCT",
    "I-PRODUCT",

    "B-BRAND",
    "I-BRAND",

    "B-LOCATION",
    "I-LOCATION",

    "B-COUNTRY",
    "I-COUNTRY",

    "B-CITY",
    "I-CITY",

    "B-MARKET",
    "I-MARKET",

    "B-INDUSTRY",
    "I-INDUSTRY",

    "B-COMPETITOR",
    "I-COMPETITOR",

    "B-REGULATION",
    "I-REGULATION",

    "B-EVENT",
    "I-EVENT",

    "B-METRIC",
    "I-METRIC",

    "B-CURRENCY",
    "I-CURRENCY",
]


LABEL_TO_ID = {
    label: index
    for index, label in enumerate(
        ENTITY_LABELS
    )
}


ID_TO_LABEL = {
    index: label
    for label, index in LABEL_TO_ID.items()
}
