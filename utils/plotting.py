import plotly.graph_objects as go
import pandas as pd
import numpy as np
from matplotlib import colors as c

N_TEMPORAL_FEATURES = 15


def make_figure(
    new_df: pd.DataFrame, which="temporal", normalised=True, subselect=None
):
    n_neurons = np.unique(new_df["unit"].to_numpy()).shape[0]
    if np.array((which == "temporal")).any():
        new_df = new_df.iloc[: N_TEMPORAL_FEATURES * n_neurons]
        update_title = True
    elif np.array((which == "waveform")).any():
        new_df = new_df.iloc[N_TEMPORAL_FEATURES * n_neurons :]
        update_title = True
    elif isinstance(which, list):
        new_df = new_df[new_df["feature"].isin(which)]
        update_title = False
    else:
        raise ValueError("which must be either temporal or waveform")

    fig = go.Figure()
    colors = ["orange", "blue", "green", "brown", "red", "purple"]
    color_dict = dict(zip(["PkC_cs", "PkC_ss", "GoC", "GrC", "MLI", "MFB"], colors))
    for i, label in enumerate(["PkC_cs", "PkC_ss", "GoC", "GrC", "MLI", "MFB"]):

        custom_data = list(
            zip(
                new_df[new_df["label"] == label]["dp"].to_numpy(),
                new_df[new_df["label"] == label]["unit"].to_numpy(),
                new_df[new_df["label"] == label]["raw_value"].to_numpy(),
                new_df[new_df["label"] == label]["color"].to_numpy(),
            )
        )

        fig.add_trace(
            go.Box(
                y=new_df[new_df["label"] == label]["normalised_value"].to_numpy()
                if normalised
                else new_df[new_df["label"] == label]["raw_value"].to_numpy(),
                x=new_df[new_df["label"] == label]["feature"].to_numpy(),
                name=f'{label} (n = {new_df["label"].value_counts()[label] // len(np.unique(new_df["feature"].to_numpy()))})',
                marker_color=colors[i],
                boxpoints="all",
                jitter=0.6,
                pointpos=0,
                legendgroup=label,
                text=[label]
                * len(new_df[new_df["label"] == label]["normalised_value"].to_numpy()),
                customdata=custom_data,
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
    )  #

    fig.update_traces(hoverinfo="none", hovertemplate=None)

    return fig


def update_on_click(
    fig: go.Figure,
    new_df: pd.DataFrame,
    which="temporal",
    normalised=True,
    subselect=None,
):
    # This is to remove previously added highlighted points!
    if len(fig.data) > 6:
        fig.data = fig.data[:6]

    n_neurons = np.unique(new_df["unit"].to_numpy()).shape[0]
    if np.array((which == "temporal")).any():
        new_df = new_df.iloc[: N_TEMPORAL_FEATURES * n_neurons]
    elif np.array((which == "waveform")).any():
        new_df = new_df.iloc[N_TEMPORAL_FEATURES * n_neurons :]
    elif isinstance(which, list):
        new_df = new_df[new_df["feature"].isin(which)]
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
            )
        )
        # fig.add_trace(
        #     go.Box(
        #         y=highlighted_point["normalised_value"].to_numpy()
        #         if normalised
        #         else highlighted_point["raw_value"].to_numpy(),
        #         x=highlighted_point["feature"].to_numpy(),
        #         marker=dict(size=12, line=dict(width=2, color="DarkSlateGrey")),
        #         marker_color=color_dict[highlighted_label],
        #         name=f"{highlighted_label} {subselect}",
        #         boxpoints="all",
        #         line=dict(color="rgba(0,0,0,0)"),
        #         fillcolor="rgba(0,0,0,0)",
        #         jitter=0.6,
        #         pointpos=0,
        #         legendgroup=highlighted_label,
        #         # showlegend=False,
        #         text=[highlighted_label]
        #         * len(highlighted_point["normalised_value"].to_numpy()),
        #         customdata=highlighted_custom_data,
        #         hovertemplate="<b> %{text} </b><br><br>"
        #         + "Feature: %{x}<br>"
        #         + "Raw value: %{highlighted_customdata[2]}<br>"
        #         + "Source: %{highlighted_customdata[0]}, unit %{highlighted_customdata[1]}"
        #         + "<extra></extra>",
        #     )
        # )
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
        new_df = new_df.iloc[: N_TEMPORAL_FEATURES * n_neurons]
    elif np.array((which == "waveform")).any():
        new_df = new_df.iloc[N_TEMPORAL_FEATURES * n_neurons :]
    elif isinstance(which, list):
        new_df = new_df[new_df["feature"].isin(which)]
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
