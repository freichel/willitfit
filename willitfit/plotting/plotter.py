'''
Receives 3D numeric representation of occupied space as well as article coordinates
Returns interactive 3D plot of packages
'''

from willitfit.params import VOL_INTERIOR, VOL_UNAVAILABLE, VOL_BORDER, VOL_EMPTY, VOLUME_SPACE
import numpy as np
import plotly.graph_objects as go


def generate_cuboids(article_coords, unavailable_space=False):
    '''Convert article start & end coords info into a list of plotly.go.Mesh3d objects
    Args:
        article_coords - a list of articles and their start coordinates: [[article_code, article_id, x_start, y_start, z_start, x_end, y_end, z_end]]
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
            facecolor=['grey'] if unavailable_space else None,
            alphahull=0,
            flatshading=True,
            #opacity=0.5 if unavailable_space else 1,
            hoverinfo="name",
            #i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
            #j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
            #k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
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
                showgrid=False,),
            yaxis = dict(
                type='linear',
                range = [0,y_max],
                showgrid=False,),
            zaxis = dict(
                type='linear',
                range = [0,z_max],
                showgrid=False,),
        )
    )
    fig = go.Figure(data=meshes, layout=layout)
    return fig