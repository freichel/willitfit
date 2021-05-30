'''
Receives list of package dimensions, weights and counts
Receives available volume
Optimizes stacking of packages in available volume
Returns 3D numeric representation of occupied space as well as article coordinates
'''

from willitfit.params import VOL_INTERIOR, VOL_UNAVAILABLE, VOL_BORDER, VOL_EMPTY
import numpy as np