"""
Narrative Ranking Plot
Ranked grid of players × metrics. Each cell is a coloured rectangle (or bubble)
whose colour and size encode percentile rank. Supports dark mode, optional circle
markers with a colorbar, and automatic column-title rotation on overflow.
"""
from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle

from skillcornerviz.utils.constants import TEXT_COLOR, DARK_BASE_COLOR
from skillcornerviz.utils.skillcorner_utils import split_string_with_new_line
from skillcornerviz.utils._fonts import load_shentox_fonts

_BUBBLE_MAX = 550
_CMAP = ListedColormap(['#FF1A1A', '#FDA4A4', '#D9D9D6', '#99E59A', '#00C800'])
_PCT_BINS = [-0.1, .2, .4, .6, .8, 1.1]


def _ordinal(n: int) -> str:
    if 11 <= (n % 100) <= 13:
        return f'{n}th'
    return f'{n}' + {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')


def plot_ranking(df: pd.DataFrame,
                 questions: dict,
                 highlight_group: list,
                 data_point_label: str = 'player_name',
                 data_point_id: str = 'player_name',
                 split_metric_char: int = 25,
                 user_circles: bool = False,
                 metric_labels: dict | None = None,
                 rotate_col_titles: bool = False,
                 split_col_titles: bool = False,
                 plot_title: str | None = None,
                 dark_mode: bool = False,
                 figsize: tuple = (10, 5),
                 invert_metric_ranks: list | None = None) -> tuple[plt.Figure, plt.Axes]:
    """
    Plot a narrative ranking grid of players × metrics.

    Parameters
    ----------
    df : DataFrame
        Full population DataFrame containing the raw metric columns.
    questions : dict
        Ordered mapping of group labels to lists of metric column names.
        Example: {'Running': ['total_distance_per_90', 'sprint_count_per_90']}
    highlight_group : list
        data_point_id values to display as columns in the grid.
    data_point_label : str
        Column used for column header labels.
    data_point_id : str
        Column used to filter and identify rows.
    split_metric_char : int
        Character limit before a metric label is split across two lines.
    user_circles : bool
        If True, draw circular bubble markers instead of filled rectangles.
    metric_labels : dict, optional
        {metric_col: 'Display Label'}. Overrides auto-formatted labels.
    rotate_col_titles : bool
        Rotate player name column headers 45°.
    split_col_titles : bool
        Split long player names onto two lines.
    plot_title : str, optional
    dark_mode : bool
    figsize : tuple
    invert_metric_ranks : list, optional
        Metric columns where a lower raw value = better rank.

    Returns
    -------
    fig, ax
    """
    load_shentox_fonts()
    plt.rcParams['font.family'] = 'Shentox'
    if invert_metric_ranks is None:
        invert_metric_ranks = []

    facecolor = TEXT_COLOR if dark_mode else 'white'
    textcolor = 'white' if dark_mode else TEXT_COLOR

    metrics = [m for metrics in questions.values() for m in metrics]

    for m in metrics:
        df[m + '_pct_rank'] = df[m].rank(pct=True)
        if m in invert_metric_ranks:
            df[m + '_pct_rank'] = 1 - df[m + '_pct_rank']
        df[m + '_marker_size'] = df[m + '_pct_rank'] * _BUBBLE_MAX
        df[m + '_colour'] = pd.cut(df[m + '_pct_rank'], bins=_PCT_BINS, labels=False, right=True)

    plot_df = df[df[data_point_id].isin(highlight_group)].reset_index()

    n_players = len(plot_df)
    player_spacing = 9 / max(n_players, 7)
    player_xpos = [i * player_spacing for i in range(n_players)]

    n_rows = len(questions) + sum(len(v) for v in questions.values())
    row_label_x = -2.5

    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(facecolor)
    ax.set_facecolor(facecolor)

    i = n_rows - 1
    for group_label, group_metrics in questions.items():
        # Group header row
        ax.text(row_label_x, i, group_label,
                fontweight='bold', fontsize=9, color=textcolor,
                ha='left', va='center', zorder=5,
                path_effects=[pe.withStroke(linewidth=1, foreground=facecolor, alpha=1)])
        i -= 1

        for metric in group_metrics:
            if metric_labels is not None:
                metric_label = metric_labels[metric]
            else:
                metric_label = (metric
                                .replace('count_', '')
                                .replace('_', ' ')
                                .title()
                                .replace('Per 30 Tip', 'P30 TIP'))

            if len(metric_label) > split_metric_char:
                metric_label = split_string_with_new_line(metric_label)

            ax.text(row_label_x, i, metric_label,
                    fontsize=8, color=textcolor, ha='left', va='center', zorder=5,
                    path_effects=[pe.withStroke(linewidth=1, foreground=facecolor, alpha=1)])

            if user_circles:
                ax.axhline(y=i, alpha=0.2, lw=.5, linestyle='--', zorder=2, color=textcolor)
                ax.scatter(player_xpos, [i] * n_players, s=_BUBBLE_MAX,
                           color=facecolor, zorder=3)
                ax.scatter(player_xpos, [i] * n_players, s=_BUBBLE_MAX,
                           color=facecolor, alpha=.2, lw=.5, edgecolor=textcolor, zorder=4)
                scatter = ax.scatter(player_xpos, [i] * n_players,
                                     s=plot_df[metric + '_marker_size'],
                                     c=plot_df[metric + '_colour'],
                                     cmap=_CMAP, alpha=1, zorder=5)
            else:
                ax.axhline(y=i - 0.35, alpha=0.2, lw=.5, linestyle='--', zorder=4, color=textcolor)
                ax.axhline(y=i + 0.35, alpha=0.2, lw=.5, linestyle='--', zorder=4, color=textcolor)

                for j in range(n_players):
                    pct = plot_df[metric + '_pct_rank'].iloc[j]
                    colour_idx = int(plot_df[metric + '_colour'].iloc[j])
                    ax.add_patch(Rectangle(
                        (player_xpos[j] - player_spacing / 2, i - 0.35),
                        width=player_spacing * pct,
                        facecolor=_CMAP.colors[colour_idx],
                        height=0.7, zorder=3))

                    ax.text(player_xpos[j], i,
                            _ordinal(round(pct * 100)),
                            rotation=0, fontweight='bold', fontsize=7, zorder=6,
                            color=textcolor, ha='center', va='center',
                            path_effects=[pe.withStroke(linewidth=1, foreground=facecolor, alpha=1)])
            i -= 1

    # Column headers
    text_objects = []
    for xpos, row in zip(player_xpos, plot_df.itertuples()):
        name = getattr(row, data_point_label)
        title = split_string_with_new_line(name) if split_col_titles else name
        rotation = 45 if rotate_col_titles else 0
        text_objects.append(
            ax.text(xpos, n_rows, title,
                    rotation=rotation, fontweight='bold', fontsize=9,
                    color=textcolor, ha='center', va='center',
                    path_effects=[pe.withStroke(linewidth=1, foreground=facecolor, alpha=1)]))

        if user_circles:
            ax.axvline(x=xpos, alpha=0.2, lw=.5, linestyle='--', zorder=2, color=textcolor)
        else:
            ax.axvline(x=xpos - player_spacing / 2, alpha=0.2, lw=.5, linestyle='--', zorder=4, color=textcolor)

    # Auto-rotate column headers if they overlap
    overlapping = False
    for idx in range(len(text_objects) - 1):
        bbox = text_objects[idx].get_window_extent()
        x_end, _ = ax.transData.inverted().transform((bbox.x1, bbox.y1))
        next_bbox = text_objects[idx + 1].get_window_extent()
        x_start, _ = ax.transData.inverted().transform((next_bbox.x0, next_bbox.y0))
        if x_end >= x_start:
            overlapping = True
            break

    if overlapping:
        for t in text_objects:
            t.set_rotation(30)
            t.set_ha('left')

    if not user_circles:
        ax.axvline(x=player_xpos[-1] + player_spacing / 2, alpha=0.2, lw=.5, linestyle='--', zorder=2,
                   color=textcolor)

    # Fill remaining vertical lines if fewer than 7 players
    for extra in range(n_players, 7):
        ax.axvline(x=(extra * player_spacing) + player_spacing / 2,
                   alpha=0.2, lw=.5, linestyle='--', zorder=2, color=textcolor)

    ax.set_ylim([-1, n_rows])
    for spine in ax.spines.values():
        spine.set_color('none')
    ax.set_xticks([])
    ax.set_yticks([])

    if user_circles:
        cbar = plt.colorbar(scatter, fraction=0.025, aspect=10, pad=0.01,
                            ticks=[0, .8, 1.6, 2.4, 3.2, 4])
        cbar.set_ticklabels(['0%', '20%', '40%', '60%', '80%', '100%'], fontsize=7)
        cbar.set_label('Percentile Rank', fontsize=8, fontweight='bold')

    if plot_title is not None:
        ax.set_title(plot_title, color=textcolor)

    plt.tight_layout()
    plt.show()

    return fig, ax
