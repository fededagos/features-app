import json
import pathlib

import dash_loading_spinners as dls
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from dash import Input, Output, State, dcc, get_asset_url, html, no_update

from app import app
from apps.footer import make_footer
from utils.constants import (
    LAB_CORRESPONDENCE,
    PLOTS_FOLDER_URL,
    SELECTED_FEATURES,
    TEMPORAL_FEATURES,
)
from utils.plotting import make_joint_figure, update_on_click

pio.kaleido.scope.mathjax = None

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("18-03-2025_combined_dashboard.csv"))

with open(DATA_PATH.joinpath("iframe_src.txt"), encoding="utf-8") as f:
    data = f.read()

iframe_src = json.loads(data)

layout = html.Div(
    [
        # Small screen message
        html.Div(
            "Access the dashboard from a device with a larger display to interact with the plots.",
            className="small-screen-message",
        ),
        # Original content wrapped in a container
        html.Div(
            [
                html.Div(
                    [
                        dcc.Store(
                            id="store",
                            data={"input_changed": [0], "norm_changed": [1], "lab": ["combined_mouse"]},
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    [
                                        "Combined mouse data",
                                        "Hausser data",
                                        "Hull data",
                                        "Lisberger data (macaque)",
                                        "All data",
                                    ],
                                    "Combined mouse data",
                                    searchable=False,
                                    clearable=False,
                                    id="dataset-choice-feature",
                                    style={
                                        "flex-grow": 4,
                                        "min-width": "250px",
                                        "margin-right": "5px",
                                    },
                                ),
                                html.Button(
                                    "Reset graph",
                                    id="reset-feature-graph",
                                    n_clicks=0,
                                    style={
                                        "flex-grow": 1,
                                        "margin-left": "5px",
                                    },
                                ),
                            ],
                            className="datasetselect",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            options=[{"label": v, "value": k} for k, v in SELECTED_FEATURES.items()],
                                            id="feature-dropdown",
                                            placeholder="Select one or more features to plot...",
                                            multi=True,
                                            style={
                                                "flex-grow": 1,
                                                "margin-right": "5px",
                                                "min-width": "50vw",
                                            },
                                        ),
                                        dcc.RadioItems(
                                            ["Normalised", "Raw values"],
                                            "Normalised",
                                            id="yaxis-type",
                                            inline=True,
                                            labelStyle={"display": "inline-block", "margin-right": "20px"},
                                            style={"flex-grow": 0, "margin-left": "5px"},
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "flex-wrap": "wrap",
                                        "margin": "5px",
                                        "justify-content": "center",
                                        "max-width": "80vw",
                                        "margin-left": "auto",
                                        "margin-right": "auto",
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            [
                                dls.Hash(
                                    [
                                        dcc.Graph(
                                            id="feature-graph",
                                            figure=go.Figure(),
                                            clear_on_unhover=True,
                                            style={"height": "75vh"},
                                            className="graphcard",
                                        ),
                                    ],
                                    debounce=300,
                                ),
                                dcc.Tooltip(
                                    id="graph-tip-features",
                                    background_color="white",
                                    border_color="white",
                                ),
                            ],
                            id="dropdown-selection",
                            className="wrapperbig",
                        ),
                        html.Div(
                            [
                                html.Hr(),
                                html.H3("Inspect element:"),
                                html.P("Click on a point in the graph to fix it here for further inspection."),
                            ],
                            id="click-data-features",
                        ),
                    ],
                ),
            ],
            className="large-screen-content",
        ),
    ],
    className="responsive-container",
)


