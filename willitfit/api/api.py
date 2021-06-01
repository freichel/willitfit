'''
DOCSTRING to come
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from willitfit.params import ERRORS_OPTIMIZER, ERRORS_SCRAPER, ERRORS_INTERFACE
from willitfit.optimizers.volumeoptimizer import generate_optimizer
#from willitfit.plotting.plotter import plot_all
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

# Decorator for interface call to API
@app.post("/collect")
def input_output(*args):
    #TODO
    # This section is for testing only
    return args
    
    
    '''
    Receives user input from front end.
    Calls relevant functions to process user input.
    Returns output to front end.
    '''
    
    '''
    Unpack the following arguments
    - article list as dict
    - volume array
    - IKEA website location and language (see params.py)
    '''
    
    '''
    Call scraper with article list and website location/language.
    Receive list of package dimensions and weights.
    '''
    scraper_return = "TBD"
    if scraper_return not in ERRORS_SCRAPER:
        pass
    else:
        return scraper_return
    
    '''
    Call optimizer with package list and volume array.
    Receive package coordinates and filled volume array.
    '''
    optimizer_return = generate_optimizer(article_list, np.copy(volume_space))
    if optimizer_return not in ERRORS_OPTIMIZER:
        filled_space, package_coordinates = optimizer_return
    else:
        return optimizer_return
    
    '''
    Call plotter with package coordinates and filled volume array.
    Receive plot
    '''
    plotter_return = plot_all(filled_space, package_coordinates)
    return plotter_return
