from dash import Input, Output, clientside_callback, dcc, html

from app import app

layout = html.Div(
    children=[
        # Title
        html.H2(
            "C4 database spiking and waveform features explorer", 
            className="notoc",
            style={
                "margin-bottom": "0.5em", 
                "textAlign": "center"
            }
        ),
        # Buttons div first
        html.Div(
            [
                html.A("Explore temporal features", href="/apps/temporal_features", className="button", style={"marginRight": "10px"}),
                html.A("Explore waveform features", href="/apps/waveform_features", className="button", style={"marginRight": "10px"}),
                html.A("Explore all features", href="/apps/explore_features", className="button"),
            ],
            style={
                "display": "flex", 
                "flexWrap": "wrap", 
                "justifyContent": "center", 
                "gap": "10px",
                "marginBottom": "20px"  # Add some space between buttons and content
            }
        ),
        # Then the iframe
        html.Iframe(
            id="exploration-docs",
            src="../assets/docs/exploration_home.html",
            style={"width": "100%", "border": "none"},
        ),
        # Hidden div to store navbar height
        html.Div(id="navbar-height-store-exploration", style={"display": "none"}),
        # Interval for initial load (hack to avoid initial height miscalculation, can mess up whole layout)
        dcc.Interval(id="initial-loader", interval=100, max_intervals=1),
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
    Output("navbar-height-store-exploration", "children"),
    Input("initial-loader", "n_intervals"),
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
    Output("exploration-docs", "style"),
    Input("navbar-height-store-exploration", "children"),
)
