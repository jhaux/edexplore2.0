from naming import (
    collapse_button_id,
    drop_id,
    collapse_container_id,
    collapse_id
)
from render import RENDERERS

from edflow.util import walk, retrieve

import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State


def example_callbacks(example, dset_handler):
    '''Creates all interactive connections to update and visualize the content
    of examples.'''

    Cooon = Connector(dset_handler)
    walk(example, Cooon, pass_key=True)

    callbacks = Cooon.callbacks
    callbacks['toggle_all'] = {'args': Cooon.toggle_all_ins_and_outs,
                              'callback': ToggleAllCallback(len(callbacks),
                                                            True)}
    return callbacks
        

class Connector:
    '''Gathers a set of callbacks that connect the various components of the
    examples page.
    '''
    def __init__(self, dset_handler):
        self.callbacks = {}
        self.dset = dset_handler

        self.toggle_all_ins_and_outs = {
            'inputs': [Input('toggle_all_button', 'n_clicks')],
            'output': []
        }

    def __call__(self, key, obj):


        self.callbacks[key] = {
            'args': {
                'output': [
                    Output(collapse_container_id(key), 'children'),
                ],
                'inputs': [
                    Input(drop_id(key), 'value'),
                    Input('slider', 'value'),
                ],
                'state': [
                ]
            },
            'callback': SelectorCallback(key, obj, self.dset)
        }

        out = Output(collapse_id(key), 'open')
        self.toggle_all_ins_and_outs['output'] += [out]


class SelectorCallback():
    '''Defines a function, which loads examples and displays them correctly
    given an index and a key.
    '''
    def __init__(self, key, obj, dset_handler):
        '''Each :class:`SelectorCallback` instance is defined by is name
        :attr:`key`. Its setup is done through the initial example :attr:`obj`
        and it has access to new examples through the :attr:`dset_handler`.
        '''
        self.name = key
        self.prime_ex = obj
        self.dset = dset_handler

    def __call__(self,
                 display_selection,
                 example_idx,
                 ):
        '''Makes sure, that the slider changes the displayed example as given
        through :attr:`example_idx` and that the visualization is done using
        the selected renderer :attr:`display_selection`.
        '''

        print('Called {} Callback with {}'.format(
            self.name,
            [
                display_selection,
                example_idx,
            ]
        ))

        # Decide what and how to show
        obj = retrieve(self.dset[example_idx], self.name)

        render, info = RENDERERS[display_selection](obj, self.name)
        info_element = dict2table(info)

        example_body = [
            html.Div(render, className='six columns'),
            html.Div(info_element, className='six columns')
        ]
        return example_body,


class ToggleAllCallback:
    '''Closes or Opens all Detail boxes in the Examples layout'''
    def __init__(self, num_elements, initial_state):
        self.num_elements = num_elements
        self.n_clicks_old = -float('inf')

        self.last_state = initial_state

    def __call__(self, n_clicks):

        new_state = self.last_state
        if n_clicks is not None and n_clicks > self.n_clicks_old:
            new_state = not self.last_state
            self.last_state = new_state

        return [new_state] * self.num_elements


def dict2table(info_dict):
    # Body
    table_content = []
    for k, v in info_dict.items():
        table_content += [html.Tr([html.Td(str(k)), html.Td(str(v))])]
    return html.Table(table_content)
