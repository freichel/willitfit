import numpy as np
import pandas as pd
from willitfit.params import CAR_DATABASE, VOL_EMPTY, VOL_UNAVAILABLE, DATA_FOLDER
#from willitfit.app_utils.utils import get_car_data
from willitfit.app_utils.googlecloud import get_cloud_data

def get_volume_space(data, car_model, extra_depth=False, ratio_height=0.5, slant=1):
    """
    Returns available volume for a specific car_model.
    Use ratio_height to tweak estimated unavailable space caused by 45-degree trunk-door slope.
    """
    # Isolate dimension cols
    dim_cols = ['depth', 'width', 'height']
    extra_depth_cols = ['extra_depth', 'width', 'height']

    # Load car data
    # data = get_cloud_data(DATA_FOLDER+"/"+CAR_DATABASE)

    # Trunk dimensions
    model_row = data[data['car_model'] == car_model]
    
    # extra_depth
    if extra_depth:
        trunk_dims = model_row[extra_depth_cols].to_numpy(int)[0]
    else:
        trunk_dims = model_row[dim_cols].to_numpy(int)[0]

    # Cuboid Volume Space
    volume_space = np.full(trunk_dims, VOL_EMPTY, dtype=int)

    # Unavailable space
    height_block = int(trunk_dims[2]*ratio_height)
    for i in range(height_block):
        volume_space[trunk_dims[0]-(i+1),:,height_block+(slant*i):] = VOL_UNAVAILABLE
    
    return volume_space
