import plotly.graph_objects as go
import plotly.express as px
import dash_core_components as dcc
from edflow.data.util import adjust_support
import numpy as np


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


def render_flow(flow_array, id):
    return str(flow_array), {'info': 'Not implemented'}


def render_text(text_obj, id):
    return str(text_obj), dict()


OPTIONS = [
    {'label': 'Image', 'value': 'im'},
    {'label': 'Points', 'value': 'scat'},
    {'label': 'Flow', 'value': 'flow'},
    {'label': 'Text', 'value': 'txt'}
]


RENDERERS = {
    'im': render_image,
    'scat': render_scatter,
    'flow': render_flow,
    'txt': render_text
}


def isimage(obj):
    return (
        isinstance(obj, np.ndarray)
        and len(obj.shape) == 3
        and obj.shape[2] in [1, 3, 4]
    )


def isflow(obj):
    return isinstance(obj, np.ndarray) \
        and len(obj.shape) == 3 and obj.shape[2] in [2]


def isscatter(obj):
    return isinstance(obj, np.ndarray) \
        and len(obj.shape) == 2 and obj.shape[1] in [2]


def istext(obj):
    return isinstance(obj, (int, float, str, np.integer, np.float))


def get_default_type(obj):
    if isimage(obj):
        return 'im'
    if isflow(obj):
        return 'flow'
    if isscatter(obj):
        return 'scat'
    return 'txt'
