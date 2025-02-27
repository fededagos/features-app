import numpy as np
import pandas as pd
import plotly.graph_objects as go
from matplotlib import colors as c

from utils.constants import *

MARKERS_DICT = {"hausser": "circle", "hull": "diamond", "lisberger": "x", "combined_mouse": "square"}


def update_on_click(
    fig: go.Figure,
    input_dataframe: pd.DataFrame,
    which="temporal",
    normalised=True,
    subselect=None,
    lab=None,
    features_selection=USE_FEATURES_SELECTION,
):
    # This is to remove previously added highlighted points!
    if lab == "hausser":
        # Why 6*2? Because there are 2 traces per cell type (1 for box, 1 for points; 6 cell types)
        default_traces = 5 * 2
    elif lab == "hull":
        # 5*2 Because the hull lab has 5 cell types only
        default_traces = 5 * 2
    elif lab == "combined_mouse":
        default_traces = 5 * 2
    elif lab == "lisberger":
        # The lisberger lab also has 5 cell types
        default_traces = 5 * 2
    else:
        # All combined
        default_traces = 15 * 2

    if len(fig.data) > default_traces:
        fig.data = fig.data[:default_traces]

    if lab in ["hausser", "hull", "combined_mouse", "lisberger"]:
        input_dataframe = input_dataframe.loc[input_dataframe["lab"] == lab].copy()
    if np.array((which == "temporal")).any():
        input_dataframe = input_dataframe[input_dataframe["feature"].isin(TEMPORAL_FEATURES)]
    elif np.array((which == "waveform")).any():
        input_dataframe = input_dataframe[input_dataframe["feature"].isin(WAVEFORM_FEATURES)]
    elif isinstance(which, list):
        input_dataframe = input_dataframe[input_dataframe["feature"].isin(which)]
    else:
        raise ValueError("which must be either temporal or waveform")

    if features_selection:
        input_dataframe = input_dataframe[input_dataframe["feature"].isin(SELECTED_FEATURES.keys())]

    input_dataframe["feature"] = input_dataframe["feature"].replace(SELECTED_FEATURES)

    # Adding highlighted point if any
    if subselect is not None:
        highlighted_point = input_dataframe[input_dataframe["plotting_id"] == subselect]
        highlighted_label = highlighted_point["label"].to_numpy()[0]
        highlighted_custom_data = list(
            zip(
                highlighted_point["dataset"].to_numpy(),
                highlighted_point["unit"].to_numpy(),
                highlighted_point["raw_value"].to_numpy(),
                highlighted_point["color"].to_numpy(),
                highlighted_point["plotting_id"].to_numpy(),
                highlighted_point["layer"].to_numpy(),
                highlighted_point["feature"].to_numpy(),
            )
        )
        fig.add_trace(
            go.Scatter(
                y=highlighted_point["joint_normalised_value"].to_numpy()
                if normalised
                else highlighted_point["raw_value"].to_numpy(),
                x=highlighted_point["feature"].to_numpy(),
                marker=dict(
                    size=12,
                    line=dict(width=2, color="DarkSlateGrey"),
                    symbol=MARKERS_DICT[highlighted_point["lab"].to_numpy()[0]],
                ),
                marker_color=highlighted_point["color"],
                name=f"{highlighted_label} {subselect}",
                legendgroup=highlighted_label,
                line=dict(dash="dot", color=highlighted_point["color"].to_numpy()[0]),
                # showlegend=False,
                text=[highlighted_label] * len(highlighted_point["normalised_value"].to_numpy()),
                customdata=highlighted_custom_data,
                hovertemplate="<b> %{text} </b><br><br>"
                + "Feature: %{x}<br>"
                + "Raw value: %{highlighted_customdata[2]}<br>"
                + "Cerebellar layer: %{highlighted_customdata[5]}<br>"
                + "Source: %{highlighted_customdata[0]}, unit %{highlighted_customdata[1]}"
                + "<extra></extra>",
            )
        )

    fig.update_traces(hoverinfo="none", hovertemplate=None)

    return fig


