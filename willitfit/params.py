'''
Defines global variables
'''
import numpy as np

# IKEA website scraper settings
IKEA_COUNTRY_DOMAIN = "de" # domain used
IKEA_WEBSITE_LANGUAGE = "de" # language used, often same as IKEA_COUNTRY_DOMAIN but may be different

# Volume array settings
VOL_UNAVAILABLE = -1
VOL_BORDER = 1
VOL_INTERIOR = -2
VOL_EMPTY = 0

# Dummy data for volume array
COORDS = [["article1",0,0,0,0,10,15,10],
          ["article2",1,10,0,0,15,10,5]]
VOLUME_SPACE = np.zeros((40,40,40), dtype=int)
VOLUME_SPACE[0:3,0:10,0:5] = VOL_UNAVAILABLE
#VOLUME_SPACE[:,0:2,:] = VOL_UNAVAILABLE
#VOLUME_SPACE[:,:,0] = VOL_UNAVAILABLE