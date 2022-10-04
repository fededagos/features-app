from dash import Dash, dcc, html, Input, Output, no_update
import pandas as pd
import pathlib
import json
import plotly.graph_objects as go
from app import app
from utils.plotting import make_figure, update_on_click, alternative_update

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("all_features.csv"))

fig = make_figure(df, which="waveform")

fig.update_traces(hoverinfo="none", hovertemplate=None)

with open(DATA_PATH.joinpath("iframe_src.txt")) as f:
    data = f.read()

iframe_src = json.loads(data)

layout = html.Div(
    [
        html.Div(
            [
                html.Button("Reset graph", id="reset-wvf-graph", n_clicks=0),
                html.P(),
                dcc.Graph(
                    id="wf-graph",
                    figure=fig,
                    clear_on_unhover=True,
                    style={"height": "75vh"},
                    className="card",
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
                html.P(
                    "Click on a point in the graph to fix it here for further inspection."
                ),
            ],
            id="click-data-wf",
        ),
    ]
)


@app.callback(
    Output(component_id="graph-tip-wf", component_property="show"),
    Output(component_id="graph-tip-wf", component_property="bbox"),
    Output(component_id="graph-tip-wf", component_property="children"),
    Output(component_id="graph-tip-wf", component_property="background_color"),
    Output(component_id="graph-tip-wf", component_property="direction"),
    Input(component_id="wf-graph", component_property="hoverData"),
)
def update_output_div(hoverData):
    if hoverData is None:
        return False, no_update, no_update, no_update, no_update

    properties_dict = hoverData["points"][0]

    bbox = properties_dict["bbox"]
    image_url = (
        "https://files.fededagos.me/individual-plots/"
        + str(properties_dict["customdata"][1])
        + "-wvf.svg"
    )
    dp = properties_dict["customdata"][0].split("/")
    dp = dp[-3] + "/" + dp[-2] + "/" + dp[-1]
    unit = properties_dict["customdata"][1]
    feature_value = properties_dict["customdata"][2]
    title = properties_dict["text"]
    color = properties_dict["customdata"][3]

    x_dist = properties_dict["bbox"]["x0"]

    if x_dist > 500:
        direction = "left"
    else:
        direction = "right"

    children = [
        html.Div(
            [
                html.Img(
                    src=image_url, style={"height": "400px", "background": "white"}
                ),
                html.H2(f"{title}"),
                html.P(f"Path: {dp}"),
                html.P(f"Unit: {unit}"),
                html.P(f"Raw feature Value: {feature_value:.2f}"),
            ],
            style={
                "text-align": "left",
                "color": "black" if title == "PkC_cs" else "white",
            },
        ),
    ]

    return True, bbox, children, color, direction


@app.callback(Output("wf-graph", "clickData"), [Input("reset-wvf-graph", "n_clicks")])
def reset_clickData(n_clicks):
    return None


@app.callback(
    Output(component_id="click-data-wf", component_property="children"),
    Output(component_id="wf-graph", component_property="figure"),
    Input(component_id="wf-graph", component_property="clickData"),
    Input(component_id="wf-graph", component_property="figure"),
)
def update_output_div(input_value, figure):
    if input_value is None:
        return [
            html.Hr(),
            html.H3("Inspect element:"),
            html.P(
                "Click on a point in the graph to fix it here for further inspection."
            ),
        ], fig
    dp = input_value["points"][0]["customdata"][0].split("/")
    dp = dp[-3] + "/" + dp[-2] + "/" + dp[-1]
    unit = input_value["points"][0]["customdata"][1]
    acg_image_url = (
        "https://files.fededagos.me/individual-plots/"
        + str(input_value["points"][0]["customdata"][1])
        + "-acg.svg"
    )
    wvf_image_url = (
        "https://files.fededagos.me/individual-plots/"
        + str(input_value["points"][0]["customdata"][1])
        + "-wvf.svg"
    )
    feat_image_url = (
        "https://files.fededagos.me/individual-plots/"
        + str(input_value["points"][0]["customdata"][1])
        + "-feat.svg"
    )

    opto_plots_url = (
        "https://files.fededagos.me/individual-plots/"
        + str(input_value["points"][0]["customdata"][1])
        + "_opto_plots_combined.svg"
    )

    amplitude_img_url = (
        "https://files.fededagos.me/individual-plots/"
        + str(input_value["points"][0]["customdata"][1])
        + "-amplitudes.png"
    )
    
    try:
        drug_sheet_url = iframe_src[input_value["points"][0]["customdata"][0]]
    except KeyError:
        drug_sheet_url = iframe_src["missing"]

    actual_figure = go.Figure(figure)

    return [
        html.Div(
            [
                html.Hr(),
                html.H4(f"Cell type: {input_value['points'][0]['text']}"),
                html.P(f"Unit {unit} in {dp}"),
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
                        html.Div(
                            className="column",
                            children=[
                                html.Img(
                                    src=feat_image_url,
                                    className="responsive2",
                                ),
                            ],
                        ),
                    ],
                ),
                html.Br(),
                html.P("Amplitude distribution:"),
                html.Img(
                    src=amplitude_img_url,
                    style={
                        "max-width": "75%",
                        "display": "block",
                        "margin-left": "auto",
                        "margin-right": "auto",
                    },
                    className="responsive",
                ),
                html.Hr(),
                html.Details(
                    [
                        html.Summary("Click to show/hide opto plots"),
                        html.Br(),
                        html.Div(
                            [
                                html.Img(src=opto_plots_url, className="responsive"),
                            ]
                        ),
                    ]
                ),
                html.Hr(),
                html.Details(
                    [
                        html.Summary(
                            "Click to show/hide drug efficacy sheet for the corresponding dataset"
                        ),
                        html.Br(),
                        html.Div(
                            [html.Iframe(
                    src=drug_sheet_url,
                    style={
                        "width": "100%",
                        "height": "1000px",
                    },
                )],
                style={"width": "100%", "padding-top": "1%"},
                        ),
                    ]
                ),
            html.Hr(),
            ]
        )
    ], update_on_click(
        actual_figure, df, which="waveform", normalised=True, subselect=unit
    )
