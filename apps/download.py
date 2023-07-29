import urllib

from dash import Input, Output, dcc, html

from app import app

layout = html.Div(
    [
        html.H1("Dataset Download Page"),
        html.Div(
            className="dataset-container",
            children=[
                html.H2("Hausser dataset"),
                html.P("Description of dataset 1"),
                html.A(
                    "Download Dataset 1",
                    id="btn-1",
                    href="https://figshare.com/s/9a9dfce1c64cb807fc96",
                    className="download-button",
                    target="_blank",
                ),
            ],
        ),
        html.Div(
            className="dataset-container",
            children=[
                html.H2("Hull labelled dataset"),
                html.P("Description of dataset 2"),
                html.A(
                    "Download Dataset 2",
                    id="btn-2",
                    href="",
                    className="download-button",
                    target="_blank",
                ),
            ],
        ),
        html.Div(
            className="dataset-container",
            children=[
                html.H2("Lisberger dataset"),
                html.P("Description of dataset 3"),
                html.A(
                    "Download Dataset 3",
                    id="btn-3",
                    href="",
                    className="download-button",
                    target="_blank",
                ),
            ],
        ),
        html.Div(
            className="dataset-container",
            children=[
                html.H2("Hull unlabelled dataset"),
                html.P("Description of dataset 4"),
                html.A(
                    "Download Dataset 4",
                    id="btn-4",
                    href="",
                    className="download-button",
                    target="_blank",
                ),
            ],
        ),
        html.Div(
            className="dataset-container",
            children=[
                html.H2("Medina unlabelled dataset"),
                html.P("Description of dataset 5"),
                html.A(
                    "Download Dataset 5",
                    id="btn-5",
                    href="",
                    className="download-button",
                    target="_blank",
                ),
            ],
        ),
    ],
    className="page-container",
)
