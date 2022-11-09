import dash_auth
from users import USERNAME_PASSWORD_PAIRS

from dash import Dash, dcc, html, Input, Output, no_update
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import waveform_features, temporal_features, explore_features, about

app.title = "Feature plots"

auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
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
                dcc.Link(
                    "Features Explorer", href="/apps/explore_features", className="tab"
                ),
                dcc.Link("About", href="/apps/about", className="tab"),
            ],
            className="wrapper",
        ),
        html.Br(),
        html.Div(id="page-content", children=[]),
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/apps/temporal_features":
        return temporal_features.layout
    elif pathname == "/apps/waveform_features":
        return waveform_features.layout
    elif pathname == "/apps/explore_features":
        return explore_features.layout
    elif pathname == "/apps/about":
        return about.layout
    else:
        return temporal_features.layout


if __name__ == "__main__":
    app.run_server(debug=True)
