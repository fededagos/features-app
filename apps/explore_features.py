from dash import Dash, dcc, html, Input, Output, State, no_update
import pandas as pd
import pathlib
from app import app
from utils.plotting import make_figure, update_on_click
import plotly.graph_objects as go

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("all_features.csv"))

layout = html.Div(
    [
        dcc.Store(id="store", data={"input_changed": False}),
        html.Div(
            [
                dcc.Dropdown(
                    df["feature"].unique(),
                    id="feature-dropdown",
                    placeholder="Select one or more features to plot...",
                    multi=True,
                ),
                dcc.RadioItems(
                    ["Normalised", "Raw values"],
                    "Normalised",
                    id="yaxis-type",
                    inline=True,
                ),
            ],
        ),
        html.Div(
            [
                dcc.Graph(
                    id="feature-graph",
                    figure=go.Figure(),
                    clear_on_unhover=True,
                    style={"height": "75vh"},
                    className="card",
                ),
                dcc.Tooltip(
                    id="graph-tip-features",
                    background_color="white",
                    border_color="white",
                ),
            ],
            id="dropdown-selection",
        ),
        html.Div(
            [
                html.Hr(),
                html.H3("Inspect element:"),
                html.P(
                    "Click on a point in the graph to fix it here for further inspection."
                ),
            ],
            id="click-data-features",
        ),
    ]
)


@app.callback(
    Output(component_id="graph-tip-features", component_property="show"),
    Output(component_id="graph-tip-features", component_property="bbox"),
    Output(component_id="graph-tip-features", component_property="children"),
    Output(component_id="graph-tip-features", component_property="background_color"),
    Output(component_id="graph-tip-features", component_property="direction"),
    Input(component_id="feature-graph", component_property="hoverData"),
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
            style={"color": "black" if title == "PkC_cs" else "white"},
        ),
    ]

    return True, bbox, children, color, direction


@app.callback(
    Output(component_id="click-data-features", component_property="children"),
    Output(component_id="feature-graph", component_property="figure"),
    Output(component_id="store", component_property="data"),
    Input(component_id="feature-graph", component_property="clickData"),
    Input("feature-dropdown", "value"),
    Input("yaxis-type", "value"),
    Input("feature-graph", "figure"),
    State("store", "data"),
)
def update_output_div(click_input, value, normalised, figure, store):

    if value is not None and len(value) != 0:
        store["input_changed"] = True
    elif value is None or len(value) == 0:
        store["input_changed"] = False
        return html.P("Hellooo"), go.Figure(), store

    if click_input is None:
        use_normalised = True if normalised == "Normalised" else False
        features = list(value)
        actual_figure = make_figure(df, which=features, normalised=use_normalised)
        return no_update, actual_figure, store
    elif click_input is not None and not store["input_changed"]:
        dp = click_input["points"][0]["customdata"][0].split("/")
        dp = dp[-3] + "/" + dp[-2] + "/" + dp[-1]
        unit = click_input["points"][0]["customdata"][1]
        acg_image_url = (
            "https://files.fededagos.me/individual-plots/"
            + str(click_input["points"][0]["customdata"][1])
            + "-acg.svg"
        )
        wvf_image_url = (
            "https://files.fededagos.me/individual-plots/"
            + str(click_input["points"][0]["customdata"][1])
            + "-wvf.svg"
        )

        opto_plots_url = (
            "https://files.fededagos.me/individual-plots/"
            + str(click_input["points"][0]["customdata"][1])
            + "_opto_plots_combined.svg"
        )

        use_normalised = True if normalised == "Normalised" else False
        features = list(value)
        actual_figure = go.Figure(figure)

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
                                        html.Img(
                                            src=opto_plots_url, className="responsive"
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ]
                )
            ],
            update_on_click(
                actual_figure, df, which=features, normalised=True, subselect=unit
            ),
            store,
        )
    elif click_input is not None and store["input_changed"]:
        dp = click_input["points"][0]["customdata"][0].split("/")
        dp = dp[-3] + "/" + dp[-2] + "/" + dp[-1]
        unit = click_input["points"][0]["customdata"][1]
        acg_image_url = (
            "https://files.fededagos.me/individual-plots/"
            + str(click_input["points"][0]["customdata"][1])
            + "-acg.svg"
        )
        wvf_image_url = (
            "https://files.fededagos.me/individual-plots/"
            + str(click_input["points"][0]["customdata"][1])
            + "-wvf.svg"
        )

        opto_plots_url = (
            "https://files.fededagos.me/individual-plots/"
            + str(click_input["points"][0]["customdata"][1])
            + "_opto_plots_combined.svg"
        )

        use_normalised = True if normalised == "Normalised" else False
        features = list(value)
        actual_figure = make_figure(df, which=features, normalised=use_normalised)

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
                        html.Hr(),
                        html.Details(
                            [
                                html.Summary("Click to show/hide opto plots"),
                                html.Br(),
                                html.Div(
                                    [
                                        html.Img(
                                            src=opto_plots_url, className="responsive"
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ]
                )
            ],
            update_on_click(
                actual_figure, df, which=features, normalised=True, subselect=unit
            ),
            store,
        )