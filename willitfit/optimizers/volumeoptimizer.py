'''
Receives list of package dimensions, weights and counts
Receives available volume
Optimizes stacking of packages in available volume
Returns 3D numeric representation of occupied space as well as article coordinates
'''

from willitfit.params import VOL_INTERIOR, VOL_UNAVAILABLE, VOL_BORDER, VOL_EMPTY
import numpy as np

'''
The following are just dummy data sets to run the algorithm
'''
article_list = [(
    "cube_1",
    2,
    [(
        1,
        10,
        10,
        10,
        1
    )]
),
                (
    "cube_2",
    2,
    [(
        1,
        15,
        15,
        15,
        2
    )]
),
                (
    "rectangle_1",
    1,
    [(
        1,
        15,
        30,
        30,
        2
    )]
)]

print(VOL_INTERIOR)