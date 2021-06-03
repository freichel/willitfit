'''
Defines global variables
'''

import numpy as np
from pathlib import Path
import os

# IKEA website scraper settings
IKEA_COUNTRY_DOMAIN = "de" # domain used
IKEA_WEBSITE_LANGUAGE = "de" # language used, often same as IKEA_COUNTRY_DOMAIN but may be different

# Volume array settings
VOL_UNAVAILABLE = -1
VOL_BORDER = 1
VOL_INTERIOR = -2
VOL_EMPTY = 0

# Deployment variables
API_URL = "http://127.0.0.1:8000/collect"
PROJECT_NAME = "willitfit"
DATA_FOLDER = "data"
CAR_DATABASE = "cars_clean.csv"
PROJECT_DIR = Path(os.path.abspath(__file__)).parent.parent.absolute()

# Google Cloud variables
PROJECT_ID = PROJECT_NAME
BUCKET_NAME = PROJECT_ID+"-bucket"
BUCKET_FOLDER = DATA_FOLDER
GOOGLE_APPLICATION_CREDENTIALS = PROJECT_NAME+"/keys/willitfit-bc6d464d89ff.json"

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
ARTICLE_NOT_FOUND = "One or more articles do not exist."
ERRORS_SCRAPER = [WEBSITE_UNAVAILABLE, ARTICLE_NOT_FOUND]

# Interface
NOT_PDF = "Document is not a PDF."
PDF_UNREADABLE = "Unexpected format."
API_CALL_ERROR = "Back-end offline."
NO_DATA_PROVIDED = "Please upload wishlist PDF or add Article Numbers!"
ERRORS_INTERFACE = [NOT_PDF, PDF_UNREADABLE, API_CALL_ERROR, NO_DATA_PROVIDED]

# Dummy data for volume array
COORDS = [["article1",0,1,0,0,0,10,15,10],
          ["article2",1,1,10,0,0,15,10,5]]
VOLUME_SPACE = np.zeros((40,40,40), dtype=int)
#VOLUME_SPACE[0:3,0:10,0:5] = VOL_UNAVAILABLE
#VOLUME_SPACE[:,0:2,:] = VOL_UNAVAILABLE
#VOLUME_SPACE[:,:,0] = VOL_UNAVAILABLE
