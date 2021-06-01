'''
Receives 3D numeric representation of occupied space as well as article coordinates
Returns interactive 3D plot of packages
'''

from numpy.lib.shape_base import split
from willitfit.params import COORDS, VOL_INTERIOR, VOL_UNAVAILABLE, VOL_BORDER, VOL_EMPTY, VOLUME_SPACE
from willitfit.plotting.plot_helper import get_split_indexes, split_array_by_index
import numpy as np
import plotly.graph_objects as go


def generate_cuboids(article_coords):
    '''Convert article start & end coords info into a list of plotly.go.Mesh3d objects
    Args:
        article_coords - a list of articles and their start/end coordinates: [[article_code, article_id, x_start, y_start, z_start, x_end, y_end, z_end]]
        unavailable_space - (optional: default=False) denotes whether the generated cuboids should be treated as unavailable space
    Returns:
        meshes - a list of cuboids as Mesh3d objects
    '''
    meshes = []

    for item in article_coords:
        # corners for each face
        x1 = item[2] # x_start
        x2 = item[5] # x_end
        y1 = item[3] # y_start
        y2 = item[6] # y_end
        z1 = item[4] # z_start
        z2 = item[7] # z_end

        mesh = go.Mesh3d(
            name=item[0],
            # 8 vertices of a cube
            x=[x1, x1, x2, x2, x1, x1, x2, x2],
            y=[y1, y2, y2, y1, y1, y2, y2, y1],
            z=[z1, z1, z1, z1, z2, z2, z2, z2],
            alphahull=0,
            flatshading=True,
            opacity=0.5,
            hoverinfo="name"
        )
        meshes.append(mesh)

    return meshes


def draw_3d_plot(meshes):
    '''Draw a 3D plotly.go plot of cuboids
    Args:
        meshes - a list of cuboids as Mesh3d objects
    Returns:
        fig - a plotly.go.Figure
    Returns:
    '''
    x_max = VOLUME_SPACE.shape[0]
    y_max = VOLUME_SPACE.shape[1]
    z_max = VOLUME_SPACE.shape[2]
    layout = go.Layout(
        scene = dict(
            aspectmode='cube',
            xaxis = dict(
                type='linear',
                range = [0,x_max],
                showgrid=False,
                showspikes=False,
                #showbackground=False,
                ),
            yaxis = dict(
                type='linear',
                range = [0,y_max],
                showgrid=False,
                showspikes=False,
                #showbackground=False,
                ),
            zaxis = dict(
                type='linear',
                range = [0,z_max],
                showgrid=False,
                showspikes=False,
                #showbackground=False,
                ),
        )
    )
    fig = go.Figure(data=meshes, layout=layout)
    return fig


def generate_mesh3d_from_coords(coords_arr):
    '''Generate plotly.go.mesh3d objects from arrays of coords
    Args:
        coords_arr - list of 3 by n np.arrays, with coordinates for each vertex
    Returns:
        meshes - list of plotly.go.mesh3d objects
    '''
    meshes = []
    for arr in coords_arr:
        x,y,z = arr
        meshes.append(go.Mesh3d(x=x,
                                y=y,
                                z=z,
                                alphahull=0,
                                color='grey',
                                flatshading=True))

    return meshes


def get_unavailable_meshes(fitted_array):
    '''Parse an array with unavailable space (VOL_UNAVAILABLE) and generate Mesh3d objects
    Args:
        fitted_array - 3D array with any number of "unavailable" cells
    Returns:
        meshes - a list of plotly.go.Mesh3d objects
    '''

    # get all coords which are 'unavailable'
    unavail_coords = np.argwhere(fitted_array == VOL_UNAVAILABLE).T

    # split coords based on their shapes
    split_indexes = get_split_indexes(unavail_coords)
    coords_split = split_array_by_index(unavail_coords, split_indexes)

    meshes = generate_mesh3d_from_coords(coords_split)

    return meshes


def plot_all(fitted_array=VOLUME_SPACE, article_coords=COORDS):
    '''Primary function for generating 3D plot
    Args:
        fitted_array - 3D numpy array with optimally fit packages
        article_coords - list of articles and their start/end coordinates
    '''
    package_meshes = generate_cuboids(article_coords)
    unavailable_meshes = get_unavailable_meshes(fitted_array)

    fig = draw_3d_plot(unavailable_meshes + package_meshes)

    return fig