"""
Receives 3D numeric representation of occupied space as well as article coordinates
Returns interactive 3D plot of packages
"""

from re import M
from willitfit.params import VOL_INTERIOR, VOL_UNAVAILABLE, VOL_BORDER, VOL_EMPTY
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.ndimage import convolve


def generate_cuboids(package_coordinates, product_names):
    """Convert article start & end coords info into a list of plotly.go.Mesh3d objects
    Args:
        package_coordinates - a list of articles and their start/end coordinates: [[article_code, article_id, package_id, x_start, y_start, z_start, x_end, y_end, z_end]]
        product_names - pandas.DataFrame with article_code as index, product_name column
    Returns:
        meshes - a list of cuboids as Mesh3d objects
    """
    meshes = []

    for item in package_coordinates:
        x1 = item[3]  # x_start
        y1 = item[4]  # y_start
        z1 = item[5]  # z_start

        x2 = item[6]  # x_end
        y2 = item[7]  # y_end
        z2 = item[8]  # z_end

        mesh = go.Mesh3d(
            name=str(product_names.loc[item[0], "product_name"]) + " | " + item[0],
            # 8 vertices of a cuboid
            x=[x1, x1, x2, x2, x1, x1, x2, x2],
            y=[y1, y2, y2, y1, y1, y2, y2, y1],
            z=[z1, z1, z1, z1, z2, z2, z2, z2],
            alphahull=0,
            # Set package styling below
            flatshading=True,
            opacity=0.5,
            showlegend=True,
            hoverinfo="name",
            hoverlabel=dict(namelength=-1),
        )
        meshes.append(mesh)

    return meshes


def generate_mesh3d_from_coords(coords_arr):
    """Generate a plotly.go.Mesh3d object from a numpy array of coords
    Args:
        coords_arr - list of 3 by n np.arrays, with coordinates for each vertex
    Returns:
        mesh - a plotly.go.Mesh3d object
    """
    x, y, z = coords_arr
    mesh = go.Mesh3d(
        name="Unavailable space",
        x=x,
        y=y,
        z=z,
        alphahull=0,
        # Set unavailable space styling below
        color="grey",
        flatshading=True,
        visible="legendonly",
        showlegend=True,
        hoverinfo="none",
    )

    return mesh


def get_unavailable_mesh(volume_space):
    """Parse an array with unavailable space (VOL_UNAVAILABLE) and generate a Mesh3d object
    Args:
        volume_space - 3D array with any number of "unavailable" cells
    Returns:
        mesh - a plotly.go.Mesh3d object
    """
    # Binarize unavailable space
    volume_space = np.isin(volume_space, VOL_UNAVAILABLE).astype(np.uint8)

    # Kernal for convolve function
    kernel = np.zeros((5, 5, 5))
    kernel[2, :, 2] = 1
    kernel[2, 2, :] = 1
    kernel[:, 2, 2] = 1

    # Convolve over the unavailable to find edges
    convolved = convolve(volume_space, kernel, mode="constant", cval=0.0)

    # Select corners based on the convolution 'score'
    edge_coords = np.argwhere(convolved == 7)

    mesh = generate_mesh3d_from_coords(edge_coords.T)

    return mesh


def draw_3d_plot(meshes, volume_dimensions):
    """Draw a 3D plotly.go plot of meshes
    Args:
        meshes - a list of plotly.go.Mesh3d objects
        volume_dimensions - a tuple of 3 integers (x,y,z) referring to the dimensions of the volume
    Returns:
        fig - a plotly.go.Figure object
    """
    x_max, y_max, z_max = volume_dimensions
    print(volume_dimensions)

    # Styling for all plot axes
    def axis_dict(max):
        return dict(
            type="linear",
            range=[0, max],
            showgrid=False,
            showspikes=False,
            showticklabels=False,
            title=dict(text=""),
            backgroundcolor="lightgrey",
            # showbackground=False,
        )

    layout = go.Layout(
        scene = dict(
            aspectmode="manual",
            aspectratio=dict(x=1,y=1,z=1),
            xaxis = axis_dict(x_max),
            yaxis = axis_dict(y_max),
            zaxis = axis_dict(z_max),
        ),
        width=None,
        height=None,
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(
            borderwidth=2,
            font=dict(size=16),
            title=dict(side="top", text="Article List", font=dict(size=16)),
            y=0.9,
            itemsizing="constant",
        ),
    )
    fig = go.Figure(data=meshes, layout=layout)

    return fig


def plot_all(volume_space, package_coordinates, product_names, plot_unavailable=True):

    """Primary function for generating 3D plot
    Args:
        volume_space - 3D numpy array with optimally fit packages
        package_coordinates - list of articles and their start/end coordinates, produced by optimizers.volumeoptimizer
        product_names - pandas.DataFrame with article_code as index, product_name column
        plot_unavailable - bool(default=False). If true, also plot unavailable space
    Returns:
        fig = a plotly.go.Figure object
    """
    meshes = generate_cuboids(package_coordinates, product_names)

    if plot_unavailable:
        unavailable_mesh = get_unavailable_mesh(volume_space)
        meshes.append(unavailable_mesh)

    volume_dimensions = volume_space.shape
    fig = draw_3d_plot(meshes, volume_dimensions)

    return fig
