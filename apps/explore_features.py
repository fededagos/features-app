from dash import Dash, dcc, html, Input, Output, State, no_update
import pandas as pd
import pathlib
import json
import dash_loading_spinners as dls
from app import app
from utils.plotting import make_joint_figure_side_by_side, update_on_click
import plotly.graph_objects as go
from apps.footer import make_footer
from utils.constants import PLOTS_FOLDER_URL, TEMPORAL_FEATURES

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("hull_hausser_all_features.csv"))

with open(DATA_PATH.joinpath("iframe_src.txt")) as f:
    data = f.read()

iframe_src = json.loads(data)

layout = html.Div(
    [
        dcc.Store(
            id="store",
            data={"input_changed": [0], "norm_changed": [1], "lab": ["hausser"]},
        ),
        html.Div(
            [
                dcc.Dropdown(
                    ["Hausser data", "Hull data", "Combined data"],
                    "Hausser data",
                    searchable=False,
                    clearable=False,
                    id="dataset-choice-feature",
                    style={
                        "flex-grow": 4,
                        "min-width": "200px",
                        "margin-right": "5px",
                    },
                ),
                html.Button(
                    "Reset graph",
                    id="reset-feature-graph",
                    n_clicks=0,
                    style={"flex-grow": 1, "margin-left": "5px",},
                ),
            ],
            className="datasetselect",
        ),
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
                dls.Hash(
                    [
                        dcc.Graph(
                            id="feature-graph",
                            figure=go.Figure(),
                            clear_on_unhover=True,
                            style={"height": "75vh"},
                            className="card",
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

    # If hovering on a temporal feature show the ACG, otherwise show the waveform
    if which_feature in set(TEMPORAL_FEATURES):
        image_url = PLOTS_FOLDER_URL + str(plotting_id) + "-acg.svg"
    else:
        image_url = PLOTS_FOLDER_URL + str(plotting_id) + "-wvf.svg"

    x_dist = properties_dict["bbox"]["x0"]

    if x_dist > 500:
        direction = "left"
    else:
        direction = "right"

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
                html.P(
                    "Click on a point in the graph to fix it here for further inspection."
                ),
            ],
            go.Figure(),
            store,
            None,
            0,
            "Hausser data",
            None,
        )

    # Check if user requested for a lab data input change
    lab_correspondence = {
        "Hausser data": "hausser",
        "Hull data": "hull",
        "Combined data": "combined",
    }
    lab_id = lab_correspondence[lab]
    store["lab"].append(lab_id)
    lab_changed = store["lab"][-1] != store["lab"][-2]

    if value is not None and len(value) != 0:
        store["input_changed"].append(len(value))
        store["norm_changed"].append(int(normalised == "Normalised"))
    elif value is None or len(value) == 0:
        store["input_changed"] = [0]

        return (
            [
                html.Hr(),
                html.H3("Inspect element:"),
                html.P(
                    "Click on a point in the graph to fix it here for further inspection."
                ),
            ],
            go.Figure(),
            store,
            None,
            no_update,
            no_update,
            no_update,
        )

    input_changed = (
        store["input_changed"][-1] != store["input_changed"][-2]
        if len(store["input_changed"]) > 2
        else False
    )
    norm_changed = (
        store["norm_changed"][-1] != store["norm_changed"][-2]
        if len(store["norm_changed"]) > 2
        else False
    )

    if click_input is None or lab_changed:
        use_normalised = True if normalised == "Normalised" else False
        features = list(value)
        actual_figure = make_joint_figure_side_by_side(
            df, which=features, normalised=use_normalised, lab=lab_id
        )
        return no_update, actual_figure, store, None, no_update, no_update, no_update

    elif click_input is not None and not input_changed and not norm_changed:
        dp = click_input["points"][0]["customdata"][0].split("/")
        dp = dp[-1]
        unit = click_input["points"][0]["customdata"][1]
        plotting_id = click_input["points"][0]["customdata"][4]

        acg_image_url = PLOTS_FOLDER_URL + str(plotting_id) + "-acg.svg"
        wvf_image_url = PLOTS_FOLDER_URL + str(plotting_id) + "-wvf.svg"
        amplitude_img_url = PLOTS_FOLDER_URL + str(plotting_id) + "-amplitudes.png"
        cell_type = click_input['points'][0]['text']

        # All hull data has a plotting id greater than 1000
        if int(plotting_id) < 1000:
            opto_plots_url = (
                PLOTS_FOLDER_URL + str(plotting_id) + "_opto_plots_combined.png"
            )
            
        elif (cell_type=="PkC_ss" or cell_type=="PkC_cs") and  "YC001" not in dp:
            opto_plots_url = PLOTS_FOLDER_URL + "purkinje_cell.png"
            
        else:
            opto_plots_url = PLOTS_FOLDER_URL + "opto_plots_unavailable.png"

        try:
            drug_sheet_url = iframe_src[click_input["points"][0]["customdata"][0]]
        except KeyError:
            drug_sheet_url = iframe_src["missing"]

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
                        *make_footer(amplitude_img_url, opto_plots_url, drug_sheet_url),
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
    elif click_input is not None and (input_changed or norm_changed or lab_changed):
        dp = click_input["points"][0]["customdata"][0].split("/")
        dp = dp[-1]
        unit = click_input["points"][0]["customdata"][1]
        plotting_id = click_input["points"][0]["customdata"][4]

        acg_image_url = PLOTS_FOLDER_URL + str(plotting_id) + "-acg.svg"
        wvf_image_url = PLOTS_FOLDER_URL + str(plotting_id) + "-wvf.svg"

        opto_plots_url = (
            PLOTS_FOLDER_URL + str(plotting_id) + "_opto_plots_combined.png"
        )
        amplitude_img_url = PLOTS_FOLDER_URL + str(plotting_id) + "-amplitudes.png"

        try:
            drug_sheet_url = iframe_src[click_input["points"][0]["customdata"][0]]
        except KeyError:
            drug_sheet_url = iframe_src["missing"]

        use_normalised = True if normalised == "Normalised" else False
        features = list(value)
        actual_figure = make_joint_figure_side_by_side(
            df, which=features, normalised=use_normalised, lab=lab_id
        )

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
                        *make_footer(amplitude_img_url, opto_plots_url, drug_sheet_url),
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
