from dash import Dash, Input, Output, dcc, html, no_update
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app, server

# Connect to your app pages
from apps import (
    about,
    download,
    explore_features,
    landing,
    temporal_features,
    waveform_features,
)

app.title = "Feature plots"

top_menu = [
    html.Div(html.H1(html.Strong("C4 Database")), style={"text-align": "center"}),
    html.Div(
        [
            dcc.Link(
                "Temporal Features",
                href="/apps/temporal_features",
                className="tab first",
            ),
            dcc.Link(
                "Waveform Features",
                href="/apps/waveform_features",
                className="tab",
            ),
            dcc.Link("Features Explorer", href="/apps/explore_features", className="tab"),
            dcc.Link("Download datasets", href="/apps/download", className="tab"),
            dcc.Link("About", href="/apps/about", className="tab"),
        ],
        className="wrapper",
    ),
    html.Br(),
]

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="top-menu", children=top_menu),
        html.Div(id="page-content", children=[]),
    ]
)


@app.callback(Output("page-content", "children"), Output("top-menu", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/apps/about":
        return about.layout, top_menu
    elif pathname == "/apps/explore_features":
        return explore_features.layout, top_menu
    elif pathname == "/apps/waveform_features":
        return waveform_features.layout, top_menu
    elif pathname == "/apps/temporal_features":
        return temporal_features.layout, top_menu
    elif pathname == "/apps/download":
        return download.layout, top_menu
    else:
        return landing.layout, html.Div()


if __name__ == "__main__":
    app.run_server(debug=True, port=8050, host="127.0.0.1")
