'''
DOCSTRING to come
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from willitfit.params import ERRORS_OPTIMIZER, ERRORS_SCRAPER, ERRORS_INTERFACE
from willitfit.optimizers.volumeoptimizer import generate_optimizer
from willitfit.plotting.plotter import plot_all
import numpy as np

# Initialize API
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Class to capture user interface inputs
class RequestText(BaseModel):
    article_list: list
    car_id: str
    IKEA_country: str
    IKEA_language: str

# Decorator for interface call to API
@app.post("/collect")
def input_output(request_text: RequestText):
    '''
    Receives user input from front end.
    Calls relevant functions to process user input.
    Returns output to front end.
    '''
    
    '''
    Unpack the following arguments
    - Article list as dict
    - Car ID
    - IKEA website location and language (see params.py too)
    '''
    request_dict = dict(request_text)
    article_list = request_dict["article_list"]
    car_id = request_dict["car_id"]
    IKEA_COUNTRY_DOMAIN = request_dict["IKEA_country"]
    IKEA_WEBSITE_LANGUAGE = request_dict["IKEA_language"]
    
    '''
    Find car trunk dimensions for given car_id
    '''
    #TODO
    # Placeholder for now
    volume_space = np.zeros((100,100,100), dtype=int)
            
    '''
    Call scraper with article list and website location/language.
    Receive list of package dimensions and weights.
    '''
    #TODO
    # Placeholder code
    scraper_return = "TBD"
    if scraper_return not in ERRORS_SCRAPER:
        pass
    else:
        return scraper_return
    '''
    Call optimizer with package list and volume array.
    Receive package coordinates and filled volume array.
    '''
    optimizer_return = generate_optimizer(article_list, np.copy(volume_space), generator_random_lists=0, optimizer_max_attempts=2)
    if optimizer_return not in ERRORS_OPTIMIZER:
        filled_space, package_coordinates = optimizer_return
    else:
        return optimizer_return
    '''
    Call plotter with package coordinates and filled volume array.
    Receive plot
    '''
    plotter_return = plot_all(filled_space, package_coordinates)
    return str(plotter_return)
