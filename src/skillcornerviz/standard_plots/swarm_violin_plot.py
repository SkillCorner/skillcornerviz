"""
Liam Bailey
09/03/2023
SkillCorner Swarm & Violin Plots.
This code defines a function `plot_swarm_violin` that plots a swarm/violin plot
using the seaborn and matplotlib libraries. The function takes several parameters
including the DataFrame (`df`), the columns to plot on the x-axis (`x_metric`)
and y-axis (`y_metric`), the categorical values to include on the y-axis
(`y_groups`), and other optional parameters such as labels, colors, and
highlighting specific data points.
"""
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from adjustText import adjust_text
import seaborn as sns
from matplotlib.ticker import EngFormatter
from skillcornerviz.utils.constants import (
    BASE_COLOR, PRIMARY_HIGHLIGHT_COLOR, SECONDARY_HIGHLIGHT_COLOR,
    DARK_BASE_COLOR, DARK_PRIMARY_HIGHLIGHT_COLOR, DARK_SECONDARY_HIGHLIGHT_COLOR,
    TEXT_COLOR,
)
from skillcornerviz.utils._fonts import load_shentox_fonts

def plot_swarm_violin(df,
                      x_metric,
                      y_metric,
                      y_groups=None,
                      x_label=None,
                      y_group_labels=None,
                      x_unit=None,
                      primary_highlight_group=None,
                      secondary_highlight_group=None,
                      data_point_id='player_name',
                      data_point_label='player_name',
                      label_fontsize=7,
                      fontsize=7,
                      point_size=9,
                      highlight_point_size=10,
                      base_colour=BASE_COLOR,
                      primary_highlight_color=PRIMARY_HIGHLIGHT_COLOR,
                      secondary_highlight_color=SECONDARY_HIGHLIGHT_COLOR,
                      figsize=(8, 4),
                      dark_mode=False):
    """
    Plots a swarm/violin plot.

    Parameters:
    -----------
    df : DataFrame
        Metric DataFrame.
    x_metric : str
        The column in df we want to plot on the x-axis.
    y_metric : str
        The column in df we want to plot on the y-axis. This should be categorical.
    y_groups : list[str], optional
        The categorical values from the y_value column we want to include.
    x_label : str, optional
        The label for the x-axis. This should reflect what the x_value is.
    y_group_labels : list[str], optional
        The labels for the y-axis. This should reflect the data being split across the y-axis.
    x_unit : str, optional
        If we want to add a unit to the axis values. For example % or km/h.
    secondary_highlight_group : list, optional
        A group of players to label & highlight in secondary color.
    primary_highlight_group : list, optional
        A group of players to label & highlight in primary color.
    data_point_id : str, optional
        The column in df that represents the unique identifier for each data point.
    data_point_label : str, optional
        The column in df that contains the labels to display for each data point.
    base_colour : str, optional
        The base color for the plot.
    primary_highlight_color : str, optional
        The highlight color for the primary highlight group.
    secondary_highlight_color : str, optional
        The highlight color for the secondary highlight group.
    figsize : tuple, optional
        The size of the figure (width, height).
    dark_mode : bool, optional
        Enables dark mode styling. (default: False)

    Returns:
    --------
    fig : Figure
        The generated figure.
    ax : Axes
        The axes of the generated plot.
    """

    load_shentox_fonts()
    plt.rcParams['font.family'] = 'Shentox'
    if y_groups is None:
        y_groups = list(df[y_metric].unique())

    if x_label is None:
        x_label = x_metric

    if y_group_labels is None:
        y_group_labels = y_groups

    if primary_highlight_group is None:
        primary_highlight_group = []

    if secondary_highlight_group is None:
        secondary_highlight_group = []

    if dark_mode:
        background_color = TEXT_COLOR
        text_color = 'white'
        label_stroke = 'black'
        if base_colour == BASE_COLOR:
            base_colour = DARK_BASE_COLOR
        if primary_highlight_color == PRIMARY_HIGHLIGHT_COLOR:
            primary_highlight_color = DARK_PRIMARY_HIGHLIGHT_COLOR
        if secondary_highlight_color == SECONDARY_HIGHLIGHT_COLOR:
            secondary_highlight_color = DARK_SECONDARY_HIGHLIGHT_COLOR
    else:
        background_color = 'white'
        text_color = TEXT_COLOR
        label_stroke = 'white'

    plot_data = df[df[y_metric].isin(y_groups)]

    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    violin_parts = sns.violinplot(data=plot_data,
                                  x=x_metric,
                                  y=y_metric,
                                  order=y_groups,
                                  inner=None,
                                  width=1,
                                  zorder=5)

    for pc in violin_parts.collections:
        pc.set_facecolor(text_color)
        pc.set_edgecolor(text_color)
        pc.set_linewidth(0.5)
        pc.set_alpha(0.075)

    plot_data = plot_data.assign(swarm_group='background_group')
    plot_data = plot_data.assign(colour=base_colour)

    plot_data.loc[plot_data[data_point_id].isin(primary_highlight_group), 'swarm_group'] = 'primary_highlight_group'
    plot_data.loc[plot_data[data_point_id].isin(primary_highlight_group), 'colour'] = primary_highlight_color

    plot_data.loc[plot_data[data_point_id].isin(secondary_highlight_group), 'swarm_group'] = 'secondary_highlight_group'
    plot_data.loc[plot_data[data_point_id].isin(secondary_highlight_group), 'colour'] = secondary_highlight_color

    sns.set_palette([secondary_highlight_color, primary_highlight_color])
    hue_order = ['secondary_highlight_group', 'primary_highlight_group']

    plot_data = plot_data.sort_values(by=data_point_id)

    sns.swarmplot(data=plot_data,
                  x=x_metric,
                  y=y_metric,
                  order=y_groups,
                  color=base_colour,
                  alpha=1,
                  size=point_size - (len(y_groups)),
                  edgecolor=text_color,
                  linewidth=0.1)

    if len(primary_highlight_group) > 0 or len(secondary_highlight_group) > 0:
        swarmplots = sns.swarmplot(data=plot_data[plot_data['swarm_group'] != 'background_group'],
                                   x=x_metric,
                                   y=y_metric,
                                   order=y_groups,
                                   hue_order=hue_order,
                                   hue='swarm_group',
                                   alpha=1,
                                   size=highlight_point_size - (len(y_groups)),
                                   edgecolor=text_color,
                                   linewidth=0.3,
                                   zorder=4)

        artists = ax.get_children()
        swarmplot_positions = list(range(len(y_groups) * 2, len(y_groups) * 3))

        for i, group in zip(swarmplot_positions, y_groups):
            group_df = plot_data[plot_data[y_metric] == group].sort_values(by=x_metric, ascending=True).reset_index()
            label_df = group_df[group_df['swarm_group'] != 'background_group'].reset_index()

            offsets = swarmplots.collections[i].get_offsets()

            if len(label_df) == len(offsets):
                label_df.loc[:, 'plotted_metric'] = [tup[0] for tup in offsets]
                label_df.loc[:, 'y'] = [tup[1] for tup in offsets]

                texts = [ax.text(label_df[x_metric].iloc[i],
                                 label_df['y'].iloc[i],
                                 str(label_df[data_point_label].iloc[i]),
                                 color=text_color,
                                 fontsize=fontsize,
                                 fontweight='bold',
                                 zorder=6,
                                 path_effects=[pe.withStroke(linewidth=1,
                                                             foreground=label_stroke,
                                                             alpha=1)]
                                 ) for i in range(len(label_df))]

                adjust_text(texts,
                            ax=ax,
                            add_objects=[artists[i]],
                            expand_points=(1, 3),
                            expand_objects=(1, 3),
                            expand_text=(1, 3),
                            force_objects=.75,
                            force_points=.75,
                            force_text=.75,
                            only_move=dict(points='y', text='y', objects='y'),
                            autoalign='y',
                            arrowprops=dict(arrowstyle="-",
                                            color=text_color,
                                            alpha=1,
                                            lw=.5, zorder=2))

    ax.set_xlabel(x_label, fontweight='bold', fontsize=label_fontsize, color=text_color)
    ax.set_ylabel('', color=text_color)

    ax.tick_params(axis='x', colors=text_color, labelsize=label_fontsize)
    ax.tick_params(axis='y', colors=text_color, labelsize=label_fontsize)

    ax.set_yticklabels(y_group_labels, fontweight='bold', color=text_color)

    if x_unit is not None:
        formatter0 = EngFormatter(unit=x_unit)
        ax.xaxis.set_major_formatter(formatter0)

    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_color(text_color)
    ax.yaxis.set_ticks_position('none')
    ax.spines['left'].set_color('None')

    xmin, xmax = ax.get_xlim()
    if x_unit == '%' and xmax > 110:
        ax.set_xlim([xmin, 110])

    ax.grid(color=text_color,
            axis='both',
            linestyle='--',
            linewidth=0.5,
            alpha=0.25,
            zorder=1)

    ax.legend().remove()

    plt.tight_layout()
    plt.show()

    return fig, ax
