"""
Table Grid (Heatmap)
Renders a seaborn heatmap where rows are entities (e.g. teams or players),
columns are metrics, and cell colour encodes a z-score or any normalised value
clipped to ±2.5. Supports optional column gap dividers between metric groups.

Data is expected to already be z-scored before being passed in.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

from skillcornerviz.utils.constants import TEXT_COLOR
from skillcornerviz.utils._fonts import load_shentox_fonts

_CMAP = LinearSegmentedColormap.from_list(
    'sc_table_grid',
    ['#FF1A1A', '#FDA4A4', '#D9D9D6', '#99E59A', '#00C800'],
    N=5,
)
_NORM_BOUNDS = (-2.6, 2.6)
_CBAR_LABELS = [
    'Very Low\nFor Sample',
    'Low For\nSample',
    'Average For\nSample',
    'High For\nSample',
    'Very High\nFor Sample',
]


def plot_table_grid(df: pd.DataFrame,
                    metrics: list,
                    labels: list,
                    data_point_id: str,
                    highlight_group: list | None = None,
                    sort_by: str | None = None,
                    sort_ascending: bool = False,
                    gap_positions: list | None = None,
                    rotate_xticks: bool = True,
                    figsize: tuple = (10, 6),
                    plot_title: str = '') -> tuple[plt.Figure, plt.Axes]:
    """
    Plot a colour-coded heatmap grid of z-scored metrics.

    Parameters
    ----------
    df : DataFrame
        Must contain `data_point_id`, optional `sort_by`, and all columns in `metrics`.
        Values are expected to be z-scores (or any normalised metric); they are
        clipped to ±2.5 for display purposes.
    metrics : list
        Column names to display as heatmap columns.
    labels : list
        Display labels corresponding to `metrics`. Must be the same length.
    data_point_id : str
        Column used as row labels (e.g. 'team_shortname', 'player_name').
    highlight_group : list, optional
        If provided, only rows whose `data_point_id` value is in this list are displayed.
    sort_by : str, optional
        Column to sort rows by before plotting. Rows are unsorted if None.
    sort_ascending : bool
        Sort direction when `sort_by` is provided. Default False (descending).
    gap_positions : list[int], optional
        Indices at which to insert blank separator columns between metric groups.
        Applied to the original `metrics` list (before any internal reindexing).
    rotate_xticks : bool
        Rotate column header labels 45°. Default True.
    figsize : tuple
    plot_title : str

    Returns
    -------
    fig, ax
    """
    load_shentox_fonts()
    plt.rcParams['font.family'] = 'Shentox'
    if len(metrics) != len(labels):
        raise ValueError(f"metrics and labels must be the same length ({len(metrics)} vs {len(labels)})")

    if gap_positions is None:
        gap_positions = []

    plot_df = df[[data_point_id] + metrics].copy()

    if highlight_group is not None:
        plot_df = plot_df[plot_df[data_point_id].isin(highlight_group)]

    if sort_by is not None and sort_by in df.columns:
        plot_df = plot_df.assign(_sort=df[sort_by]).sort_values('_sort', ascending=sort_ascending).drop(columns='_sort')

    plot_df = plot_df.set_index(data_point_id)[metrics]
    display_labels = list(labels)

    # Clip to ±2.5 for colour scale
    plot_df = plot_df.clip(lower=-2.5, upper=2.5)

    # Insert blank gap columns
    for offset, pos in enumerate(sorted(gap_positions)):
        adjusted = pos + offset
        plot_df = pd.concat([
            plot_df.iloc[:, :adjusted],
            pd.DataFrame(np.nan, index=plot_df.index, columns=[None]),
            plot_df.iloc[:, adjusted:],
        ], axis=1)
        display_labels.insert(adjusted, '')

    norm = plt.Normalize(*_NORM_BOUNDS)

    fig, ax = plt.subplots(figsize=figsize)

    if plot_title:
        ax.set_title(plot_title, fontsize=12, fontweight='bold', color=TEXT_COLOR, pad=15)

    heatmap = sns.heatmap(plot_df, annot=False, cmap=_CMAP, fmt='.1f',
                          linewidths=0.5, zorder=3, norm=norm, ax=ax)

    ax.set_ylabel('')
    ax.xaxis.set_label_position('top')
    ax.tick_params(axis='x', colors=TEXT_COLOR, labelsize=10, length=0,
                   rotation=45 if rotate_xticks else 0,
                   top=True, labeltop=True, bottom=False, labelbottom=False)
    ax.tick_params(axis='y', colors=TEXT_COLOR, labelsize=9, length=0)
    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels(display_labels, fontweight='bold',
                       ha='left' if rotate_xticks else 'center')

    ax.grid(axis='y', color=TEXT_COLOR, alpha=0.2, lw=0.5, linestyle='--')

    cbar = heatmap.collections[0].colorbar
    cbar.set_ticks([-2, -1, 0, 1, 2])
    cbar.set_ticklabels(_CBAR_LABELS, fontsize=9)

    plt.tight_layout()
    plt.show()

    return fig, ax
