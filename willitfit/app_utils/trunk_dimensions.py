import numpy as np
import pandas as pd
from willitfit.params import VOL_EMPTY, VOL_UNAVAILABLE

# Prototype Car DataFrame
df_dict = {
    'car_model': ['Subaru saloon 2018', 'Toyota hatch 2015', 'BMW coup 2019'],
    'max_depth': [159, 133, np.nan],
    'depth': [70, 67, 81],
    'height': [76, 86, 35],
    'width': [89, 100, 85]}

data = pd.DataFrame(df_dict)
data.set_index('car_model', inplace=True)

def get_volume_space(car_model, ratio_door=0.2):
    """
    Returns available volume for a specific car_model.
    Use ratio_door to tweak estimated unavailable space caused by 45-degree trunk-door slope.
    """
    # Isolate dimension cols
    dim_cols = ['depth', 'height', 'width']

    # Trunk dimensions
    trunk_dims = data.loc[car_model][dim_cols].to_numpy(int)

    # Cuboid Volume Space
    volume_space = np.full(trunk_dims, VOL_EMPTY, dtype=int)

    # Unavailable space
    depth_to_block = int(trunk_dims[0]*ratio_door)
    for i in range(-depth_to_block, 0, 1):
        volume_space[i,-i:,:] = VOL_UNAVAILABLE

    return volume_space