def make_joint_figure(
    df: pd.DataFrame,
    which="temporal",
    normalised=True,
    lab="hausser",
    features_selection=USE_FEATURES_SELECTION,
):
    if lab == "hausser":
        df = df.loc[df["lab"] == "hausser"].copy()
    elif lab == "hull":
        df = df.loc[df["lab"] == "hull"].copy()
    elif lab == "combined_mouse":
        # df = df.loc[df["lab"].isin(["hausser", "hull"])].copy()
        df = df.loc[df["lab"] == "combined_mouse"].copy()
    elif lab == "lisberger":
        df = df.loc[df["lab"] == "lisberger"].copy()
    elif lab == "all":
        df = df.loc[df["lab"].isin(["hausser", "hull", "lisberger"])].copy()

    if np.array((which == "temporal")).any():
        df = df[df["feature"].isin(TEMPORAL_FEATURES)]
        update_title = True
    elif np.array((which == "waveform")).any():
        df = df[df["feature"].isin(WAVEFORM_FEATURES)]
        update_title = True
    elif isinstance(which, list):
        df = df[df["feature"].isin(which)]
        update_title = False
    else:
        raise ValueError("which must be either temporal or waveform")

    if features_selection:
        df = df[df["feature"].isin(SELECTED_FEATURES.keys())]

    df["feature"] = df["feature"].replace(SELECTED_FEATURES)

    fig = go.Figure()

    for i, label in enumerate(["PkC_cs", "PkC_ss", "GoC", "MLI", "MFB"]):
        for lab in np.unique(df["lab"].to_numpy()):
            plotting_df = df.loc[(df["lab"] == lab) & (df["label"] == label)]
            if len(plotting_df) == 0:
                continue

            good_neurons = plotting_df[plotting_df["color"] != "gray"]
            neuron_color = good_neurons[good_neurons["label"] == label]["color"].to_numpy()[0]

            custom_data_good = list(
                zip(
                    good_neurons[good_neurons["label"] == label]["dataset"].to_numpy(),
                    good_neurons[good_neurons["label"] == label]["unit"].to_numpy(),
                    good_neurons[good_neurons["label"] == label]["raw_value"].to_numpy(),
                    good_neurons[good_neurons["label"] == label]["color"].to_numpy(),
                    good_neurons[good_neurons["label"] == label]["plotting_id"].to_numpy(),
                    good_neurons[good_neurons["label"] == label]["layer"].to_numpy(),
                    good_neurons[good_neurons["label"] == label]["feature"].to_numpy(),
                )
            )

            fig.add_trace(
                go.Box(
                    y=good_neurons[good_neurons["label"] == label]["joint_normalised_value"].to_numpy()
                    if normalised
                    else good_neurons[good_neurons["label"] == label]["raw_value"].to_numpy(),
                    x=good_neurons[good_neurons["label"] == label]["feature"].to_numpy(),
                    name=f"{lab.capitalize()} {label} (n = {plotting_df['label'].value_counts()[label] // len(np.unique(plotting_df['feature'].to_numpy()))})",
                    marker_color=neuron_color,
                    offsetgroup=str(label) + str(lab),
                    legendgroup=label,
                    marker={"opacity": 0},
                    showlegend=False,
                    text=[label]
                    * len(good_neurons[good_neurons["label"] == label]["joint_normalised_value"].to_numpy()),
                    customdata=custom_data_good,
                    hovertemplate="<b> %{text} </b><br><br>"
                    + "Feature: %{x}<br>"
                    + "Raw value: %{customdata[2]}<br>"
                    + "Cerebellar layer: %{customdata[5]}<br>"
                    + "Source: %{customdata[0]}, unit %{customdata[1]}"
                    + "<extra></extra>",
                )
            )

            fig.add_trace(
                go.Box(
                    y=good_neurons[good_neurons["label"] == label]["joint_normalised_value"].to_numpy()
                    if normalised
                    else good_neurons[good_neurons["label"] == label]["raw_value"].to_numpy(),
                    x=good_neurons[good_neurons["label"] == label]["feature"].to_numpy(),
                    name=f"{lab.capitalize()} {label} (n = {plotting_df['label'].value_counts()[label] // len(np.unique(plotting_df['feature'].to_numpy()))})",
                    marker_color=neuron_color,
                    boxpoints="all",
                    jitter=0.6,
                    pointpos=0,
                    offsetgroup=str(label) + str(lab),
                    legendgroup=label,
                    # legendgrouptitle=dict(text=label),
                    line=dict(color="rgba(0,0,0,0)"),
                    fillcolor="rgba(0,0,0,0)",
                    showlegend=True,
                    marker={"symbol": MARKERS_DICT[lab]},
                    text=[label]
                    * len(good_neurons[good_neurons["label"] == label]["joint_normalised_value"].to_numpy()),
                    customdata=custom_data_good,
                    hovertemplate="<b> %{text} </b><br><br>"
                    + "Feature: %{x}<br>"
                    + "Raw value: %{customdata[2]}<br>"
                    + "Cerebellar layer: %{customdata[5]}<br>"
                    + "Source: %{customdata[0]}, unit %{customdata[1]}"
                    + "<extra></extra>",
                )
            )

        fig.update_layout(
            title=go.layout.Title(
                text=f"<b>{which.title()} features distributions by cell types </b><br><sup>Click on legend to show/hide elements. Hover on points for details.</sup>",
                xref="paper",
                x=0,
            )
            if update_title
            else None,
            yaxis_title="Feature Value (z-score)" if normalised else "Feature Value",
            xaxis_title="Feature",
            legend_title="Cell type",
            boxmode="group",  # group together boxes of the different traces for each value of x
            # xaxis=dict(
            #     ticktext=[SELECTED_FEATURES],
            # ),
        )
        fig.update_traces(
            marker=dict(size=1, line=dict(width=2, color="DarkSlateGrey")),
            selector=dict(mode="markers"),
        )

        fig.update_traces(hoverinfo="none", hovertemplate=None)
        fig.update_layout(legend={"itemsizing": "constant", "itemwidth": 30})

    return fig
