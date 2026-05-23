"""
Liam Bailey
16/03/2023
Bar plot
The plot_bar_chart function is used to generate a bar chart based on the given data.
It accepts various parameters such as the DataFrame (df) containing the metric data,
the column to plot on the axis (x_value), labels for the axis (label) and the
unit of measurement (unit), groups of players to highlight (primary_highlight_group
and secondary_highlight_group), colors for highlighting (primary_highlight and
secondary_highlight_color), and other optional customization parameters.
"""
import matplotlib.pyplot as plt

from matplotlib.ticker import EngFormatter
import pandas as pd
from skillcornerviz.utils.constants import BASE_COLOR, PRIMARY_HIGHLIGHT_COLOR, SECONDARY_HIGHLIGHT_COLOR, \
    DARK_PRIMARY_HIGHLIGHT_COLOR, DARK_SECONDARY_HIGHLIGHT_COLOR, DARK_BASE_COLOR
from skillcornerviz.utils.constants import TEXT_COLOR
from skillcornerviz.utils._fonts import load_shentox_fonts
import matplotlib.patheffects as pe

def plot_bar_chart(df,
                   metric,
                   label=None,
                   unit=None,
                   primary_highlight_group=None,
                   secondary_highlight_group=None,
                   primary_highlight_color=PRIMARY_HIGHLIGHT_COLOR,
                   secondary_highlight_color=SECONDARY_HIGHLIGHT_COLOR,
                   data_point_id='player_name',
                   data_point_label='player_name',
                   plot_title=None,
                   base_color=BASE_COLOR,
                   add_bar_values=False,
                   figsize=(8, 4),
                   lim=None,
                   order=None,
                   vertical=False,
                   rotation=90,
                   fontsize=7,
                   dark_mode=False):
    """
    Plot a bar chart using the given data.

    Parameters
    ----------
    df : DataFrame
        Metric DataFrame.
    metric : str
        The column in df we want to plot on the x-axis.
    label : str, optional
        The label for the x-axis. This should reflect what the x_value is.
    unit : str, optional
        If we want to add a unit to the axis values. For example % or km/h.
    primary_highlight_group : list, optional
        A group of players to label & highlight in Primary Color
    secondary_highlight_group : list, optional
        A group of players to label & highlight in Secondary Color.
    primary_highlight_color : str, optional
        The color for primary highlighted players (default: 'PHYSICAL PITCH').
    secondary_highlight_color : str, optional
        The color for secondary highlighted players (default: 'PHYSICAL PITCH S60' from SkillCorner's Palette).
    data_point_id : str, optional
        The identifier column for each data point (default: 'player_name').
    data_point_label : str, optional
        The label column for each data point (default: 'player_name').
    plot_title : str, optional
        The title of the plot.
    base_color : str, optional
        The base color for the bars (default: 'INNOVATION' from SkillCorner's Palette).
    figsize : tuple, optional
        Tuple (x, y) that defines the dimensions of the figure (default: (8, 4)).
    lim: tuple, optional
       Tuple (x, y) that defines the axis limits
    order : list, optional
        List that orders the axis (dimensional data) (default: None)
    vertical: bool, optional
        Orients the chart vertically or horizontally. (default: False)
    rotation: int, optional
        Rotates the labels if vertical=True is used. (default: 90)
    fontsize: int, optional
        Sets the fontsize used for texts.
    dark_mode: bool, optional
        Enables dark mode styling. (default: False)

    Returns
    -------
    fig : matplotlib.figure.Figure
        The generated figure.
    ax : matplotlib.axes.Axes
        The generated axes.

    """
    load_shentox_fonts()
    plt.rcParams['font.family'] = 'Shentox'
    if metric not in df.columns:
        raise ValueError("The metric you have entered is not in the DataFrame")

    if dark_mode:
        background_color = TEXT_COLOR
        primary_highlight_color = DARK_PRIMARY_HIGHLIGHT_COLOR
        secondary_highlight_color = DARK_SECONDARY_HIGHLIGHT_COLOR
        text_color = 'white'
        edge_color = None
    else:
        background_color = 'white'
        text_color = TEXT_COLOR
        edge_color = None

    if label is None:
        label = unit

    if primary_highlight_group is None:
        primary_highlight_group = []
    if secondary_highlight_group is None:
        secondary_highlight_group = []

    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    if order is None:
        if not vertical:
            df = df.sort_values(by=metric)
        else:
            df = df.sort_values(by=metric, ascending=False)
    else:
        df[data_point_id] = pd.Categorical(df[data_point_id], categories=order, ordered=True)
        df = df.sort_values(data_point_id)
    y_pos = range(0, len(df))

    if not vertical:
        bars = ax.barh(y_pos,
                       df[metric],
                       color=DARK_BASE_COLOR if dark_mode else BASE_COLOR,
                       edgecolor=edge_color,
                       lw=0.5,
                       zorder=3,
                       alpha=1)
        for i, bar in zip(y_pos, bars):
            if df[data_point_id].iloc[i] in secondary_highlight_group or \
                    df[data_point_id].iloc[i] in primary_highlight_group:
                bar.set_color(secondary_highlight_color)
                bar.set_alpha(1)

                if df[data_point_id].iloc[i] in primary_highlight_group:
                    bar.set_color(primary_highlight_color)

                bar.set_edgecolor(edge_color)
                bar.set_linewidth(0.5)

                if add_bar_values:
                    if unit is not None:
                        str_value = str(round(df[metric].iloc[i], 2)) + ' ' + unit + '  '
                    else:
                        str_value = str(round(df[metric].iloc[i], 2)) + '  '

                    ax.text(df[metric].iloc[i], i, str_value,
                            ha='right', va='center',
                            fontsize=fontsize, fontweight='bold',
                            color=background_color if dark_mode else 'white',
                            path_effects=[pe.withStroke(linewidth=.75,
                                                        foreground=text_color,
                                                        alpha=1)])
            else:
                if add_bar_values:
                    if unit is not None:
                        str_value = str(round(df[metric].iloc[i], 2)) + ' ' + unit + '  '
                    else:
                        str_value = str(round(df[metric].iloc[i], 2)) + '  '

                    ax.text(df[metric].iloc[i], i, str_value,
                            ha='right', va='center',
                            fontsize=fontsize, fontweight='bold',
                            color=text_color,
                            path_effects=[pe.withStroke(linewidth=.75,
                                                        foreground=background_color,
                                                        alpha=1)])

        ax.spines['left'].set_color(text_color)
        ax.spines['bottom'].set_color(None)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(df[data_point_label])

        for i, tick_label in enumerate(ax.get_yticklabels()):
            if df[data_point_id].iloc[i] in secondary_highlight_group or \
                    df[data_point_id].iloc[i] in primary_highlight_group:
                tick_label.set_fontproperties({'weight': 'bold', 'size': fontsize})
            else:
                tick_label.set_fontproperties({'size': fontsize})

        if unit is not None:
            formatter0 = EngFormatter(unit=unit)
            ax.xaxis.set_major_formatter(formatter0)
        ax.set_xlabel(label,
                      fontweight='bold',
                      fontsize=fontsize,
                      labelpad=8)
        if lim is not None:
            ax.set_xlim(lim)

    elif vertical:
        bars = ax.bar(y_pos,
                      df[metric],
                      color=DARK_BASE_COLOR if dark_mode else base_color,
                      edgecolor=text_color,
                      lw=0.5,
                      zorder=3,
                      alpha=1)
        for i, bar in zip(y_pos, bars):
            if df[data_point_id].iloc[i] in secondary_highlight_group or \
                    df[data_point_id].iloc[i] in primary_highlight_group:
                bar.set_color(secondary_highlight_color)

                if df[data_point_id].iloc[i] in primary_highlight_group:
                    bar.set_color(primary_highlight_color)

                bar.set_edgecolor(text_color)
                bar.set_linewidth(0.5)

            if add_bar_values:
                if unit is not None:
                    str_value = str(round(df[metric].iloc[i], 2)) + ' ' + unit
                else:
                    str_value = str(round(df[metric].iloc[i], 2))

                ax.text(i, df[metric].iloc[i], str_value,
                        ha='center', va='bottom',
                        fontsize=fontsize, fontweight='bold',
                        color=text_color,
                        path_effects=[pe.withStroke(linewidth=.75,
                                                    foreground=background_color,
                                                    alpha=1)])

        ax.spines['left'].set_color(None)
        ax.spines['bottom'].set_color(text_color)

        ax.set_xticks(y_pos)
        ax.set_xticklabels(df[data_point_label], rotation=rotation)

        for i, tick_label in enumerate(ax.get_xticklabels()):
            if df[data_point_id].iloc[i] in secondary_highlight_group or \
                    df[data_point_id].iloc[i] in primary_highlight_group:
                tick_label.set_fontproperties({'weight': 'bold', 'size': fontsize})
            else:
                tick_label.set_fontproperties({'size': fontsize})

        if unit is not None:
            formatter0 = EngFormatter(unit=unit)
            ax.yaxis.set_major_formatter(formatter0)
        ax.set_ylabel(label,
                      fontweight='bold',
                      fontsize=fontsize)
        if lim is not None:
            ax.set_ylim(lim)

    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    ax.tick_params(axis='x',
                   colors=text_color,
                   labelsize=fontsize,
                   length=0)
    ax.tick_params(axis='y',
                   colors=text_color,
                   labelsize=fontsize)

    ax.yaxis.label.set_color(text_color)
    ax.xaxis.label.set_color(text_color)

    ax.grid(color=text_color,
            axis='both',
            linestyle='--',
            linewidth=0.5,
            alpha=0.25,
            zorder=1)

    if plot_title is not None:
        ax.set_title(plot_title, fontweight='normal', color=text_color)

    for k, spine in ax.spines.items():
        spine.set_zorder(10)
    plt.tight_layout()
    plt.show()

    return fig, ax
