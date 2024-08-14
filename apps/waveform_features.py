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
from utils.constants import LAB_CORRESPONDENCE, PLOTS_FOLDER_URL, SELECTED_FEATURES
from utils.plotting import make_joint_figure, update_on_click

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("Nov-14-combined_dashboard.csv"))

fig = make_joint_figure(df, which="waveform", lab="combined_mouse")

fig.update_traces(hoverinfo="none", hovertemplate=None)

with open(DATA_PATH.joinpath("iframe_src.txt"), encoding="utf-8") as f:
    data = f.read()

iframe_src = json.loads(data)

layout = html.Div(
    [
        html.Div(
            [
                dcc.Store(
                    id="lab-choice-waveform",
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
                    id="dataset-choice-waveform",
                    style={
                        "flex-grow": 4,
                        "min-width": "250px",
                        "margin-right": "5px",
                    },
                ),
                html.Button(
                    "Reset graph",
                    id="reset-wvf-graph",
                    n_clicks=0,
                    style={
                        "flex-grow": 1,
                        "margin-left": "5px",
                    },
                ),
                # html.Div(
                #     [
                #         html.Button("Download plot", id="btn-image-wvf", n_clicks=0),
                #         dcc.Download(id="download-image-wvf"),
                #     ],
                #     style={
                #         "flex-grow": 1,
                #         "margin-left": "5px",
                #     },
                # ),
            ],
            className="datasetselect",
        ),
        html.Div(
            [
                dls.Hash(
                    [
                        dcc.Graph(
                            id="wf-graph",
                            figure=fig,
                            clear_on_unhover=True,
                            style={"height": "75vh"},
                            className="graphcard",
                        )
                    ],
                    debounce=300,
                ),
                dcc.Tooltip(
                    id="graph-tip-wf",
                    background_color="white",
                    border_color="white",
                ),
            ],
            id="wvf-graph-container",
            className="wrapperbig",
        ),
        html.Div(
            [
                html.Hr(),
                html.H3("Inspect element:"),
                html.P("Click on a point in the graph to fix it here for further inspection."),
            ],
            id="click-data-wf",
        ),
    ]
)


# @app.callback(
#     Output("download-image-wvf", "data"),
#     Output("btn-image-wvf", "n_clicks"),
#     Input("btn-image-wvf", "n_clicks"),
#     State("wf-graph", "figure"),
#     prevent_initial_call=True,
# )
# def func(n_clicks, figure):
#     time.sleep(0.5)
#     if n_clicks is None or figure is None:
#         return no_update, no_update

#     if n_clicks != 0:
#         fmt = "pdf"
#         filename = f"figure.{fmt}"
#         write_image(figure, "assets/plots/" + filename)
#         return (
#             dcc.send_file(
#                 "./assets/plots/" + filename,
#             ),
#             0,
#         )


@app.callback(
    Output(component_id="graph-tip-wf", component_property="show"),
    Output(component_id="graph-tip-wf", component_property="bbox"),
    Output(component_id="graph-tip-wf", component_property="children"),
    Output(component_id="graph-tip-wf", component_property="background_color"),
    Output(component_id="graph-tip-wf", component_property="direction"),
    Input(component_id="wf-graph", component_property="hoverData"),
)
def update_hover(hoverData):
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
            style={
                "text-align": "left",
                "color": "white",
            },
        ),
    ]

    return True, bbox, children, color, direction


@app.callback(
    Output("wf-graph", "clickData"),
    Output("dataset-choice-waveform", "value"),
    Input("reset-wvf-graph", "n_clicks"),
)
def reset_click_data(n_clicks):
    return None, "Combined mouse data"


@app.callback(
    Output(component_id="click-data-wf", component_property="children"),
    Output(component_id="wf-graph", component_property="figure"),
    Output(component_id="lab-choice-waveform", component_property="data"),
    Input(component_id="wf-graph", component_property="clickData"),
    Input(component_id="wf-graph", component_property="figure"),
    Input(component_id="dataset-choice-waveform", component_property="value"),
    State(component_id="lab-choice-waveform", component_property="data"),
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
            make_joint_figure(df, which="waveform", lab=store_data["lab"][-1]),
            store_data,
        )
    dp = input_value["points"][0]["customdata"][0].split("/")
    dp = dp[-1]
    unit = input_value["points"][0]["customdata"][1]
    plotting_id = input_value["points"][0]["customdata"][4]

    acg_image_url = get_asset_url(PLOTS_FOLDER_URL + str(plotting_id) + "-acg.svg")
    wvf_image_url = get_asset_url(PLOTS_FOLDER_URL + str(plotting_id) + "-wvf.svg")
    feat_image_url = get_asset_url(PLOTS_FOLDER_URL + str(plotting_id) + "-feat.svg")
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
                                className="column",
                                children=[
                                    html.Img(
                                        src=acg_image_url,
                                        className="responsivesvg",
                                    )
                                ],
                            ),
                            html.Div(
                                className="column",
                                children=[
                                    html.Img(
                                        src=wvf_image_url,
                                        className="responsivesvg",
                                    ),
                                ],
                            ),
#                             html.Div(
#                                 className="column",
#                                 children=[
#                                     html.Img(
#                                         src=feat_image_url,
#                                         className="responsive2",
#                                     ),
#                                 ],
#                             ),
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
            which="waveform",
            normalised=True,
            subselect=plotting_id,
            lab=lab_id,
        ),
        store_data,
    )
