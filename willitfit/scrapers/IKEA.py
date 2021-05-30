'''
Receives list of article codes and article counts.
Scrapes IKEA website to obtain package dimensions (rounded up to next cm), weights (in kg rounded up 2 decimals) and counts.
Returns list of package dimensions and weights.
'''

from willitfit.params import IKEA_COUNTRY_DOMAIN, IKEA_WEBSITE_LANGUAGE
import requests
from bs4 import BeautifulSoup

IKEA_URL = "https://www.ikea.IKEA_COUNTRY_DOMAIN/IKEA_WEBSITE_LANGUAGE"