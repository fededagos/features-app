import numpy as np
import pandas as pd
import plotly.graph_objects as go
from matplotlib import colors as c

from utils.constants import *


def make_figure(
    new_df: pd.DataFrame, which="temporal", normalised=True, subselect=None
):
    n_neurons = np.unique(new_df["plotting_id"].to_numpy()).shape[0]
    if np.array((which == "temporal")).any():
        new_df = new_df[new_df["feature"].isin(TEMPORAL_FEATURES)]
        update_title = True
    elif np.array((which == "waveform")).any():
        new_df = new_df[new_df["feature"].isin(WAVEFORM_FEATURES)]
        update_title = True
    elif isinstance(which, list):
        new_df = new_df[new_df["feature"].isin(which)]
        update_title = False
    else:
        raise ValueError("which must be either temporal or waveform")

    fig = go.Figure()
    colors = ["orange", "blue", "green", "brown", "red", "purple"]
    color_dict = dict(zip(["PkC_cs", "PkC_ss", "GoC", "GrC", "MLI", "MFB"], colors))
    good_neurons = new_df[new_df["color"] != "gray"]
    grey_neurons = new_df[new_df["color"] == "gray"]
    for i, label in enumerate(["PkC_cs", "PkC_ss", "GoC", "GrC", "MLI", "MFB"]):
        custom_data_good = list(
            zip(
                good_neurons[good_neurons["label"] == label]["dp"].to_numpy(),
                good_neurons[good_neurons["label"] == label]["unit"].to_numpy(),
                good_neurons[good_neurons["label"] == label]["raw_value"].to_numpy(),
                good_neurons[good_neurons["label"] == label]["color"].to_numpy(),
                good_neurons[good_neurons["label"] == label]["plotting_id"].to_numpy(),
            )
        )

        custom_data_grey = list(
            zip(
                grey_neurons[grey_neurons["label"] == label]["dp"].to_numpy(),
                grey_neurons[grey_neurons["label"] == label]["unit"].to_numpy(),
                grey_neurons[grey_neurons["label"] == label]["raw_value"].to_numpy(),
                grey_neurons[grey_neurons["label"] == label]["color"].to_numpy(),
                grey_neurons[grey_neurons["label"] == label]["plotting_id"].to_numpy(),
            )
        )

        fig.add_trace(
            go.Box(
                y=good_neurons[good_neurons["label"] == label][
                    "normalised_value"
                ].to_numpy()
                if normalised
                else good_neurons[good_neurons["label"] == label][
                    "raw_value"
                ].to_numpy(),
                x=good_neurons[good_neurons["label"] == label]["feature"].to_numpy(),
                name=f'{label} (n = {new_df["label"].value_counts()[label] // len(np.unique(new_df["feature"].to_numpy()))})',
                marker_color=colors[i],
                offsetgroup=label,
                legendgroup=label,
                marker={"opacity": 0},
                text=[label]
                * len(
                    good_neurons[good_neurons["label"] == label][
                        "normalised_value"
                    ].to_numpy()
                ),
                customdata=custom_data_good,
                hovertemplate="<b> %{text} </b><br><br>"
                + "Feature: %{x}<br>"
                + "Raw value: %{customdata[2]}<br>"
                + "Source: %{customdata[0]}, unit %{customdata[1]}"
                + "<extra></extra>",
            )
        )

        fig.add_trace(
            go.Box(
                y=good_neurons[good_neurons["label"] == label][
                    "normalised_value"
                ].to_numpy()
                if normalised
                else good_neurons[good_neurons["label"] == label][
                    "raw_value"
                ].to_numpy(),
                x=good_neurons[good_neurons["label"] == label]["feature"].to_numpy(),
                name=f'{label} (n = {new_df["label"].value_counts()[label] // len(np.unique(new_df["feature"].to_numpy()))})',
                marker_color=colors[i],
                boxpoints="all",
                jitter=0.6,
                pointpos=0,
                offsetgroup=label,
                legendgroup=label,
                # legendgrouptitle=dict(text=label),
                line=dict(color="rgba(0,0,0,0)"),
                fillcolor="rgba(0,0,0,0)",
                showlegend=False,
                text=[label]
                * len(
                    good_neurons[good_neurons["label"] == label][
                        "normalised_value"
                    ].to_numpy()
                ),
                customdata=custom_data_good,
                hovertemplate="<b> %{text} </b><br><br>"
                + "Feature: %{x}<br>"
                + "Raw value: %{customdata[2]}<br>"
                + "Source: %{customdata[0]}, unit %{customdata[1]}"
                + "<extra></extra>",
            )
        )

        fig.add_trace(
            go.Box(
                y=grey_neurons[grey_neurons["label"] == label][
                    "normalised_value"
                ].to_numpy()
                if normalised
                else grey_neurons[grey_neurons["label"] == label][
                    "raw_value"
                ].to_numpy(),
                x=grey_neurons[grey_neurons["label"] == label]["feature"].to_numpy(),
                name=f'{label} (n = {new_df["label"].value_counts()[label] // len(np.unique(new_df["feature"].to_numpy()))})',
                marker_color="gray",
                boxpoints="all",
                jitter=0.6,
                pointpos=0,
                offsetgroup=label,
                legendgroup=label,
                # legendgrouptitle=dict(text=label),
                line=dict(color="rgba(0,0,0,0)"),
                fillcolor="rgba(0,0,0,0)",
                showlegend=False,
                text=[label]
                * len(
                    grey_neurons[grey_neurons["label"] == label][
                        "normalised_value"
                    ].to_numpy()
                ),
                customdata=custom_data_grey,
                hovertemplate="<b> %{text} </b><br><br>"
                + "Feature: %{x}<br>"
                + "Raw value: %{customdata[2]}<br>"
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
    )
    fig.update_traces(
        marker=dict(size=1, line=dict(width=2, color="DarkSlateGrey")),
        selector=dict(mode="markers"),
    )

    fig.update_traces(hoverinfo="none", hovertemplate=None)

    return fig


def update_on_click(
    fig: go.Figure,
    new_df: pd.DataFrame,
    which="temporal",
    normalised=True,
    subselect=None,
    lab="hausser",
):
    # This is to remove previously added highlighted points!
    if lab == "hausser":
        # Why 6*3? Because there are 3 traces per cell type (1 for box, 1 for points, 1 for zero values; 6 cell types)
        default_traces = 6 * 3
    elif lab == "hull":
        # 4*3 Because the hull lab has 3 cell types only
        default_traces = 4 * 3
    else:
        # The labs combined have (6+4)*3 = 30 traces in total
        default_traces = 10 * 3

    if len(fig.data) > default_traces:
        fig.data = fig.data[:default_traces]

    n_neurons = np.unique(new_df["unit"].to_numpy()).shape[0]
    if np.array((which == "temporal")).any():
        new_df = new_df[new_df["feature"].isin(TEMPORAL_FEATURES)]
    elif np.array((which == "waveform")).any():
        new_df = new_df[new_df["feature"].isin(WAVEFORM_FEATURES)]
    elif isinstance(which, list):
        new_df = new_df[new_df["feature"].isin(which)]
    else:
        raise ValueError("which must be either temporal or waveform")

    colors = ["orange", "blue", "green", "brown", "red", "purple"]
    color_dict = dict(zip(["PkC_cs", "PkC_ss", "GoC", "GrC", "MLI", "MFB"], colors))

    # Adding highlighted point if any
    if subselect is not None:
        highlighted_point = new_df[new_df["plotting_id"] == subselect]
        highlighted_label = highlighted_point["label"].to_numpy()[0]
        highlighted_custom_data = list(
            zip(
                highlighted_point["dp"].to_numpy(),
                highlighted_point["unit"].to_numpy(),
                highlighted_point["raw_value"].to_numpy(),
                highlighted_point["color"].to_numpy(),
                highlighted_point["plotting_id"].to_numpy(),
            )
        )
        fig.add_trace(
            go.Scatter(
                y=highlighted_point["joint_normalised_value"].to_numpy()
                if normalised
                else highlighted_point["raw_value"].to_numpy(),
                x=highlighted_point["feature"].to_numpy(),
                marker=dict(size=12, line=dict(width=2, color="DarkSlateGrey")),
                marker_color=highlighted_point["color"],
                name=f"{highlighted_label} {subselect}",
                legendgroup=highlighted_label,
                line=dict(dash="dot", color=highlighted_point["color"].to_numpy()[0]),
                # showlegend=False,
                text=[highlighted_label]
                * len(highlighted_point["normalised_value"].to_numpy()),
                customdata=highlighted_custom_data,
                hovertemplate="<b> %{text} </b><br><br>"
                + "Feature: %{x}<br>"
                + "Raw value: %{highlighted_customdata[2]}<br>"
                + "Source: %{highlighted_customdata[0]}, unit %{highlighted_customdata[1]}"
                + "<extra></extra>",
            )
        )

    fig.update_traces(hoverinfo="none", hovertemplate=None)

    return fig


def alternative_update(
    fig: go.Figure,
    new_df: pd.DataFrame,
    which="temporal",
    normalised=True,
    subselect=None,
):
    if len(fig.data) > 6:
        fig.data = fig.data[:6]
    fig.layout.clickmode = "event+select"

    n_neurons = np.unique(new_df["unit"].to_numpy()).shape[0]
    if np.array((which == "temporal")).any():
        df = df[df["feature"].isin(TEMPORAL_FEATURES)]
    elif np.array((which == "waveform")).any():
        df = df[df["feature"].isin(WAVEFORM_FEATURES)]
    elif isinstance(which, list):
        df = df[df["feature"].isin(which)]
    else:
        raise ValueError("which must be either temporal or waveform")

    colors = ["orange", "blue", "green", "brown", "red", "purple"]
    color_dict = dict(zip(["PkC_cs", "PkC_ss", "GoC", "GrC", "MLI", "MFB"], colors))

    # Adding highlighted point if any
    if subselect is not None:
        highlighted_point = new_df[new_df["unit"] == subselect]
        highlighted_label = highlighted_point["label"].to_numpy()[0]
        highlighted_custom_data = list(
            zip(
                highlighted_point["dp"].to_numpy(),
                highlighted_point["unit"].to_numpy(),
                highlighted_point["raw_value"].to_numpy(),
                highlighted_point["color"].to_numpy(),
                highlighted_point["plotting_id"].to_numpy(),
            )
        )

        fig.add_trace(
            go.Scatter(
                y=highlighted_point["normalised_value"].to_numpy()
                if normalised
                else highlighted_point["raw_value"].to_numpy(),
                x=highlighted_point["feature"].to_numpy(),
                marker=dict(size=12, line=dict(width=2, color="DarkSlateGrey")),
                marker_color=color_dict[highlighted_label],
                name=f"{highlighted_label} {subselect}",
                legendgroup=highlighted_label,
                line=dict(dash="dot"),
                # showlegend=False,
                text=[highlighted_label]
                * len(highlighted_point["normalised_value"].to_numpy()),
                customdata=highlighted_custom_data,
                hovertemplate="<b> %{text} </b><br><br>"
                + "Feature: %{x}<br>"
                + "Raw value: %{highlighted_customdata[2]}<br>"
                + "Source: %{highlighted_customdata[0]}, unit %{highlighted_customdata[1]}"
                + "<extra></extra>",
            )
        )

    fig.for_each_trace(
        lambda trace: trace.update(
            line=dict(
                color="rgba"
                + str(c.to_rgba(color_dict[trace.legendgroup])[:-1] + (0.5,))
            ),
            fillcolor="rgba"
            + str(c.to_rgba(color_dict[trace.legendgroup])[:-1] + (0.5,)),
        ),
    )
    fig.update_traces(hoverinfo="none", hovertemplate=None)

    return fig


def make_joint_figure(
    df: pd.DataFrame,
    which="temporal",
    normalised=True,
    subselect=None,
    lab="hausser",
):
    if lab == "hausser":
        df = df.loc[df["lab"] == "hausser"].copy()
    elif lab == "hull":
        df = df.loc[df["lab"] == "hull"].copy()
    n_neurons = np.unique(df["plotting_id"].to_numpy()).shape[0]

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

    fig = go.Figure()
    for lab in np.unique(df["lab"].to_numpy()):
        plotting_df = df[df["lab"] == lab]
        if len(plotting_df) == 0:
            continue
        good_neurons = plotting_df[plotting_df["color"] != "gray"]
        grey_neurons = plotting_df[plotting_df["color"] == "gray"]
        for i, label in enumerate(["PkC_cs", "PkC_ss", "GoC", "GrC", "MLI", "MFB"]):
            if len(plotting_df[plotting_df["label"] == label]) == 0:
                continue

            neuron_color = good_neurons[good_neurons["label"] == label][
                "color"
            ].to_numpy()[0]

            custom_data_good = list(
                zip(
                    good_neurons[good_neurons["label"] == label]["dp"].to_numpy(),
                    good_neurons[good_neurons["label"] == label]["unit"].to_numpy(),
                    good_neurons[good_neurons["label"] == label][
                        "raw_value"
                    ].to_numpy(),
                    good_neurons[good_neurons["label"] == label]["color"].to_numpy(),
                    good_neurons[good_neurons["label"] == label][
                        "plotting_id"
                    ].to_numpy(),
                )
            )

            custom_data_grey = list(
                zip(
                    grey_neurons[grey_neurons["label"] == label]["dp"].to_numpy(),
                    grey_neurons[grey_neurons["label"] == label]["unit"].to_numpy(),
                    grey_neurons[grey_neurons["label"] == label][
                        "raw_value"
                    ].to_numpy(),
                    grey_neurons[grey_neurons["label"] == label]["color"].to_numpy(),
                    grey_neurons[grey_neurons["label"] == label][
                        "plotting_id"
                    ].to_numpy(),
                )
            )

            fig.add_trace(
                go.Box(
                    y=good_neurons[good_neurons["label"] == label][
                        "joint_normalised_value"
                    ].to_numpy()
                    if normalised
                    else good_neurons[good_neurons["label"] == label][
                        "raw_value"
                    ].to_numpy(),
                    x=good_neurons[good_neurons["label"] == label][
                        "feature"
                    ].to_numpy(),
                    name=f'{lab.capitalize()} {label} (n = {plotting_df["label"].value_counts()[label] // len(np.unique(plotting_df["feature"].to_numpy()))})',
                    marker_color=neuron_color,
                    offsetgroup=label,
                    legendgroup=label,
                    marker={"opacity": 0},
                    text=[label]
                    * len(
                        good_neurons[good_neurons["label"] == label][
                            "joint_normalised_value"
                        ].to_numpy()
                    ),
                    customdata=custom_data_good,
                    hovertemplate="<b> %{text} </b><br><br>"
                    + "Feature: %{x}<br>"
                    + "Raw value: %{customdata[2]}<br>"
                    + "Source: %{customdata[0]}, unit %{customdata[1]}"
                    + "<extra></extra>",
                )
            )

            fig.add_trace(
                go.Box(
                    y=good_neurons[good_neurons["label"] == label][
                        "joint_normalised_value"
                    ].to_numpy()
                    if normalised
                    else good_neurons[good_neurons["label"] == label][
                        "raw_value"
                    ].to_numpy(),
                    x=good_neurons[good_neurons["label"] == label][
                        "feature"
                    ].to_numpy(),
                    name=f'{lab.capitalize()} {label} (n = {plotting_df["label"].value_counts()[label] // len(np.unique(plotting_df["feature"].to_numpy()))})',
                    marker_color=neuron_color,
                    boxpoints="all",
                    jitter=0.6,
                    pointpos=0,
                    offsetgroup=label,
                    legendgroup=label,
                    # legendgrouptitle=dict(text=label),
                    line=dict(color="rgba(0,0,0,0)"),
                    fillcolor="rgba(0,0,0,0)",
                    showlegend=False,
                    text=[label]
                    * len(
                        good_neurons[good_neurons["label"] == label][
                            "joint_normalised_value"
                        ].to_numpy()
                    ),
                    customdata=custom_data_good,
                    hovertemplate="<b> %{text} </b><br><br>"
                    + "Feature: %{x}<br>"
                    + "Raw value: %{customdata[2]}<br>"
                    + "Source: %{customdata[0]}, unit %{customdata[1]}"
                    + "<extra></extra>",
                )
            )

            fig.add_trace(
                go.Box(
                    y=grey_neurons[grey_neurons["label"] == label][
                        "joint_normalised_value"
                    ].to_numpy()
                    if normalised
                    else grey_neurons[grey_neurons["label"] == label][
                        "raw_value"
                    ].to_numpy(),
                    x=grey_neurons[grey_neurons["label"] == label][
                        "feature"
                    ].to_numpy(),
                    name=f'{lab.capitalize()} {label} (n = {plotting_df["label"].value_counts()[label] // len(np.unique(plotting_df["feature"].to_numpy()))})',
                    marker_color="gray",
                    boxpoints="all",
                    jitter=0.6,
                    pointpos=0,
                    offsetgroup=label,
                    legendgroup=label,
                    # legendgrouptitle=dict(text=label),
                    line=dict(color="rgba(0,0,0,0)"),
                    fillcolor="rgba(0,0,0,0)",
                    showlegend=False,
                    text=[label]
                    * len(
                        grey_neurons[grey_neurons["label"] == label][
                            "joint_normalised_value"
                        ].to_numpy()
                    ),
                    customdata=custom_data_grey,
                    hovertemplate="<b> %{text} </b><br><br>"
                    + "Feature: %{x}<br>"
                    + "Raw value: %{customdata[2]}<br>"
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
        )
        fig.update_traces(
            marker=dict(size=1, line=dict(width=2, color="DarkSlateGrey")),
            selector=dict(mode="markers"),
        )

        fig.update_traces(hoverinfo="none", hovertemplate=None)

    return fig


def make_joint_figure_side_by_side(
    df: pd.DataFrame,
    which="temporal",
    normalised=True,
    subselect=None,
    lab="hausser",
):
    if lab == "hausser":
        df = df.loc[df["lab"] == "hausser"].copy()
    elif lab == "hull":
        df = df.loc[df["lab"] == "hull"].copy()
    n_neurons = np.unique(df["plotting_id"].to_numpy()).shape[0]

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

    fig = go.Figure()

    for i, label in enumerate(["PkC_cs", "PkC_ss", "GoC", "GrC", "MLI", "MFB"]):
        for lab in np.unique(df["lab"].to_numpy()):
            plotting_df = df.loc[(df["lab"] == lab) & (df["label"] == label)]
            if len(plotting_df) == 0:
                continue

            good_neurons = plotting_df[plotting_df["color"] != "gray"]
            grey_neurons = plotting_df[plotting_df["color"] == "gray"]

            neuron_color = good_neurons[good_neurons["label"] == label][
                "color"
            ].to_numpy()[0]

            custom_data_good = list(
                zip(
                    good_neurons[good_neurons["label"] == label]["dp"].to_numpy(),
                    good_neurons[good_neurons["label"] == label]["unit"].to_numpy(),
                    good_neurons[good_neurons["label"] == label][
                        "raw_value"
                    ].to_numpy(),
                    good_neurons[good_neurons["label"] == label]["color"].to_numpy(),
                    good_neurons[good_neurons["label"] == label][
                        "plotting_id"
                    ].to_numpy(),
                )
            )

            custom_data_grey = list(
                zip(
                    grey_neurons[grey_neurons["label"] == label]["dp"].to_numpy(),
                    grey_neurons[grey_neurons["label"] == label]["unit"].to_numpy(),
                    grey_neurons[grey_neurons["label"] == label][
                        "raw_value"
                    ].to_numpy(),
                    grey_neurons[grey_neurons["label"] == label]["color"].to_numpy(),
                    grey_neurons[grey_neurons["label"] == label][
                        "plotting_id"
                    ].to_numpy(),
                )
            )

            fig.add_trace(
                go.Box(
                    y=good_neurons[good_neurons["label"] == label][
                        "joint_normalised_value"
                    ].to_numpy()
                    if normalised
                    else good_neurons[good_neurons["label"] == label][
                        "raw_value"
                    ].to_numpy(),
                    x=good_neurons[good_neurons["label"] == label][
                        "feature"
                    ].to_numpy(),
                    name=f'{lab.capitalize()} {label} (n = {plotting_df["label"].value_counts()[label] // len(np.unique(plotting_df["feature"].to_numpy()))})',
                    marker_color=neuron_color,
                    offsetgroup=str(label) + str(lab),
                    legendgroup=label,
                    marker={"opacity": 0},
                    text=[label]
                    * len(
                        good_neurons[good_neurons["label"] == label][
                            "joint_normalised_value"
                        ].to_numpy()
                    ),
                    customdata=custom_data_good,
                    hovertemplate="<b> %{text} </b><br><br>"
                    + "Feature: %{x}<br>"
                    + "Raw value: %{customdata[2]}<br>"
                    + "Source: %{customdata[0]}, unit %{customdata[1]}"
                    + "<extra></extra>",
                )
            )

            fig.add_trace(
                go.Box(
                    y=good_neurons[good_neurons["label"] == label][
                        "joint_normalised_value"
                    ].to_numpy()
                    if normalised
                    else good_neurons[good_neurons["label"] == label][
                        "raw_value"
                    ].to_numpy(),
                    x=good_neurons[good_neurons["label"] == label][
                        "feature"
                    ].to_numpy(),
                    name=f'{lab.capitalize()} {label} (n = {plotting_df["label"].value_counts()[label] // len(np.unique(plotting_df["feature"].to_numpy()))})',
                    marker_color=neuron_color,
                    boxpoints="all",
                    jitter=0.6,
                    pointpos=0,
                    offsetgroup=str(label) + str(lab),
                    legendgroup=label,
                    # legendgrouptitle=dict(text=label),
                    line=dict(color="rgba(0,0,0,0)"),
                    fillcolor="rgba(0,0,0,0)",
                    showlegend=False,
                    text=[label]
                    * len(
                        good_neurons[good_neurons["label"] == label][
                            "joint_normalised_value"
                        ].to_numpy()
                    ),
                    customdata=custom_data_good,
                    hovertemplate="<b> %{text} </b><br><br>"
                    + "Feature: %{x}<br>"
                    + "Raw value: %{customdata[2]}<br>"
                    + "Source: %{customdata[0]}, unit %{customdata[1]}"
                    + "<extra></extra>",
                )
            )

            fig.add_trace(
                go.Box(
                    y=grey_neurons[grey_neurons["label"] == label][
                        "joint_normalised_value"
                    ].to_numpy()
                    if normalised
                    else grey_neurons[grey_neurons["label"] == label][
                        "raw_value"
                    ].to_numpy(),
                    x=grey_neurons[grey_neurons["label"] == label][
                        "feature"
                    ].to_numpy(),
                    name=f'{lab.capitalize()} {label} (n = {plotting_df["label"].value_counts()[label] // len(np.unique(plotting_df["feature"].to_numpy()))})',
                    marker_color="gray",
                    boxpoints="all",
                    jitter=0.6,
                    pointpos=0,
                    offsetgroup=str(label) + str(lab),
                    legendgroup=label,
                    # legendgrouptitle=dict(text=label),
                    line=dict(color="rgba(0,0,0,0)"),
                    fillcolor="rgba(0,0,0,0)",
                    showlegend=False,
                    text=[label]
                    * len(
                        grey_neurons[grey_neurons["label"] == label][
                            "joint_normalised_value"
                        ].to_numpy()
                    ),
                    customdata=custom_data_grey,
                    hovertemplate="<b> %{text} </b><br><br>"
                    + "Feature: %{x}<br>"
                    + "Raw value: %{customdata[2]}<br>"
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
        )
        fig.update_traces(
            marker=dict(size=1, line=dict(width=2, color="DarkSlateGrey")),
            selector=dict(mode="markers"),
        )

        fig.update_traces(hoverinfo="none", hovertemplate=None)

    return fig
