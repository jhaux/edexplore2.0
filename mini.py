from edflow.util import walk, pp2mkdtable

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import dash
import plotly
import plotly.graph_objs as go

from layouts import example_layout
from naming import container_id, drop_id
from interact import example_callbacks
from dset import DsetHandler


class Edexplore():
    def __init__(self, dataset):
        '''
        Parameters
        ----------
        dataset : DatasetMixin
            The data we want to take a look at.
        '''

        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        
        self.app = dash.Dash(__name__,
                             external_stylesheets=external_stylesheets)
        # self.app.config.suppress_callback_exceptions = True

        self.base_example = dataset[0]

        self.app.layout = example_layout(self.base_example, len(dataset))

        self.dset_handler = DsetHandler(dataset)

        self.setup_callbacks(self.base_example)

    def setup_callbacks(self, example):
        callbacks = example_callbacks(example, self.dset_handler)

        for name, connection in callbacks.items():
            self.app.callback(**connection['args'])(connection['callback'])
  
  
if __name__ == '__main__':

    from edflow.data.believers.meta import MetaDataset
    
    mpath = '/home/jhaux/Dr_J/Projects/VUNet4Bosch/Prjoti_J/'
    Ht = MetaDataset(mpath)
    Ht.expand = True
    
    Ht.show()

    E = Edexplore(Ht)
    E.app.run_server(debug=True)
