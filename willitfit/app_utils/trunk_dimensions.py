import numpy as np
import pandas as pd
from willitfit.params import VOL_EMPTY, VOL_UNAVAILABLE

def get_volume_space(car_model, data, ratio_door=0.2):
    """
    Returns available volume for a specific car_model.
    Use ratio_door to tweak estimated unavailable space caused by 45-degree trunk-door slope.
    """
    # Isolate dimension cols
    dim_cols = ['depth', 'height', 'width']

    # Trunk dimensions
    model_row = data[data['car_model'] == car_model]
    trunk_dims = model_row[dim_cols].to_numpy(int)[0]

    # Cuboid Volume Space
    volume_space = np.full(trunk_dims, VOL_EMPTY, dtype=int)

    # Unavailable space
    depth_to_block = int(trunk_dims[0]*ratio_door)
    for i in range(-depth_to_block, 0, 1):
        volume_space[i,-i:,:] = VOL_UNAVAILABLE

    return volume_space
