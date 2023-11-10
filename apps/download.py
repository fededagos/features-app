import urllib

from dash import Input, Output, dcc, html

from app import app

layout = html.Div(
    [
        html.H2(html.Strong("Datasets Download"), style={"text-align": "center"}),
        html.Div(
            className="information-container",
            children=[
                # html.H2("General information about the datasets"),
                dcc.Markdown(
                    """All datasets are in the common `.h5` format. 
                    If you are not familiar with `.h5` check out the [`h5py`](https://docs.h5py.org/en/stable/quick.html) quickstart guide and our
                    helper functions in [`npyx`](https://github.com/m-beau/NeuroPyxels/blob/master/npyx/h5.py) for easier handling of the files. """
                ),
            ],
        ),
        html.Div(
            className="dataset-container",
            children=[
                html.H2("Hausser dataset"),
                html.P(
                    "Contains both labelled (optotagged and crosscorrelogram identified) and unlabelled neurons recorded by the Hausser lab at UCL. Neurons are recorded in the mouse using Neuropixels 1.0 and 2.0 probes."
                ),
                html.A(
                    "Download Hausser Dataset",
                    id="btn-1",
                    href="https://figshare.com/ndownloader/files/43102990?private_link=9a9dfce1c64cb807fc96",
                    className="download-button",
                    target="_blank",
                ),
            ],
        ),
        html.Div(
            className="dataset-container",
            children=[
                html.H2("Hull labelled dataset"),
                html.P(
                    "Contains labelled (optotagged and crosscorrelogram identified) neurons recorded by the Hull lab at Duke. Neurons are recorded in the mouse using Neuropixels 1.0 probes."
                ),
                html.A(
                    "Download Hull labelled dataset",
                    id="btn-2",
                    href="https://figshare.com/ndownloader/files/43102996?private_link=9a9dfce1c64cb807fc96",
                    className="download-button",
                    target="_blank",
                ),
            ],
        ),
        html.Div(
            className="dataset-container",
            children=[
                html.H2("Lisberger dataset"),
                html.P(
                    "Contains both labelled (expert-identified) and unlabelled neurons recorded by the Lisberger lab at Duke. Neurons are recorded in the monkey using a variety of electrodes."
                ),
                html.A(
                    "Download Lisberger dataset",
                    id="btn-3",
                    href="https://figshare.com/ndownloader/files/41721090?private_link=9a9dfce1c64cb807fc96",
                    className="download-button",
                    target="_blank",
                ),
            ],
        ),
        html.Div(
            className="dataset-container",
            children=[
                html.H2("Hull unlabelled dataset"),
                html.P(
                    "Contains unlabelled neurons recorded by the Hull lab at Duke. Neurons are recorded in the mouse using Neuropixels 1.0 probes."
                ),
                html.A(
                    "Download Hull unlabelled dataset",
                    id="btn-4",
                    href="https://figshare.com/ndownloader/files/41720901?private_link=9a9dfce1c64cb807fc96",
                    className="download-button",
                    target="_blank",
                ),
            ],
        ),
        html.Div(
            className="dataset-container",
            children=[
                html.H2("Medina unlabelled dataset"),
                html.P(
                    "Contains unlabelled neurons recorded by the Medina lab at Baylor College of Medicine. Neurons are recorded in the mouse using Neuropixels 1.0 probes."
                ),
                html.A(
                    "Download Medina unlabelled dataset",
                    id="btn-5",
                    href="https://figshare.com/ndownloader/files/41721195?private_link=9a9dfce1c64cb807fc96",
                    className="download-button",
                    target="_blank",
                ),
            ],
        ),
    ],
    className="page-container",
)
