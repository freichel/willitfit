import numpy as np
import pandas as pd
from willitfit.params import CAR_DATABASE, VOL_EMPTY, VOL_UNAVAILABLE
from willitfit.app_utils.utils import get_car_data

def get_volume_space(car_model, data, ratio_height=0.5, slant=1):
    """
    Returns available volume for a specific car_model.
    Use ratio_height to tweak estimated unavailable space caused by 45-degree trunk-door slope.
    """
    # Isolate dimension cols
    dim_cols = ['depth', 'height', 'width']

    # Trunk dimensions
    model_row = data[data['car_model'] == car_model]
    trunk_dims = model_row[dim_cols].to_numpy(int)[0]

    # Cuboid Volume Space
    volume_space = np.full(trunk_dims, VOL_EMPTY, dtype=int)

    # Unavailable space
    height_block = int(trunk_dims[1]*ratio_height)
    for i in range(height_block):
        volume_space[i,height_block+(slant*i):,:] = VOL_UNAVAILABLE
    return volume_space
