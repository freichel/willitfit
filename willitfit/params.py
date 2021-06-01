'''
Defines global variables
'''

# IKEA website scraper settings
IKEA_COUNTRY_DOMAIN = "de" # domain used 
IKEA_WEBSITE_LANGUAGE = "de" # language used, often same as IKEA_COUNTRY_DOMAIN but may be different

# Volume array settings
VOL_UNAVAILABLE = -1
VOL_BORDER = 1
VOL_INTERIOR = -2
VOL_EMPTY = 0

# Function return codes
# Optimizer
INSUFFICIENT_SPACE = "Not enough space for packages in chosen trunk."
INSUFFICIENT_DIMENSION = "At least one package dimension exceeds trunk dimension."
OPT_INSUFFICIENT_SPACE = "Optimizer could not place this package (internal return code)."
OPT_UNSUCCESSFUL = "Optimizer was unable to place all packages."
ERRORS_OPTIMIZER = [INSUFFICIENT_SPACE, INSUFFICIENT_DIMENSION, OPT_INSUFFICIENT_SPACE, OPT_UNSUCCESSFUL]

#TODO
'''
Scraper section
Please modify/enhance those error codes as needed
'''
# Scraper
WEBSITE_UNAVAILABLE = "Website temporarily unavailable."
ARTICLE_NOT_FOUND = "One or mor articles do not exist."
ERRORS_SCRAPER = [WEBSITE_UNAVAILABLE, ARTICLE_NOT_FOUND]

#TODO
'''
Interface section
Please modify/enhance those error codes as needed
'''
# Interface
NOT_PDF = "Document is not a PDF."
PDF_UNREADABLE = "Unexpected format."
API_CALL_ERROR = "Back-end offline."
ERRORS_INTERFACE = [NOT_PDF, PDF_UNREADABLE, API_CALL_ERROR]