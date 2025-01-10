import json
import pathlib
import time

import dash_loading_spinners as dls
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State, dcc, get_asset_url, html, no_update
from plotly.io import write_image

from app import app
from apps.footer import make_footer
from utils.constants import LAB_CORRESPONDENCE, PLOTS_FOLDER_URL
from utils.plotting import make_joint_figure, update_on_click

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
PLOT_PATH = PATH.joinpath("../assets/plots").resolve()

df = pd.read_csv(DATA_PATH.joinpath("Nov-14-combined_dashboard.csv"))

fig = make_joint_figure(df, which="temporal", lab="combined_mouse")

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
                            id="lab-choice-temporal",
                            data={"lab": ["combined_mouse"]},
                        ),
                        dcc.Dropdown(
                            [
                                "Combined mouse data",
                                "Hausser data",
                                "Hull data",
                                "Lisberger data (macaque)",
                            ],
                            "Combined mouse data",
                            searchable=False,
                            clearable=False,
                            id="dataset-choice-temporal",
                            style={
                                "flex-grow": 4,
                                "min-width": "250px",
                                "margin-right": "5px",
                            },
                        ),
                        html.Button(
                            "Reset graph",
                            id="reset-graph",
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
                        dls.Hash(
                            [
                                dcc.Graph(
                                    id="graph",
                                    figure=fig,
                                    clear_on_unhover=True,
                                    style={"height": "75vh"},
                                    className="graphcard",
                                ),
                            ],
                            debounce=300,
                        ),
                        dcc.Tooltip(
                            id="graph-tip",
                            background_color="white",
                            border_color="white",
                            direction="bottom",
                        ),
                    ],
                    id="graph-container",
                    className="wrapperbig",
                ),
                html.Div(
                    [
                        html.Hr(),
                        html.H3("Inspect element:"),
                        html.P("Click on a point in the graph to fix it here for further inspection."),
                    ],
                    id="click-data",
                ),
            ],
            className="large-screen-content",
        ),
    ],
    className="responsive-container",
)


@app.callback(
    Output("graph", "clickData"),
    Output("dataset-choice-temporal", "value"),
    [Input("reset-graph", "n_clicks")],
)
def reset_click_data(n_clicks):
    return None, "Combined mouse data"


@app.callback(
    Output(component_id="graph-tip", component_property="show"),
    Output(component_id="graph-tip", component_property="bbox"),
    Output(component_id="graph-tip", component_property="children"),
    Output(component_id="graph-tip", component_property="background_color"),
    Output(component_id="graph-tip", component_property="direction"),
    Input(component_id="graph", component_property="hoverData"),
)
def update_graphtip(hoverData):
    if hoverData is None:
        return False, no_update, no_update, no_update, no_update

    properties_dict = hoverData["points"][0]

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

    image_url = get_asset_url(PLOTS_FOLDER_URL + str(plotting_id) + "-acg.svg")

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
            style={
                "text-align": "left",
                "color": "white",
            },
        ),
    ]

    return True, bbox, children, color, direction


@app.callback(
    Output(component_id="click-data", component_property="children"),
    Output(component_id="graph", component_property="figure"),
    Output(component_id="lab-choice-temporal", component_property="data"),
    Input(component_id="graph", component_property="clickData"),
    Input(component_id="graph", component_property="figure"),
    Input(component_id="dataset-choice-temporal", component_property="value"),
    Input(component_id="lab-choice-temporal", component_property="data"),
)
def update_figure(input_value, figure, lab, store_data):
    # Check if user requested for a lab data input change
    lab_correspondence = LAB_CORRESPONDENCE
    lab_id = lab_correspondence[lab]
    store_data["lab"].append(lab_id)
    lab_changed = store_data["lab"][-1] != store_data["lab"][-2]

    if input_value is None and not lab_changed:
        return (
            [
                html.Hr(),
                html.H3("Inspect element:"),
                html.P("Click on a point in the graph to fix it here for further inspection."),
            ],
            fig,
            store_data,
        )
    elif lab_changed:
        return (
            [
                html.Hr(),
                html.H3("Inspect element:"),
                html.P("Click on a point in the graph to fix it here for further inspection."),
            ],
            make_joint_figure(df, which="temporal", lab=store_data["lab"][-1]),
            store_data,
        )

    dp = input_value["points"][0]["customdata"][0].split("/")
    dp = dp[-1]
    unit = input_value["points"][0]["customdata"][1]
    plotting_id = input_value["points"][0]["customdata"][4]
    acg_image_url = get_asset_url(PLOTS_FOLDER_URL + str(plotting_id) + "-acg.svg")
    wvf_image_url = get_asset_url(PLOTS_FOLDER_URL + str(plotting_id) + "-wvf.svg")
    amplitude_img_url = get_asset_url(PLOTS_FOLDER_URL + str(plotting_id) + "-amplitudes.png")
    cell_type = input_value["points"][0]["text"]

    # All hull data has a plotting id greater than 1000
    if int(plotting_id) < 1000 and not (cell_type in ["PkC_ss", "PkC_cs"] and "YC001" not in dp):
        opto_plots_url = get_asset_url(PLOTS_FOLDER_URL + str(plotting_id) + "_opto_plots_combined.png")

    elif cell_type in ["PkC_ss", "PkC_cs"] and "YC001" not in dp:
        opto_plots_url = get_asset_url(PLOTS_FOLDER_URL + "purkinje_cell.png")

    else:
        opto_plots_url = get_asset_url(PLOTS_FOLDER_URL + "opto_plots_unavailable.png")

    actual_figure = go.Figure(figure)
    return (
        [
            html.Div(
                [
                    html.Hr(),
                    html.H4(["Cell type: ", html.Strong(input_value["points"][0]["text"])]),
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
                    *make_footer(amplitude_img_url, opto_plots_url),
                ]
            )
        ],
        update_on_click(
            actual_figure,
            df,
            which="temporal",
            normalised=True,
            subselect=plotting_id,
            lab=lab_id,
        ),
        store_data,
    )
