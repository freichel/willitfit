from willitfit.plotting.plotter import generate_cuboids


import plotly.graph_objects as go
from willitfit.plotting.plotter import generate_cuboids

def generate_cuboids():
    coords = [["article1",0,0,0,0,10,15,10],
          ["article2",1,10,0,0,15,10,5]]
    meshes = generate_cuboids(coords)
    assert(isinstance(meshes, list))
    assert(isinstance(meshes[0],go.Mesh3d))