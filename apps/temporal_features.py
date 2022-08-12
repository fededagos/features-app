from dash import Dash, dcc, html, Input, Output, no_update
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import pathlib
from app import app
from utils.plotting import make_figure, update_on_click

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("all_features.csv"))

fig = make_figure(df, which="temporal")

layout = html.Div(
    [
        html.Div(
            [
                dcc.Graph(
                    id="graph",
                    figure=fig,
                    clear_on_unhover=True,
                    style={"height": "75vh"},
                    className = 'card'
                ),
                dcc.Tooltip(
                    id="graph-tip",
                    background_color="white",
                    border_color="white",
                    direction="bottom",
                ),
            ]
        ),
        html.Div(
            [
                html.Hr(),
                html.H3("Inspect element:"),
                html.P(
                    "Click on a point in the graph to fix it here for further inspection."
                ),
            ],
            id="click-data",
        ),
    ]
)


@app.callback(
    Output(component_id="graph-tip", component_property="show"),
    Output(component_id="graph-tip", component_property="bbox"),
    Output(component_id="graph-tip", component_property="children"),
    Output(component_id="graph-tip", component_property="background_color"),
    Output(component_id="graph-tip", component_property="direction"),
    Input(component_id="graph", component_property="hoverData"),
)
def update_output_div(hoverData):
    if hoverData is None:
        return False, no_update, no_update, no_update, no_update

    properties_dict = hoverData["points"][0]

    bbox = properties_dict["bbox"]
    image_url = (
        "https://files.fededagos.me/individual-plots/"
        + str(properties_dict["customdata"][1])
        + "-acg.jpg"
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
                html.Img(src=image_url, style={"width": "60%"}),
                html.H2(f"{title}"),
                html.P(f"Path: {dp}"),
                html.P(f"Unit: {unit}"),
                html.P(f"Raw feature Value: {feature_value:.2f}"),
            ],
            style={"color": "black" if title == "PkC_cs" else "white"},
        ),
    ]

    return True, bbox, children, color, direction


@app.callback(
    Output(component_id="click-data", component_property="children"),
    Output(component_id="graph", component_property="figure"),
    Input(component_id="graph", component_property="clickData"),
    Input(component_id="graph", component_property="figure"),
)
def update_output_div(input_value, figure):

    if input_value is None:
        return no_update, no_update

    dp = input_value["points"][0]["customdata"][0].split("/")
    dp = dp[-3] + "/" + dp[-2] + "/" + dp[-1]
    unit = input_value["points"][0]["customdata"][1]
    acg_image_url = (
        "https://files.fededagos.me/individual-plots/"
        + str(input_value["points"][0]["customdata"][1])
        + "-acg.jpg"
    )
    wvf_image_url = (
        "https://files.fededagos.me/individual-plots/"
        + str(input_value["points"][0]["customdata"][1])
        + "-wvf.jpg"
    )

    opto_plots_url = (
        "https://files.fededagos.me/individual-plots/"
        + str(input_value["points"][0]["customdata"][1])
        + "_opto_plots_combined.jpg"
    )

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
                            className="column2",
                            children=[
                                html.Img(
                                    src=acg_image_url,
                                    className="responsive",
                                )
                            ],
                        ),
                        html.Div(
                            className="column2",
                            children=[
                                html.Img(
                                    src=wvf_image_url,
                                    className="responsive",
                                ),
                            ],
                        ),
                    ],
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
            ]
        )
    ], update_on_click(
        actual_figure, df, which="temporal", normalised=True, subselect=unit
    )
