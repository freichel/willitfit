"""
Defines global variables
"""

import numpy as np
from pathlib import Path
import os

# Interface settings
LANG_CHOOSE = "---Choose a language---"
CAR_BRAND_CHOOSE = "---Choose a brand---"
CAR_MODEL_CHOOSE = "---Choose a model---"

# IKEA website scraper settings
IKEA_COUNTRY_DOMAIN = "de"  # domain used
IKEA_WEBSITE_LANGUAGE = (
    "de"  # language used, often same as IKEA_COUNTRY_DOMAIN but may be different
)
IKEA_DATABASE_DTYPES = {
    "height": "int16",
    "width": "int16",
    "length": "int16",
    "packages": "int8",
    "article_code": "str",
    "subarticle_code": "str",
}

# Humanised language codes
LANG_CODE = {
    LANG_CHOOSE: LANG_CHOOSE,
    "Deutsch": "de",
    "English": "en",
    "Français": "fr",
    "Nederlands": "nl",
    "Dansk": "da",
    "Norsk": "no",
    "Suomi": "fi",
    "Svenska": "se",
    "Česky": "cs",
    "Español": "es",
    "Italiano": "it",
    "Magyar": "hu",
    "Polski": "pl",
    "Português": "pt",
    "Romȃna": "ro",
    "Slovenský": "sk",
    "Hrvatski": "hr",
    "Srpski": "sr",
    "Slovenščina": "sl",
}

# Volume array settings
VOL_UNAVAILABLE = -1
VOL_BORDER = 1
VOL_INTERIOR = -2
VOL_EMPTY = 0

# Optimizer settings
# BIAS_STACKS = [(False, 0), (True, 0.8), (True, 1)]
BIAS_STACKS = [(True, 0.8)]
RANDOM_LIST_COUNT = 8
OPT_MAX_ATTEMPTS = 10
GEN_SORTERS = ["volume|descending"]

# Deployment variables
PROJECT_DIR = Path(os.path.abspath(__file__)).parent.parent.absolute()
PROJECT_NAME = "willitfit"
DATA_FOLDER = "data"
CAR_DATABASE = "cars_clean_config.csv"
ARTICLE_DATABASE = "ikea_database.csv"
INTERFACE_INSTRUCTIONS = "frontend/pdf_frontend_instructions.md"

# Google Cloud variables
PROJECT_ID = PROJECT_NAME
BUCKET_NAME = PROJECT_ID + "-bucket"
BUCKET_FOLDER = DATA_FOLDER
GOOGLE_APPLICATION_CREDENTIALS = PROJECT_NAME + "/keys/willitfit-bc6d464d89ff.json"

# Function return codes
# Optimizer
INSUFFICIENT_SPACE = "Not enough space for packages in chosen trunk."
INSUFFICIENT_DIMENSION = "At least one package dimension exceeds trunk dimension."
OPT_INSUFFICIENT_SPACE = (
    "Optimizer could not place this package (internal return code)."
)
OPT_UNSUCCESSFUL = "Optimizer was unable to place all packages."
ERRORS_OPTIMIZER = [
    INSUFFICIENT_SPACE,
    INSUFFICIENT_DIMENSION,
    OPT_INSUFFICIENT_SPACE,
    OPT_UNSUCCESSFUL,
]

# Scraper
WEBSITE_UNAVAILABLE = "Website temporarily unavailable."
ARTICLE_NOT_FOUND = "One or more articles do not exist."
ERRORS_SCRAPER = [WEBSITE_UNAVAILABLE, ARTICLE_NOT_FOUND]
DTYPE_DICT = {
    "width": int,
    "height": int,
    "length": int,
    "weight": float,
    "packages": int,
    "subarticle_code": str,
    "article_code": str,
    "product_name": str
}

# Interface
NOT_PDF = "Document is not a PDF."
UNABLE_TO_PARSE_LANG = 'Check that the PDF language matches the language selected.'
LIST_UNREADABLE = "Unexpected list format."
NO_DATA_PROVIDED = "Please upload wishlist PDF or add articles to the form."
ERRORS_INTERFACE = [NOT_PDF, UNABLE_TO_PARSE_LANG, LIST_UNREADABLE, NO_DATA_PROVIDED]
