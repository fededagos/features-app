from dash import html


def make_footer(amplitude_img_url, opto_plots_url):
    return [
        html.H6("Amplitude distribution (spontaneous period):"),
        html.Img(
            src=amplitude_img_url,
            style={
                "max-width": "60vw",
                "display": "block",
                # "margin-left": "auto",
                # "margin-right": "auto",
            },
            className="responsive",
        ),
        html.Hr(),
        # html.Details(
        #     [
        #         html.Summary(
        #             "Click to show/hide opto plots", style={"font-size": "larger"}
        #         ),
        #         html.Br(),
        #         html.Div(
        #             [
        #                 html.Img(
        #                     src=opto_plots_url,
        #                     className="responsive",
        #                 ),
        #             ]
        #         ),
        #     ]
        # ),
        # html.Hr(),
    ]
