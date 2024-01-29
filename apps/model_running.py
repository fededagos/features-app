from dash import dcc, html

from app import app

test_snippet = """
```python
import npyx 
import numpy as np

# Load the data
np.random.seed(1)
"""

layout = html.Div(
    [
        html.Div(html.H1("About", style={"font-weight": "bold", "textAlign": "center"}), className="row"),
        html.Div(
            [
                html.Div(
                    id="toc-column",
                    children=[
                        html.H6("Table of Contents", style={"font-weight": "bold"}),
                        html.Ul(
                            [
                                html.Li(
                                    [
                                        html.A("Running the model from the command line", href="#command-line"),
                                        html.Ul(
                                            html.Li(html.A("Installing npyx", href="#installing-npyx")),
                                        ),
                                    ]
                                ),
                                html.Li(html.A("Running the model directly from phy", href="#phy")),
                            ],
                            style={"paddingLeft": "20px"},
                        ),
                    ],
                    className="three columns",
                    style={
                        "maxWidth": "200px",
                    },
                ),
                html.Div(
                    id="main-column",
                    children=[
                        html.H2("Running from the command line", id="command-line", style={"font-weight": "bold"}),
                        html.P(
                            """
                            Here we describe how to run the model on your own spike sorted data from the command line.
                            ... it should start from “create an anaconda environment”, and finish with the command-line options in detail
                            """
                        ),
                        dcc.Markdown(
                            test_snippet,
                            style={
                                "whiteSpace": "pre",
                                "backgroundColor": "#e9e9e9",
                                "padding": "10px",
                                "border": "10px",
                            },
                        ),
                        html.H3("Installing npyx", id="installing-npyx"),
                        html.H2("Running the model directly from phy", id="phy", style={"font-weight": "bold"}),
                        html.P(
                            """
                            Coming soon...
                            """
                        ),
                    ],
                    className="nine columns",
                    style={"textAlign": "left", "marginLeft": "auto", "marginRight": "auto"},
                ),
            ],
            className="row",
            style={"display": "flex", "flexWrap": "wrap", "alignItems": "flex-start"},
        ),
    ],
    className="about-container",
    style={"maxWidth": "1200px", "margin": "0 auto"},
)
