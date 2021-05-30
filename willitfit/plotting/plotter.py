'''
Receives 3D numeric representation of occupied space as well as article coordinates
Returns interactive 3D plot of packages
'''

from willitfit.params import VOL_INTERIOR, VOL_UNAVAILABLE, VOL_BORDER, VOL_EMPTY
import numpy as np
import matplotlib.pyplot as plt