import os

import dash
import dash_bootstrap_components as dbc
from flask import Flask

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(
    __name__,
    # requests_pathname_prefix="/features/",
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}],
    assets_folder=os.path.join(os.getcwd(), "assets"),
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server
