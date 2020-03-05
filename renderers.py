import plotly.graph_objects as go
import plotly.express as px
import dash_core_components as dcc
from edflow.data.util import adjust_support


OPTIONS = [
    {'label': 'Image', 'value': 'image'},
    {'label': 'Points', 'value': 'scatter'},
    {'label': 'Flow', 'value': 'flow'},
    {'label': 'Text', 'value': 'text'}
]


def render_image(image_array, id):
    '''Displays an image. Allows zooming!

    Based on https://plot.ly/python/imshow/ and https://plot.ly/python/images/

    Parameters
    ----------
    image_array : np.ndarray
        Image to display. Shape: ``[W, H, 3 or 4]``. Will be modified for
        display using :func:`adjust_support`.
    '''

    plot_im = adjust_support(image_array, '0->255')

    # Create figure and add image
    fig = px.imshow(plot_im)

    info_dict = {
        'min': image_array.min(),
        'max': image_array.max(),
        'dtype': image_array.dtype,
        'dimensions': '{}x{}'.format(*image_array.shape[:2])
    }

    return dcc.Graph(id=id, figure=fig), info_dict

def render_scatter(scatter_points, id):
    '''Makes a scatterplot of points
    Parameters
    ----------
    image_array : np.ndarray
        Points to display. Shape: ``[N, 2]``
    '''

    fig = go.Figure(layout={'yaxis': {'scaleanchor': 'x',
                                      'scaleratio': 1.0 }})
    fig.update_yaxes(autorange="reversed")

    fig.add_trace(go.Scatter(x=scatter_points[..., 0],
                             y=scatter_points[..., 1],
                             mode='markers'))

    info_dict = {
        'x min': scatter_points[..., 0].min(),
        'x max': scatter_points[..., 0].max(),
        'y min': scatter_points[..., 1].min(),
        'y max': scatter_points[..., 1].max(),
        'number of points': len(scatter_points)
    }

    return dcc.Graph(id=id, figure=fig), info_dict

if __name__ == '__main__':
    import numpy as np
    render_image(np.random.uniform(0, 256, size=[256, 256, 4]).astype('uint8'))
