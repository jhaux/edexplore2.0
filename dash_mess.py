import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import dash
import plotly
import plotly.graph_objs as go
import numpy as np


from edflow.data.believers.meta import MetaDataset
from edflow.util import walk, pp2mkdtable

Ht = MetaDataset('/home/jhaux/remote/cg2/export/scratch/jhaux/Data/human gait/meta_dset')
Ht.expand = True

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
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


def isimage(obj):
    return (
        isinstance(obj, np.ndarray)
        and len(obj.shape) == 3
        and obj.shape[2] in [1, 3, 4]
    )


def isflow(obj):
    return isinstance(obj, np.ndarray) and len(obj.shape) == 3 and obj.shape[2] in [2]


def istext(obj):
    return isinstance(obj, (int, float, str, np.integer, np.float))


def get_default_type(obj):
    if isimage(obj):
        return 'image'
    if isflow(obj):
        return 'flow'
    return 'text'


class DisplayElements:
    def __init__(self):
        self.elements = []
    def __call__(self, key, obj):

        default_type = get_default_type(obj)
        
        el = html.Div([
            html.H3(key),
            html.Div(str(obj)),
            dcc.Dropdown(
                id=f'{key}-dropdown',
                options=[
                    {'label': 'image', 'value': 'image'},
                    {'label': 'Flow', 'value': 'flow'},
                    {'label': 'Text', 'value': 'text'}
                ],
            value=default_type
            )
        ],
        className='row',
        id=key)

        self.elements += [el]


def generate_control_id(value):
    return 'Control {}'.format(value)

@app.callback(
    Output('controls-container', 'children'),
    [Input('datasource-1', 'value')])
def display_controls(datasource_1_value):
    # generate 2 dynamic controls based off of the datasource selections
    ex = Ht[int(datasource_1_value)]
    de = DisplayElements()
    walk(ex, de, pass_key=True)
    content = de.elements
    print(content)
    return html.Div(
            content,
        )


if __name__ == '__main__':
    app.run_server(debug=True)
