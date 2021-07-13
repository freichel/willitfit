"""
Defines global variables
"""

from pathlib import Path
import os


# Interface settings
LANG_CHOOSE = "---Choose a language---"
CAR_BRAND_CHOOSE = "---Choose a brand---"
CAR_MODEL_CHOOSE = "---Choose a model---"

# IKEA website scraper settings
IKEA_COUNTRY_DOMAIN = {
    'de1': 'de',
    'de2': 'at',
    'de3': 'ch',
    'en1': 'us',
    'en2': 'ca',
    'en3': 'gb',
    'en4': 'au',
    'fr': 'fr',
    'nl1': 'nl',
    'nl2': 'be',
    'da': 'dk',
    'no': 'no',
    'no': 'fi',
    'sv': 'se',
    'cs': 'cz',
    'es': 'es',
    'it': 'it',
    'hu': 'hu',
    'pl': 'pl',
    'pt': 'pt',
    'ro': 'ro',
    'sk': 'sk',
    'hr': 'hr',
    'sr': 'rs',
    'si': 'si',
}

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
    'Deutsch (DE)': 'de1',
    'Deutsch (AT)': 'de2',
    'Deutsch (CH)': 'de3',
    'English (US)': 'en1',
    'English (CA)': 'en2',
    'English (UK)': 'en3',
    'English (AU)': 'en4',
    'Français': 'fr',
    'Nederlands (NL)': 'nl1',
    'Nederlands (BE)': 'nl2',
    'Dansk': 'da',
    'Norsk': 'no',
    'Suomi': 'fi',
    'Svenska': 'se',
    'Česky': 'cs',
    'Español': 'es',
    'Italiano': 'it',
    'Magyar': 'hu',
    'Polski': 'pl',
    'Português': 'pt',
    'Romȃna': 'ro',
    'Slovenský': 'sk',
    'Hrvatski': 'hr',
    'Srpski': 'sr',
    'Slovenščina': 'sl',
}

# Volume array settings
VOL_UNAVAILABLE = -1
VOL_BORDER = 1
VOL_INTERIOR = -2
VOL_EMPTY = 0

# Optimizer settings
BIAS_STACKS = [(False, 0), (True, 0.8), (True, 1)]
RANDOM_LIST_COUNT = 3
OPT_MAX_ATTEMPTS = 10
GEN_SORTERS = ["volume|descending"]
OPTIMIZER_OPTIONS = {
    "Efficient" : ["Very fast, but may miss more optimal results.", ["Rigid", "Rigid"], 0, 1],
    "Standard" : ["Usually the most appropriate setting for most users. Provides a balance between speed and performance.", ["Rigid", "Biased"], 3, 5],
    "Thorough" : ["Much longer processing time, but may find a better result through brute force.", ["Rigid", "Flexible"], 10, 10]
}
STACKING_OPTIONS = {
    "Rigid" : ["Packages are placed as flat as possible.", 2],
    "Biased" : ["Packages will most likely be placed as flat as possible, but there is some randomness", 1],
    "Flexible" : ["Packages can be placed in any orientation at random.", 0]
}

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
ARTICLE_NOT_FOUND = "One or more articles could not be found."
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
UNABLE_TO_PARSE_LANG = "Check that the PDF language matches the language selected."
LIST_UNREADABLE = "Unexpected list format."
NO_DATA_PROVIDED = "Please upload wishlist PDF or add articles to the form."
ERRORS_INTERFACE = [NOT_PDF, UNABLE_TO_PARSE_LANG, LIST_UNREADABLE, NO_DATA_PROVIDED]
