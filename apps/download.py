import urllib

from dash import Input, Output, dcc, get_asset_url, html

from app import app

layout = html.Div(
    [
        html.Div(
            className="information-container",
            children=[
                html.H2("Download datasets", style={"margin-bottom": "0.5em", "textAlign": "center"}),
                html.Img(
                    src=get_asset_url("figure_4_summary_plots.svg"),
                    className="responsivesvg",
                    style={"max-width": "100%"},
                ),
                dcc.Markdown(
                    """
                    Excerpt from Figure 4 of [Beau et al. (2025)](https://doi.org/10.1016/j.cell.2025.01.041), showing 
                    summary peak-channel waveform and autocorrelograms for the ground-truth optotagged neurons in the 
                    database. The ground-truth units can be found in the *Häusser lab* and *Hull lab* ground truth 
                    datasets for download below.
                    
                    ---
                    All C4 datasets are in binary `.h5` format. 
                    If you are not familiar with `.h5`, have a look at the [`h5py`](https://docs.h5py.org/en/stable/quick.html) quickstart guide and our
                    helper functions in [`NeuroPyxels`](https://github.com/m-beau/NeuroPyxels/blob/master/npyx/h5.py).
                    """
                ),
            ],
        ),
        html.Div(
            className="dataset-container",
            children=[
                html.H2("Häusser lab ground truth dataset"),
                html.P(
                    "Contains both labelled (optotagged and crosscorrelogram identified) and unlabelled neurons recorded by the Häusser lab at UCL. Neurons are recorded in the mouse using Neuropixels 1.0 and 2.0 probes."
                ),
                html.A(
                    "Download Häusser lab Dataset",
                    id="btn-1",
                    href="https://rdr.ucl.ac.uk/ndownloader/files/43102990",
                    className="download-button",
                    target="_blank",
                ),
            ],
        ),
        html.Div(
            className="dataset-container",
            children=[
                html.H2("Hull lab ground truth dataset"),
                html.P(
                    "Contains labelled (optotagged and crosscorrelogram identified) neurons recorded by the Hull lab at Duke. Neurons are recorded in the mouse using Neuropixels 1.0 probes."
                ),
                html.A(
                    "Download Hull lab labelled dataset",
                    id="btn-2",
                    href="https://rdr.ucl.ac.uk/ndownloader/files/43102996",
                    className="download-button",
                    target="_blank",
                ),
            ],
        ),
        html.Div(
            className="dataset-container",
            children=[
                html.H2("Lisberger lab dataset"),
                html.P(
                    "Contains both human expert-labelled and unlabelled neurons recorded by the Lisberger lab at Duke. Neurons are recorded in the monkey using several different electrode types."
                ),
                html.A(
                    "Download Lisberger lab dataset",
                    id="btn-3",
                    href="https://rdr.ucl.ac.uk/ndownloader/files/41721090",
                    className="download-button",
                    target="_blank",
                ),
            ],
        ),
        html.Div(
            className="dataset-container",
            children=[
                html.H2("Hull lab unlabelled dataset"),
                html.P(
                    "Contains unlabelled neurons recorded by the Hull lab at Duke. Neurons are recorded in the mouse using Neuropixels 1.0 probes."
                ),
                html.A(
                    "Download Hull lab unlabelled dataset",
                    id="btn-4",
                    href="https://rdr.ucl.ac.uk/ndownloader/files/41720901",
                    className="download-button",
                    target="_blank",
                ),
            ],
        ),
        html.Div(
            className="dataset-container",
            children=[
                html.H2("Medina lab unlabelled dataset"),
                html.P(
                    "Contains unlabelled neurons recorded by the Medina lab at Baylor College of Medicine. Neurons are recorded in the mouse using Neuropixels 1.0 probes."
                ),
                html.A(
                    "Download Medina lab unlabelled dataset",
                    id="btn-5",
                    href="https://rdr.ucl.ac.uk/ndownloader/files/42117129",
                    className="download-button",
                    target="_blank",
                ),
            ],
        ),
        html.P(""),
    ],
    className="page-container",
)
