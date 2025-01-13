import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State

# Connect to main app.py file
from app import app, server

# Connect to your app pages
from apps import (
    about,
    classifier,
    download,
    explore_features,
    landing,
    temporal_features,
    waveform_features,
)

app.title = "C4 Database"

top_menu = dbc.Navbar(
    id="main-navbar",
    children=dbc.Container(
        [
            dbc.NavbarBrand(
                html.H2("C4 Database", style={"fontWeight": "bold"}),
                href="/apps/about",
                style={"fontWeight": "bold", "white-space": "nowrap"},
                class_name="navbar-heading",
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.NavLink("Download datasets", href="/apps/download"),
                            style={
                                "border-right": "1px solid #dee2e6",
                                "padding-right": "10px",
                                "padding-left": "10px",
                                "white-space": "nowrap",
                            },
                            class_name="navbar-item",
                        ),
                        dbc.NavItem(
                            dbc.NavLink("Classifier", href="/apps/classifier"),
                            style={
                                "border-right": "1px solid #dee2e6",
                                "padding-right": "10px",
                                "padding-left": "10px",
                                "white-space": "nowrap",
                            },
                            class_name="navbar-item",
                        ),
                        dbc.NavItem(
                            dbc.NavLink("About", href="/apps/about"),
                            style={
                                "border-right": "1px solid #dee2e6",
                                "padding-right": "10px",
                                "padding-left": "10px",
                                "white-space": "nowrap",
                            },
                            class_name="navbar-item",
                        ),
                        dbc.DropdownMenu(
                            children=[
                                dbc.DropdownMenuItem(
                                    "Temporal Features", href="/apps/temporal_features", class_name="navbar-item"
                                ),
                                dbc.DropdownMenuItem(divider=True),
                                dbc.DropdownMenuItem(
                                    "Waveform Features", href="/apps/waveform_features", class_name="navbar-item"
                                ),
                                dbc.DropdownMenuItem(divider=True),
                                dbc.DropdownMenuItem(
                                    "Features Explorer", href="/apps/explore_features", class_name="navbar-item"
                                ),
                            ],
                            nav=True,
                            in_navbar=True,
                            label="Explore Neuron Features",
                            style={"white-space": "nowrap", "padding-right": "10px", "padding-left": "10px"},
                            align_end=True,
                            class_name="navbar-dropdown",
                        ),
                    ],
                    className="ml-auto",
                    navbar=True,
                    fill=True,
                    justified=False,
                    style={
                        "text-align": "center",
                    },
                ),
                id="navbar-collapse",
                navbar=True,
                is_open=False,
            ),
        ]
    ),
    color="light",
    dark=False,
    sticky="top",
    className="mb-4",
)


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
    elif pathname == "/apps/classifier":
        return classifier.layout, top_menu
    else:
        return landing.layout, html.Div()


@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    return not is_open if n else is_open


if __name__ == "__main__":
    app.run_server(debug=True, port=8050, host="127.0.0.1")
