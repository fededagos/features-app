from dash import dcc, html

from app import app

lipsum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam nec est et risus vestibulum facilisis rhoncus vitae dolor. Mauris facilisis risus eu risus feugiat dignissim. In hac habitasse platea dictumst. Vestibulum mattis massa ut nisl malesuada porta. Integer at neque urna. Ut laoreet sit amet orci at tristique. Donec erat est, molestie a diam vel, imperdiet sollicitudin ex. Duis at mollis risus.

Curabitur tincidunt malesuada dui, non tincidunt neque molestie vitae. In aliquet justo eu suscipit egestas. Nulla eleifend laoreet lacus, ornare porttitor nunc. Proin porta scelerisque est sit amet lobortis. In eget eros nisl. Praesent ut neque sit amet enim interdum laoreet eu vel quam. Vestibulum vel massa facilisis, mattis tellus egestas, rutrum arcu. Sed condimentum, lectus ac vulputate convallis, tellus augue blandit metus, eu interdum ipsum nunc at arcu. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Cras non tincidunt ligula, at pretium urna.

Pellentesque quis gravida est, et tincidunt neque. Nam pretium faucibus sem semper hendrerit. Ut luctus sapien quis justo ultricies porttitor. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Aenean finibus dictum tellus sed accumsan. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam venenatis urna vel diam rhoncus sollicitudin.

Phasellus dictum orci sed tincidunt ultricies. Donec iaculis lorem et nibh auctor, ac fermentum ex feugiat. Praesent gravida et nisl sit amet facilisis. Quisque in pulvinar lectus, vel sagittis dolor. Aenean gravida lorem eu purus ornare, a scelerisque nibh tempor. Integer justo lectus, aliquam nec nisi non, faucibus convallis risus. Nullam pretium orci dolor. Duis quis ex ante. Maecenas luctus auctor arcu a sollicitudin. Aliquam erat volutpat. In tincidunt mauris non ante egestas hendrerit. Phasellus rutrum turpis ac mauris facilisis euismod. Fusce scelerisque hendrerit finibus. Nam eu ipsum ex. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.

Fusce vitae lectus mi. Quisque ac feugiat dolor. Nunc vehicula elementum metus, sit amet varius ipsum mollis id. Vestibulum sagittis fringilla fermentum. Etiam dignissim vehicula nisl, in vulputate purus mattis in. In aliquet at nunc id fermentum. Etiam sit amet urna vitae purus pharetra consectetur. Cras lectus odio, blandit nec maximus a, gravida ut massa. Suspendisse vitae bibendum nulla. Curabitur fringilla venenatis massa eget tincidunt. Integer a turpis ultrices, varius nisl eget, efficitur quam. Vivamus arcu enim, malesuada at posuere non, interdum et eros. Quisque velit risus, consequat vel eros sed, vulputate tempus est. Donec quis faucibus mauris.

"""

layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src="https://www.hackerspace-ffm.de/wiki/images/Test-sign_640.png",
                            style={
                                "maxWidth": "100%",
                                "maxHeight": "100px",
                                "flex": "1 1 auto",
                                "objectFit": "contain",
                            },
                        ),
                        html.Img(
                            src="https://www.hackerspace-ffm.de/wiki/images/Test-sign_640.png",
                            style={
                                "maxWidth": "100%",
                                "maxHeight": "100px",
                                "flex": "1 1 auto",
                                "objectFit": "contain",
                            },
                        ),
                        html.Img(
                            src="https://www.hackerspace-ffm.de/wiki/images/Test-sign_640.png",
                            style={
                                "maxWidth": "100%",
                                "maxHeight": "100px",
                                "flex": "1 1 auto",
                                "objectFit": "contain",
                            },
                        ),
                        html.Img(
                            src="https://www.hackerspace-ffm.de/wiki/images/Test-sign_640.png",
                            style={
                                "maxWidth": "100%",
                                "maxHeight": "100px",
                                "flex": "1 1 auto",
                                "objectFit": "contain",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flexWrap": "wrap",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "gap": "20px",
                        "marginBottom": "50px",  # Adjust the gap and margin as needed
                    },
                ),
                html.H1(
                    "Welcome to the C4 Database", style={"margin-bottom": "0.5em", "font-weight": "bold"}
                ),  # Adjust the bottom margin as needed
                html.P(lipsum, style={"margin-bottom": "2em"}),  # Adjust the bottom margin as needed
                html.Div(
                    [
                        html.A("Take me to it!", href="/apps/about", className="button", style={"marginRight": "10px"}),
                        html.A("Another button", href="#", className="button"),
                    ],
                    style={"display": "flex", "flexWrap": "wrap", "justifyContent": "center", "gap": "10px"},
                ),
            ],
            className="wrapper",
            style={
                "display": "flex",
                "flexDirection": "column",
                "justifyContent": "center",
                "alignItems": "center",
                "minHeight": "100vh",  # This makes sure that the wrapper takes the full viewport height
            },
        )
    ]
)
