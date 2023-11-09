from dash import dcc, html

from app import app

layout = html.Div(
    [
        html.H1("About", style={"font-weight": "bold"}),
        html.Div(
            children=[
                html.H6("Table of Contents", style={"font-weight": "bold"}),
                html.Ul(
                    [
                        html.Li(html.A("Introduction", href="#introduction")),
                        html.Li(html.A("Features", href="#features")),
                        html.Li(html.A("Features glossary", href="#features-glossary")),
                        html.Li(html.A("Plot details", href="#plot-details")),
                        html.Li(html.A("Contact", href="#contact")),
                    ],
                ),
            ],
            className="toc-container",
        ),
        html.H2("Introduction", id="introduction"),
        html.P(
            "This web application is intended to be used to visually explore the C4 database using features extracted from the data. \
            Even though the features are not directly used as computed for cell-types classification, they can be used to quickly navigate and get insights about the database."
        ),
        html.P(
            [
                "The features are computed directly from the published .h5 databases ",
                html.A("(which can be downloaded here)", href="/apps/download"),
                " using npyx.",
            ]
        ),
        html.H2("Features", id="features"),
        html.P("Here, we list some of the key features of our application."),
        html.H2("Features glossary", id="features-glossary"),
        html.P("What the names of the features mean."),
        html.H2("Plot details", id="plot-details"),
        html.P(
            "All plots are generated using Plotly for python. Each box spans from quartile 1 (Q1) to quartile 3 (Q3). \
            The second quartile (Q2, i.e. the median) is marked by a line inside the box. The fences growing outward from the boxes' \
                edges span +/- 1.5 times the interquartile range (IQR: Q3-Q1)."
        ),
        html.H2("Contact", id="contact"),
        html.P(
            [
                "For any questions or feedback, please ",
                html.A("contact us", href="mailto:fede.dagos@gmail.com"),
                ".",
            ]
        ),
    ],
    className="about-container",
)