@app.callback(
    Output(component_id="graph-tip-features", component_property="show"),
    Output(component_id="graph-tip-features", component_property="bbox"),
    Output(component_id="graph-tip-features", component_property="children"),
    Output(component_id="graph-tip-features", component_property="background_color"),
    Output(component_id="graph-tip-features", component_property="direction"),
    Input(component_id="feature-graph", component_property="hoverData"),
)
def update_hover(hoverData):
    if hoverData is None:
        return False, no_update, no_update, no_update, no_update

    properties_dict = hoverData["points"][0]
    which_feature = properties_dict["x"]

    bbox = properties_dict["bbox"]
    dp = properties_dict["customdata"][0].split("/")
    dp = dp[-1]
    unit = properties_dict["customdata"][1]
    feature_value = properties_dict["customdata"][2]
    title = properties_dict["text"]
    color = properties_dict["customdata"][3]
    plotting_id = properties_dict["customdata"][4]
    cerebellum_layer = properties_dict["customdata"][5]
    feature_name = properties_dict["customdata"][6]

    # If hovering on a temporal feature show the ACG, otherwise show the waveform
    if which_feature in set(TEMPORAL_FEATURES):
        image_url = get_asset_url(PLOTS_FOLDER_URL + str(plotting_id) + "-acg.svg")
    else:
        image_url = get_asset_url(PLOTS_FOLDER_URL + str(plotting_id) + "-wvf.svg")

    x_dist = properties_dict["bbox"]["x0"]

    direction = "left" if x_dist > 500 else "right"

    children = [
        html.Div(
            [
                html.Img(
                    src=image_url,
                    style={
                        "min-width": "250px",
                        "max-width": "70%",
                        "max-height": "400px",
                        "background": "white",
                    },
                ),
                html.H2(f"{title}"),
                html.P(f"Path: {dp}"),
                html.P(f"Unit: {unit}"),
                html.P(f"Cerebellar layer: {cerebellum_layer}"),
                html.P(f"{feature_name}: {feature_value:.2f}"),
            ],
            style={"color": "white"},
        ),
    ]

    return True, bbox, children, color, direction


