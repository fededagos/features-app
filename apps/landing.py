from dash import dcc, get_asset_url, html

from app import app

layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=get_asset_url("unis/UCL_LOGO.svg"),
                            style={
                                "maxWidth": "calc(25% - 20px)",  # 25% for 4 logos in a row, minus the gap
                                "maxHeight": "100px",
                                "minWidth": "100px",
                                "flex": "1 1 auto",
                                "objectFit": "contain",
                            },
                        ),
                        html.Img(
                            src=get_asset_url("unis/Baylor.svg"),
                            style={
                                "maxWidth": "calc(25% - 20px)",  # 25% for 4 logos in a row, minus the gap
                                "maxHeight": "100px",
                                "minWidth": "100px",
                                "flex": "1 1 auto",
                                "objectFit": "contain",
                            },
                        ),
                        html.Img(
                            src=get_asset_url("unis/Duke.svg"),
                            style={
                                "maxWidth": "calc(25% - 20px)",  # 25% for 4 logos in a row, minus the gap
                                "maxHeight": "100px",
                                "minWidth": "100px",
                                "flex": "1 1 auto",
                                "objectFit": "contain",
                            },
                        ),
                        html.Img(
                            src=get_asset_url("unis/bar-ilan.svg"),
                            style={
                                "maxWidth": "calc(25% - 20px)",  # 25% for 4 logos in a row, minus the gap
                                "maxHeight": "100px",
                                "minWidth": "100px",
                                "flex": "1 1 auto",
                                "objectFit": "contain",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flexDirection": "row",
                        "flexWrap": "wrap",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "gap": "20px",
                        "marginBottom": "50px",
                    },
                ),
                html.H1(
                    "Welcome to the C4 Database", style={"margin-bottom": "0.5em", "font-weight": "bold"}
                ),  # Adjust the bottom margin as needed
                html.Div([
                    html.P([
                        "This website complements the publication in Cell (",
                        html.A("Beau et al., 2025", href="https://doi.org/10.1016/j.cell.2025.01.041"),
                        ") describing a classifier for identifying cell types in extracellular recordings from cerebellar cortex. Here you can:"], 
                        style={
                            "textAlign": "left",
                            "marginBottom": "1em"
                        }
                    ),
                    html.Ul(
                        [
                            html.Li([
                                "Find the ",
                                html.A([html.Strong("documentation to run the C4 classifier")], href="/apps/classifier"),
                                " on your cerebellar cortex recordings. The classifier should work out of the box for Neuropixels recordings, provided that you filtered your data appropriately. The classifier relies on ",
                                html.A("NeuroPyxels", href="https://github.com/m-beau/NeuroPyxels"),
                                ", which is licensed under the ",
                                html.A("GNU General Public License v3.0", href="https://www.gnu.org/licenses/#GPL"),
                                "."
                            ]),
                            html.Li([
                                "Visualize and download the ",
                                html.A([html.Strong("C4 ground-truth database")], href="/apps/download"),
                                " of opto-tagged Purkinje cells, molecular layer interneurons, Golgi cells, and mossy fibres, recorded in awake mice."
                            ]),
                            html.Li([
                                html.A([html.Strong("Explore classical spiking and waveform statistics")], href="/apps/exploration_home"),
                                " from the neurons of the C4 database (some key statistics are summarized in the Supplementary Table 1 of Beau et al., 2025). The C4 classifier predicts cell type identity from neurons' raw waveforms and autocorrelograms, not from 'classical features'. However, since these features are commonly reported in papers we present them here because they are useful for putting the C4 database into the context of the literature."
                            ])
                        ],
                        style={
                            "paddingLeft": "20px"  # Reduced padding for bullets to match heading
                        }
                    ),
                html.H4("Using and Citing the C4 Database"),
                html.P([
                    "The data and visualizations on this website are intended to be freely available for use by the scientific community. The C4 dataset is licensed under the ",
                    html.A("Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License", href="https://creativecommons.org/licenses/by-nc-sa/4.0/"),
                    ", while our classifier is licensed under the ",
                    html.A("GNU General Public License v3.0", href="https://www.gnu.org/licenses/#GPL"),
                    " as part of ",
                    html.A("NeuroPyxels", href="https://github.com/m-beau/NeuroPyxels"),
                    ". ",
                    html.Strong("If you download and use our data for a publication, and/or if you would like to refer to the database, please cite "),
                    html.A("Beau et al., 2025, Cell", href="https://doi.org/10.1016/j.cell.2025.01.041"),
                    html.Strong(" together with the "),
                    html.A("NeuroPyxels repository", href="https://github.com/m-beau/NeuroPyxels"),
                    html.Strong(" ("),
                    html.A("Beau et al., 2021, Zenodo", href="https://zenodo.org/records/5509776"),
                    html.Strong(")"),
                    html.Strong(", and include the link to this database (https://www.c4-database.com) in your methods section."),
                    " Thank you!"
                ],
        style={
            "textAlign": "left",
            "marginBottom": "1em"
        }
    )
                ],
                style={
                    "width": "100%",
                    "maxWidth": "800px",
                    "margin": "0 auto",
                    "textAlign": "left",
                }),
                html.P('', style={"margin-bottom": "2em"}),  # Adjust the bottom margin as needed
                html.Div(
                    [
                        html.A("About", href="/apps/about", className="button", style={"marginRight": "10px"}),
                        html.A("Classifier documentation", href="/apps/classifier", className="button", style={"marginRight": "10px"}),
                        html.A("Download dataset", href="/apps/download", className="button", style={"marginRight": "10px"}),
                        html.A("Explore dataset", href="/apps/exploration_home", className="button"),
                    ],
                    style={"display": "flex", "flexWrap": "wrap", "justifyContent": "center", "gap": "10px"},
                ),
            ],
            className="wrapper",
            style={
                "marginTop": "10px",  # This makes sure that the wrapper is not too close to the top
                "justifyContent": "center",
                "alignItems": "center",
                "minHeight": "100vh",  # This makes sure that the wrapper takes the full viewport height
            },
        )
    ]
)
