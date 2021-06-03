'''
Back-end to connect user interface with various modules.
Receives user inputs via POST request on /collect:
- List of IKEA articles
- Car model
- Website location and language
Receives car trunk dimensions for chose car model.
Feeds list of IKEA articles into scraper and receives list of packages for each article.
Updates this list with article counts.
Feeds trunk dimensions and package lists to optimizer, receives optimal stacking of packages.
Feeds package coordinates and filled trunk dimensions to plotter, receives plot.
Returns plot to user interface.
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from willitfit.params import ERRORS_OPTIMIZER, ERRORS_SCRAPER, ERRORS_INTERFACE
from willitfit.optimizers.volumeoptimizer import generate_optimizer
from willitfit.plotting.plotter import plot_all
from willitfit.scrapers.IKEA import product_info_and_update_csv_database
from willitfit.app_utils.trunk_dimensions import get_volume_space
import numpy as np
import matplotlib.pyplot as plt
import plotly
import pandas as pd

# Initialize API
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Class to capture user interface inputs parsed via POST
class RequestText(BaseModel):
    article_dict: dict
    car_model: str
    IKEA_country: str
    IKEA_language: str

# Decorator for interface call to API
@app.post("/collect")
def input_output(request_text: RequestText):
    '''
    See moddule docstring for detailed information.
    '''
    
    '''
    Unpack the following arguments
    - Article list as dict
    - Car ID
    - IKEA website location and language (see params.py too)
    '''
    request_dict = dict(request_text)
    article_dict = request_dict["article_dict"]
    #TODO
    # Value in dict is passed as list, should be int
    article_dict = {key: sum(value) for key,value in article_dict.items()}
    car_id = request_dict["car_model"]
    IKEA_COUNTRY_DOMAIN = request_dict["IKEA_country"]
    IKEA_WEBSITE_LANGUAGE = request_dict["IKEA_language"]
    
    '''
    Find car trunk dimensions for given car_id
    '''
    
    volume_space = get_volume_space(car_id)
    #volume_space = np.zeros((100,100,100), dtype=int)
            
    '''
    Call scraper with article list and website location/language.
    Receive list of package dimensions and weights for each article.
    '''
    
    
    #TODO
    scraper_return = product_info_and_update_csv_database(article_dict)
    if scraper_return not in ERRORS_SCRAPER:
        article_list = scraper_return
    else:
        return scraper_return
    
    '''
    Call optimizer with article list and volume array.
    Receive package coordinates and filled volume array.
    '''
    optimizer_return = generate_optimizer(article_list, np.copy(volume_space), generator_random_lists=2, optimizer_max_attempts=5)
    if optimizer_return not in ERRORS_OPTIMIZER:
        filled_space, package_coordinates = optimizer_return
    else:
        return optimizer_return
    
    return optimizer_return
    
     
    '''
    Call plotter with package coordinates and filled volume array.
    Receive plot
    '''
    plotter_return = plot_all(filled_space, package_coordinates)
    to_interface = plotly.io.to_json(plotter_return)
    return to_interface
