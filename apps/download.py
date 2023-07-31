import urllib

from dash import Input, Output, dcc, html

from app import app

layout = html.Div(
    [
        html.H1(html.Strong("Dataset Download Page"), style={"text-align": "center"}),
        html.Div(
            className="information-container",
            children=[
                html.H2("General information about the datasets"),
                html.P("All datasets are in the `.h5` format, etc..."),
            ],
        ),
        html.Div(
            className="dataset-container",
            children=[
                html.H2("Hausser dataset"),
                html.P(
                    "The Hausser dataset contains both labelled and unlabelled neurons."
                ),
                html.A(
                    "Download Hausser Dataset",
                    id="btn-1",
                    href="https://figshare.com/ndownloader/files/41720781?private_link=9a9dfce1c64cb807fc96",
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
                    "Download Hull labelled dataset",
                    id="btn-2",
                    href="https://figshare.com/ndownloader/files/41720784?private_link=9a9dfce1c64cb807fc96",
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
                    "Download Lisberger dataset",
                    id="btn-3",
                    href="https://figshare.com/ndownloader/files/41721090?private_link=9a9dfce1c64cb807fc96",
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
                    "Download Hull unlabelled dataset",
                    id="btn-4",
                    href="https://figshare.com/ndownloader/files/41720901?private_link=9a9dfce1c64cb807fc96",
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
                    "Download Medina unlabelled dataset",
                    id="btn-5",
                    href="https://figshare.com/ndownloader/files/41721195?private_link=9a9dfce1c64cb807fc96",
                    className="download-button",
                    target="_blank",
                ),
            ],
        ),
    ],
    className="page-container",
)