@app.callback(
    Output(component_id="click-data-features", component_property="children"),
    Output(component_id="feature-graph", component_property="figure"),
    Output(component_id="store", component_property="data"),
    Output(component_id="feature-graph", component_property="clickData"),
    Output("reset-feature-graph", "n_clicks"),
    Output("dataset-choice-feature", "value"),
    Output("feature-dropdown", "value"),
    Input(component_id="feature-graph", component_property="clickData"),
    Input("feature-dropdown", "value"),
    Input("yaxis-type", "value"),
    Input("feature-graph", "figure"),
    Input(component_id="dataset-choice-feature", component_property="value"),
    Input("reset-feature-graph", "n_clicks"),
    State("store", "data"),
)
def update_figure(click_input, value, normalised, figure, lab, clicks, store):
    # The first and easiest thing to implement is the reset button
    if clicks > 0:
        return (
            [
                html.Hr(),
                html.H3("Inspect element:"),
                html.P("Click on a point in the graph to fix it here for further inspection."),
            ],
            go.Figure(),
            store,
            None,
            0,
            "Hausser data",
            None,
        )

    # Check if user requested for a lab data input change
    lab_correspondence = LAB_CORRESPONDENCE
    lab_id = lab_correspondence[lab]
    store["lab"].append(lab_id)
    lab_changed = store["lab"][-1] != store["lab"][-2]

    if value is not None and len(value) != 0:
        store["input_changed"].append(len(value))
        store["norm_changed"].append(int(normalised == "Normalised"))
    else:
        store["input_changed"] = [0]

        return (
            [
                html.Hr(),
                html.H3("Inspect element:"),
                html.P("Click on a point in the graph to fix it here for further inspection."),
            ],
            go.Figure(),
            store,
            None,
            no_update,
            no_update,
            no_update,
        )

    norm_changed = store["norm_changed"][-1] != store["norm_changed"][-2] if len(store["norm_changed"]) > 2 else False

    input_changed = (
        store["input_changed"][-1] != store["input_changed"][-2] if len(store["input_changed"]) > 2 else False
    )

    if click_input is None or lab_changed:
        use_normalised = normalised == "Normalised"
        features = list(value)
        actual_figure = make_joint_figure(df, which=features, normalised=use_normalised, lab=lab_id)
        return no_update, actual_figure, store, None, no_update, no_update, no_update

    elif not input_changed and not norm_changed:
        dp = click_input["points"][0]["customdata"][0].split("/")
        dp = dp[-1]
        unit = click_input["points"][0]["customdata"][1]
        plotting_id = click_input["points"][0]["customdata"][4]

        acg_image_url = get_asset_url(PLOTS_FOLDER_URL + str(plotting_id) + "-acg.svg")
        wvf_image_url = get_asset_url(PLOTS_FOLDER_URL + str(plotting_id) + "-wvf.svg")
        amplitude_img_url = get_asset_url(PLOTS_FOLDER_URL + str(plotting_id) + "-amplitudes.png")
        cell_type = click_input["points"][0]["text"]

        # All hull data has a plotting id greater than 1000
        if int(plotting_id) < 1000 and (cell_type not in ["PkC_ss", "PkC_cs"] or "YC001" in dp):
            opto_plots_url = get_asset_url(PLOTS_FOLDER_URL + str(plotting_id) + "_opto_plots_combined.png")

        elif cell_type in ["PkC_ss", "PkC_cs"] and "YC001" not in dp:
            opto_plots_url = get_asset_url(PLOTS_FOLDER_URL + "purkinje_cell.png")

        else:
            opto_plots_url = get_asset_url(PLOTS_FOLDER_URL + "opto_plots_unavailable.png")

        use_normalised = normalised == "Normalised"
        features = list(value)
        actual_figure = go.Figure(figure)

        footer = make_footer(amplitude_img_url, opto_plots_url) if cell_type != "GrC" else [html.Hr()]

        return (
            [
                html.Div(
                    [
                        html.Hr(),
                        html.H4(f"Cell type: {click_input['points'][0]['text']}"),
                        html.P(f"Unit {unit} in {dp}"),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="column2",
                                    children=[
                                        html.Img(
                                            src=acg_image_url,
                                            className="responsivesvg",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="column2",
                                    children=[
                                        html.Img(
                                            src=wvf_image_url,
                                            className="responsivesvg",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Br(),
                        *footer,
                    ],
                    style={"padding": "20px"},
                )
            ],
            update_on_click(
                actual_figure,
                df,
                which=features,
                normalised=use_normalised,
                subselect=plotting_id,
                lab=lab_id,
            ),
            store,
            click_input,
            no_update,
            no_update,
            no_update,
        )
    else:
        dp = click_input["points"][0]["customdata"][0].split("/")
        dp = dp[-1]
        unit = click_input["points"][0]["customdata"][1]
        plotting_id = click_input["points"][0]["customdata"][4]
        cell_type = click_input["points"][0]["text"]

        acg_image_url = get_asset_url(PLOTS_FOLDER_URL + str(plotting_id) + "-acg.svg")
        wvf_image_url = get_asset_url(PLOTS_FOLDER_URL + str(plotting_id) + "-wvf.svg")

        if int(plotting_id) < 1000 and (cell_type not in ["PkC_ss", "PkC_cs"] or "YC001" in dp):
            opto_plots_url = get_asset_url(PLOTS_FOLDER_URL + str(plotting_id) + "_opto_plots_combined.png")

        elif cell_type in ["PkC_ss", "PkC_cs"] and "YC001" not in dp:
            opto_plots_url = get_asset_url(PLOTS_FOLDER_URL + "purkinje_cell.png")

        else:
            opto_plots_url = get_asset_url(PLOTS_FOLDER_URL + "opto_plots_unavailable.png")

        amplitude_img_url = get_asset_url(PLOTS_FOLDER_URL + str(plotting_id) + "-amplitudes.png")

        use_normalised = normalised == "Normalised"
        features = list(value)
        actual_figure = make_joint_figure(df, which=features, normalised=use_normalised, lab=lab_id)

        footer = make_footer(amplitude_img_url, opto_plots_url) if cell_type != "GrC" else [html.Hr()]

        return (
            [
                html.Div(
                    [
                        html.Hr(),
                        html.H4(
                            [
                                "Cell type: ",
                                html.Strong(click_input["points"][0]["text"]),
                            ]
                        ),
                        html.H5(f"Unit {unit} in {dp}"),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="column2",
                                    children=[
                                        html.Img(
                                            src=acg_image_url,
                                            className="responsivesvg",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="column2",
                                    children=[
                                        html.Img(
                                            src=wvf_image_url,
                                            className="responsivesvg",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Br(),
                        *footer,
                    ]
                )
            ],
            update_on_click(
                actual_figure,
                df,
                which=features,
                normalised=use_normalised,
                subselect=plotting_id,
                lab=lab_id,
            ),
            store,
            click_input,
            no_update,
            no_update,
            no_update,
        )
