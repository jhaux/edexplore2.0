import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import dash
import plotly
import plotly.graph_objs as go
import numpy as np
import os

from edflow.data.believers.meta import MetaDataset
from edflow.util import walk, pp2mkdtable

from renderers import render_image, render_scatter


mpath = '/home/jhaux/Dr_J/Projects/VUNet4Bosch/Prjoti_J/'
Ht = MetaDataset(mpath)
Ht.expand = True

Ht.show()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

def layout():
    return html.Div(children=[
        html.H1(children='Hello Dash'),
        dcc.Markdown(Ht.meta['description']),

        html.Div([
        dcc.Slider(
            id='datasource-1',
            value=0,
            min=0,
            max=len(Ht),
            marks={
                0: '0',
                len(Ht): f'{len(Ht)}'
            },
            tooltip={'always_visible': True, 'placement': 'bottom'}
        ),
        ],
                 className='row'),

        # dcc.Markdown(pp2mkdtable(Ht.labels, True)),

        html.Div(
            id='controls-container'
        ),
    ])

app.layout = layout


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
        return 'image'
    if isflow(obj):
        return 'flow'
    if isscatter(obj):
        return 'scatter'
    return 'text'


def get_renderer(type):
    if type == 'image':
        return render_image
    elif type == 'scatter':
        return render_scatter
    else:
        return lambda x, k: (str(x), dict())


def dict2table(info_dict):
    # Body
    table_content = []
    for k, v in info_dict.items():
        table_content += [html.Tr([html.Td(str(k)), html.Td(str(v))])]
    return html.Table(table_content)


class DisplayElements:
    def __init__(self):
        self.elements = []
    def __call__(self, key, obj):

        default_type = get_default_type(obj)
        
        renderer = get_renderer(default_type)
        render, info = renderer(obj, f'{key}-figure')
        info_element = dict2table(info)

        selector = dcc.Dropdown(
            id=drop_id(key),
            options=[
                {'label': 'Image', 'value': 'image'},
                {'label': 'Points', 'value': 'scatter'},
                {'label': 'Flow', 'value': 'flow'},
                {'label': 'Text', 'value': 'text'}
            ],
            value=default_type
        )

        container = html.Div(
            children=[html.Div(render, className='six columns'),
                      html.Div(info_element, className='six columns')],
            id=container_id(key))

        el = html.Div([
            html.H3(key),
            container,
            selector
        ],
        className='row',
        id=key)

        self.elements += [el]


def generate_control_id(value):
    return 'Control {}'.format(value)

def container_id(key):
    return '{}_container'.format(key)

def drop_id(key):
    return '{}_drop_down'.format(key)

class Connector:
    def __init__(self):
        self.callbacks = {}
    def __call__(self, key, obj):
        # Now connect dropdown selects with display
        def display_content(display_selection):
            '''Makes sure, that the slider changes the displayed example.
            '''

            print(f'Called {key} callback with arg {display_selection}')
            renderer = get_renderer(display_selection)
            render, info = renderer(obj, f'{key}-figure')
            info_element = dict2table(info)
            return [html.Div(render, className='six columns'),
                    html.Div(info_element, className='six columns')]

        self.callbacks[key] = {
            'args': {
                'output': Output(container_id(key), 'children'),
                'inputs': [Input(drop_id(key), 'value')],
            },
            'callback': display_content
        }

@app.callback(
    Output('controls-container', 'children'),
    [Input('datasource-1', 'value')])
def display_controls(datasource_1_value):
    '''Makes sure, that the slider changes the displayed example.
    '''

    # Get example
    ex = Ht[int(datasource_1_value)]

    # display leaf variables
    de = DisplayElements()
    walk(ex, de, pass_key=True)
    content = de.elements

    connector = Connector()
    walk(ex, connector, pass_key=True)

    for key, connection in connector.callbacks.items():
        print(key, connection)
        app.callback(**connection['args'])(connection['callback'])

    return html.Div(
            content,
        )


if __name__ == '__main__':
    app.run_server(debug=True)
