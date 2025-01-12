from dash import Input, Output, clientside_callback, dcc, html

from app import app

layout = html.Div(
    children=[
        html.Iframe(
            id="about-docs",
            src="../assets/docs/about.html",
            style={"width": "100%", "border": "none"},
        ),
        # Hidden div to store navbar height
        html.Div(id="navbar-height-store-about", style={"display": "none"}),
        # Interval for initial load (hack to avoid initial height miscalculation, can mess up whole layout)
        dcc.Interval(id="initial-loader-about", interval=100, max_intervals=1),
    ],
    style={"overflow": "hidden"},
)

clientside_callback(
    """
    function(n_intervals) {
        const navbar = document.getElementById('main-navbar');
        return navbar ? navbar.offsetHeight : 0;
    }
    """,
    Output("navbar-height-store-about", "children"),
    Input("initial-loader-about", "n_intervals"),
)

clientside_callback(
    """
    function(navbar_height) {
        if (navbar_height === null) return {};
        
        return {
            height: `calc(97vh - ${navbar_height}px)`,
            width: "100%",
            border: "none"
        };
    }
    """,
    Output("about-docs", "style"),
    Input("navbar-height-store-about", "children"),
)
