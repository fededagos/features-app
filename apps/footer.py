from dash import Dash, dcc, html, Input, Output, State, no_update
import pandas as pd
import pathlib
import json
from app import app
from utils.plotting import make_figure, update_on_click
import plotly.graph_objects as go


def make_footer(amplitude_img_url, opto_plots_url, drug_sheet_url):
    return [html.P("Amplitude distribution:"), html.Img(src=amplitude_img_url, style={"max-width": "75%", "display": "block", "margin-left": "auto", "margin-right": "auto",}, className="responsive",), html.Hr(), html.Details([html.Summary("Click to show/hide opto plots"), html.Br(), html.Div([html.Img(src=opto_plots_url, className="responsive",),]),]), html.Hr(), html.Details([html.Summary("Click to show/hide drug efficacy sheet for the corresponding dataset"), html.Br(), html.P("Note: formatting in the embedded Google Sheet may be off. \
                    If this is the case, just switch blocker sheet tabs back and fort or click on another point to fix it. \
                    Alternatively, you can open the sheet in a new browser tab by clicking on the corresponding links."), html.Div([html.Iframe(src=drug_sheet_url, style={"width": "100%", "height": "1000px",},)], style={"width": "100%", "padding-top": "1%"},),]), html.Hr(),]
