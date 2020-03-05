from edflow.util import walk, pp2mkdtable

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from render import OPTIONS, get_default_type
from naming import (
    collapse_container_id,
    drop_id,
    collapse_button_id,
    collapse_id
)


def example_layout(example, num_examples):
    return html.Div([
        html.H1(children='Hello Dash'),

        html.Hr(),

        html.Div(
            [
                html.H6('Select an example:', className='two columns'),
                dcc.Slider(id='slider',
                           value=0,
                           min=0,
                           max=num_examples,
                           marks={0: '0', num_examples: str(num_examples)},
                           tooltip={'always_visible': True,
                                    'placement': 'bottom'},
                           className='eight columns'
                           ),
                dbc.Button('Toggle all', id='toggle_all_button')
            ],
            className='row'
        ),

        html.Hr(),

        html.Div(
            gather_example_layouts(example),
            id='content-container',
        ),
    ])


class DisplayElements:
    def __init__(self):
        self.elements = []

    def __call__(self, key, obj):
        selector = dcc.Dropdown(id=drop_id(key),
                                options=OPTIONS,
                                value=get_default_type(obj),
                                className='row')

        header = html.Summary(html.H4(f'{key}'), style={'list-style': 'none'})
        container = html.Div(id=collapse_container_id(key), className='row')

        el = html.Details([header, selector, container],
                          open=True,
                          id=collapse_id(key),
                          className='row')

        self.elements += [el]


def gather_example_layouts(example):
    Displayor = DisplayElements()

    walk(example, Displayor, pass_key=True)

    return Displayor.elements
