import math
import pathlib
import tarfile
import urllib.request

import ase
import ase.io
import matplotlib.pyplot as plt
import numpy as np
import plotly
from plotly import graph_objects
from IPython import display


def split_data(features, objectives, train_ratio):
    """Split data into a fitting and training set"""
    assert len(features) == len(objectives)
    total_envs = len(features)

    training_index = int(train_ratio * total_envs)
    X = np.copy(features[:training_index])
    Y = np.copy(objectives[:training_index])
    X_test = np.copy(features[training_index:])
    Y_test = np.copy(objectives[training_index:])

    return X, Y, X_test, Y_test


def plot_histogram(objective, xlabel=None, ylabel=None, log=True):
    plt.hist(objective, 50, log=log)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    plt.show()

    
def create_povray_img(
    atoms: ase.atoms.Atoms,
    basename='atoms_pov',
    x=None,
    y=None,
    z=None,
    **overrides,
    ):
        x = x or 0.
        y = y or 0.
        z = z or 0.
        
        rot = f'{x}x,{y}y,{z}z'  # found using ag: 'view -> rotate'

        # Common kwargs for eps, png, pov
        kwargs = {
            'rotation'      : rot, # text string with rotation (default='' )
            'radii'         : .85, # float, or a list with one float per atom
            'colors'        : None,# List: one (r, g, b) tuple per atom
            'show_unit_cell': 2,   # 0, 1, or 2 to not show, show, and show all of cell
            }

        # Extra kwargs only available for povray (All units in angstrom)
        kwargs.update({
            'run_povray'   : True, # Run povray or just write .pov + .ini files
            'display'      : False,# Display while rendering
            'pause'        : True, # Pause when done rendering (only if display)
            'transparent'  : True,# Transparent background
            'canvas_width' : 1024, # Width of canvas in pixels
            'canvas_height': None, # Height of canvas in pixels 
            'camera_dist'  : 50.,  # Distance from camera to front atom
            'image_plane'  : None, # Distance from front atom to image plane
            'camera_type'  : 'perspective', # perspective, ultra_wide_angle
            'point_lights' : [],             # [[loc1, color1], [loc2, color2],...]
            'area_light'   : [(2., 3., 40.), # location
                              'White',       # color
                              .7, .7, 3, 3], # width, height, Nlamps_x, Nlamps_y
            'background'   : 'White',        # color
            'textures'     : None, # Length of atoms list of texture names
            'celllinewidth': 0.1,  # Radius of the cylinders representing the cell
            })
        kwargs.update(overrides)

        # Write the .pov (and .ini) file. If run_povray=False, you must run command
        # `povray filename.ini` to convert .pov file to .png
        ase.io.write(f'{basename}.pov', atoms, **kwargs)
        return display.Image(filename=f'{basename}.png')

    
def create_contours_plot(grid, slice_indices, *grid_data, cols = 4, normalise=False, titles = None):
    num_grids = len(grid_data)
    rows = int(math.ceil(num_grids / cols))
    # colorscale=[(0, 'red'), (0.6, 'white'), (0.7, 'black'), (0.8, 'blue'), (1, 'red')]
    colorscale=['red', 'white', 'black', 'blue', 'red']
    spacing = 0.04

    slice_points = grid[slice_indices][:,0,:]

    titles = titles or tuple(f"n = {idx}" for idx in range(len(grid_data)))
    fig = plotly.subplots.make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=titles,
        shared_xaxes=True,
        shared_yaxes=True,
        horizontal_spacing=spacing,
        vertical_spacing=spacing
    )
    # colorscale=[(0, '#aabbaa'), (0.35, 'white'), (0.567, 'grey'), (0.78, 'blue'), (1., 'red')]
    #(0, '#72b7b2')
    idx = 0
    for row in range(rows):
        for col in range(cols):
            if idx < len(grid_data):
                vals = grid_data[idx][slice_indices][:, 0]
                if normalise:
                    vals = vals / vals.max()
                countour = graph_objects.Contour(
                    x=slice_points[:,0],
                    y=slice_points[:,1],
                    z=vals,
                    connectgaps=False,
                    showscale=False,
                )
                ret = fig.add_trace(countour, row=row + 1, col=col + 1)
                axis = idx + 1
                fig.update_layout({
                    f'yaxis{axis}': {'scaleratio':1, 'scaleanchor': f'x{axis}', 'matches': None,},
                    f'xaxis{axis}': {'matches': None}
                })
                idx += 1

    fig.update_yaxes(matches=None, range=(-1, 1), constrain="domain")
    fig.update_xaxes(matches=None, range=(-1, 1), constrain="domain")
    scale = 250
    fig.update_layout(height=scale * rows, width=scale * cols)
    
    return fig



def get_dragoni_dataset(path='data/iron_dragoni/') -> pathlib.Path:
    url = 'https://archive.materialscloud.org/record/file?record_id=12&filename=DB_bccFe_Dragoni.tar.gz&file_id=2addc7de-9ead-457e-8e49-34e59722d051'
    path = pathlib.Path(path)
    path.mkdir(parents=True, exist_ok=True)
    dataset_path = path / 'iron_dragoni.tar.gz'
    
    if not dataset_path.exists():
        urllib.request.urlretrieve(url, dataset_path)
        
    with tarfile.open(dataset_path) as dbs:
        dbs.extractall(path)
    
    return path

def read_dragoni_database(number: int, index=':'):
    filename = 'DB{}.xyz'.format(number)
    return ase.io.read(get_dragoni_dataset() / filename, index=index)

