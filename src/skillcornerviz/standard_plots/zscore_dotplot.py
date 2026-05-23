"""
Michael Nanopoulos
Z-Score Horizontal Dot Plot

Visualises z-score positions for a set of metrics grouped into categories.
Each row is one metric; groups appear as bold section headers.
A grey bar spans the population min–max per metric; coloured dots mark the
highlighted data points (primary and/or secondary highlight groups).
"""
from __future__ import annotations

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
from matplotlib.transforms import blended_transform_factory

from skillcornerviz.utils.constants import (
    BASE_COLOR, PRIMARY_HIGHLIGHT_COLOR, SECONDARY_HIGHLIGHT_COLOR,
    DARK_PRIMARY_HIGHLIGHT_COLOR, DARK_SECONDARY_HIGHLIGHT_COLOR,
    TEXT_COLOR, FIVE_COLORS,
)
from skillcornerviz.utils._fonts import load_shentox_fonts

def plot_zscore_dotplot(
    df: pd.DataFrame,
    questions: dict,
    primary_highlight_group: list,
    secondary_highlight_group: list | None = None,
    data_point_label: str = 'name',
    data_point_id: str = 'name',
    value_col_suffix: str = '_z',
    color_map: dict | None = None,
    y_labels: dict | None = None,
    primary_highlight_color: str = PRIMARY_HIGHLIGHT_COLOR,
    secondary_highlight_color: str = SECONDARY_HIGHLIGHT_COLOR,
    base_color: str = BASE_COLOR,
    x_range: tuple = (-3, 3),
    dot_size: int = 80,
    plot_title: str | None = None,
    subtitle: str | None = None,
    caption: str | None = None,
    group_gap: float = 0.6,
    fontsize: int = 8,
    figsize: tuple = (14, 7),
    dark_mode: bool = False,
    ax: plt.Axes | None = None,
) -> tuple[plt.Figure, plt.Axes]:
    """
    Plot a z-score horizontal dot plot with grouped metric rows.

    Parameters
    ----------
    df : pd.DataFrame
        Full population DataFrame. Must contain `data_point_id` plus metric
        columns named as: metric_base + value_col_suffix (e.g. 'pressures_z').
    questions : dict
        Ordered dict mapping group labels to lists of metric base names.
        Example: {'Type': ['pressures', 'obes'], 'Phase': ['low_block']}
    primary_highlight_group : list
        data_point_id values to show as primary coloured dots.
    secondary_highlight_group : list, optional
        data_point_id values to show as secondary coloured dots.
    data_point_label : str
        Column used for legend labels.
    data_point_id : str
        Column used to identify and filter data points.
    value_col_suffix : str
        Suffix appended to each metric base name to form the z-score column.
        Default '_z'. Pass '' if the metric name is already the full column.
    color_map : dict, optional
        {data_point_id_value: hex_color}. Overrides primary/secondary colours.
    y_labels : dict, optional
        {metric_base_name: 'Custom Label'}. Overrides auto-formatted labels.
    primary_highlight_color : str
    secondary_highlight_color : str
    base_color : str
        Colour of the population range bars.
    x_range : tuple
        (x_min, x_max) for the horizontal axis. Default (-3, 3).
    dot_size : int
    plot_title : str, optional
    subtitle : str, optional
    caption : str, optional
        Small footnote at the bottom-left of the figure.
    group_gap : float
        Extra vertical space before each new group header. Default 0.6.
    figsize : tuple
    dark_mode : bool
    ax : plt.Axes, optional
        Axes to draw on. Creates a new figure if None.

    Returns
    -------
    fig, ax
    """
    load_shentox_fonts()
    plt.rcParams['font.family'] = 'Shentox'
    if secondary_highlight_group is None:
        secondary_highlight_group = []

    if dark_mode:
        background_color = TEXT_COLOR
        text_color = 'white'
        primary_highlight_color = DARK_PRIMARY_HIGHLIGHT_COLOR
        secondary_highlight_color = DARK_SECONDARY_HIGHLIGHT_COLOR
    else:
        background_color = 'white'
        text_color = TEXT_COLOR

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)
    ax.grid(False)

    # Build y-positions
    y_pos = {}
    y_group_labels = {}
    y = 0
    current_group = None

    for group, metrics in questions.items():
        if current_group is not None:
            y += group_gap
        y_group_labels[group] = y
        y += 1
        current_group = group
        for m in metrics:
            y_pos[m] = y
            y += 1

    n_rows = y
    x_min, x_max = x_range

    # Population range bars
    for m, yp in y_pos.items():
        col = m + value_col_suffix
        if col not in df.columns:
            continue
        ax.plot([df[col].min(), df[col].max()], [yp, yp],
                color=base_color, lw=4,
                alpha=0.1 if dark_mode else 0.3,
                solid_capstyle='round', zorder=1)

    # Faint vertical grid lines
    grid_alpha = 0.04 if dark_mode else 0.1
    for v in np.arange(x_min, x_max + 0.001, 0.5):
        if v == 0:
            continue
        ax.axvline(v, color=text_color, lw=0.5, alpha=grid_alpha, zorder=1)

    # Zero line
    ax.axvline(0, color=text_color, lw=1.2, alpha=0.5, zorder=2)

    # Assign cycling colours to secondary group
    secondary_color_map = {
        dp_id: FIVE_COLORS[i % len(FIVE_COLORS)]
        for i, dp_id in enumerate(secondary_highlight_group)
    }

    def get_color(dp_id):
        if color_map and dp_id in color_map:
            return color_map[dp_id]
        if dp_id in secondary_color_map:
            return secondary_color_map[dp_id]
        return primary_highlight_color

    # Background (population) dots
    bg_df = df[~df[data_point_id].isin(
        list(primary_highlight_group) + list(secondary_highlight_group)
    )].copy()

    for _, row in bg_df.iterrows():
        xs, ys = [], []
        for m, yp in y_pos.items():
            col = m + value_col_suffix
            if col in row.index and pd.notna(row[col]):
                xs.append(row[col])
                ys.append(yp)
        ax.scatter(xs, ys, s=dot_size * 0.6, color=BASE_COLOR,
                   alpha=0.25, edgecolors='none', zorder=3)

    # Secondary dots
    secondary_df = df[df[data_point_id].isin(secondary_highlight_group)].copy()
    for _, row in secondary_df.iterrows():
        xs, ys = [], []
        for m, yp in y_pos.items():
            col = m + value_col_suffix
            if col in row.index and pd.notna(row[col]):
                xs.append(row[col])
                ys.append(yp)
        ax.scatter(xs, ys, s=dot_size, color=get_color(row[data_point_id]),
                   alpha=0.75, edgecolors=background_color, linewidths=0.5, zorder=4)

    # Primary dots (largest, top z-order)
    primary_df = df[df[data_point_id].isin(primary_highlight_group)].copy()
    for _, row in primary_df.iterrows():
        xs, ys = [], []
        for m, yp in y_pos.items():
            col = m + value_col_suffix
            if col in row.index and pd.notna(row[col]):
                xs.append(row[col])
                ys.append(yp)
        ax.scatter(xs, ys, s=dot_size * 1.5, color=get_color(row[data_point_id]),
                   alpha=1, edgecolors=background_color, linewidths=0.8, zorder=5)

    # Group section headers
    trans = blended_transform_factory(ax.transAxes, ax.transData)
    sep_alpha = 0.08 if dark_mode else 0.15

    for group, yp in y_group_labels.items():
        ax.axhline(yp - 0.5, color=text_color, lw=1, alpha=sep_alpha, zorder=2)
        ax.text(-0.02, yp + 0.4, group.upper(),
                transform=trans, ha='right', va='bottom',
                fontweight='bold', fontsize=fontsize + 1,
                color=text_color, alpha=0.65, zorder=5,
                path_effects=[pe.withStroke(linewidth=1.5,
                                            foreground=background_color, alpha=1)])
        underline_width = 0.18
        ax.plot([-underline_width - 0.02, -0.02], [yp + 0.3, yp + 0.3],
                transform=trans, color=text_color, lw=1, alpha=0.4, zorder=5)

    # Y-axis metric labels
    ax.set_yticks(list(y_pos.values()))
    ax.set_yticklabels(
        [(y_labels or {}).get(m, m.replace('_', ' ').title()).upper() for m in y_pos],
        fontsize=fontsize, color=text_color
    )
    ax.tick_params(axis='y', length=0, pad=6)

    # X-axis
    ax.set_xlim(x_min, x_max)
    tick_vals = np.arange(x_min, x_max + 0.001, 0.5)
    ax.set_xticks(tick_vals)
    ax.set_xticklabels(
        [str(int(v)) if v == int(v) else f'{v:.1f}' for v in tick_vals],
        fontsize=fontsize - 1, color=text_color
    )
    ax.tick_params(axis='x', length=0)
    ax.set_ylim(n_rows + 0.8, -0.8)

    # Axis direction annotations
    for x_pos, txt, ha in [
        (0,     'Average',                          'center'),
        (x_min, '<-- Significantly Below Average',  'left'),
        (x_max, 'Significantly Above Average -->',  'right'),
    ]:
        ax.text(x_pos, -0.5, txt,
                ha=ha, va='center', style='italic',
                fontsize=fontsize - 1, color=text_color, alpha=0.5,
                path_effects=[pe.withStroke(linewidth=1.5,
                                            foreground=background_color, alpha=1)])

    for spine in ax.spines.values():
        spine.set_visible(False)

    # Legend
    labeled_df = df[df[data_point_id].isin(
        list(primary_highlight_group) + list(secondary_highlight_group)
    )].drop_duplicates(subset=[data_point_id])

    handles = [
        Line2D([0], [0], marker='o', linestyle='none',
               markerfacecolor=get_color(row[data_point_id]),
               markeredgecolor='none',
               markersize=9, label=row[data_point_label])
        for _, row in labeled_df.iterrows()
    ]
    legend = ax.legend(handles=handles, ncol=len(handles),
                       loc='lower center', bbox_to_anchor=(0.5, 1.04),
                       frameon=False, fontsize=fontsize + 1)
    for handle, text in zip(legend.legend_handles, legend.get_texts()):
        text.set_color(handle.get_markerfacecolor())
        text.set_fontweight('bold')

    if plot_title is not None:
        ax.set_title(plot_title, weight='bold', color=text_color,
                     fontsize=fontsize + 5, loc='left', pad=8)
    if subtitle is not None:
        ax.annotate(subtitle,
                    xy=(0, 1), xycoords='axes fraction',
                    xytext=(0, 8 if plot_title is None else 28),
                    textcoords='offset points',
                    ha='left', va='bottom',
                    fontsize=fontsize, color=text_color, alpha=0.5)
    if caption:
        fig.text(0.01, -0.01, caption,
                 ha='left', va='top',
                 fontsize=fontsize - 1.5, color=text_color, alpha=0.6)

    plt.tight_layout()
    plt.show()

    return fig, ax
