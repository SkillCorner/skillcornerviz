"""
Liam Bailey
15/03/2023
SkillCorner Scatter Plot
The plot_scatter function takes a DataFrame (df) and various parameters to plot
a scatter plot. It allows customization of the x-axis (x_value), y-axis (y_value),
and optional z-axis (z_value) values. Additional parameters control labels,
annotations, units, highlighting, colors, and plot aesthetics. The function returns
the Matplotlib figure and axis objects for further manipulation or display.
"""
import scipy.stats
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import pandas as pd
from adjustText import adjust_text
from skillcornerviz.utils.constants import BASE_COLOR, PRIMARY_HIGHLIGHT_COLOR, SECONDARY_HIGHLIGHT_COLOR, \
    DARK_BASE_COLOR
from skillcornerviz.utils.constants import TEXT_COLOR, DARK_PRIMARY_HIGHLIGHT_COLOR, \
    DARK_SECONDARY_HIGHLIGHT_COLOR
from skillcornerviz.standard_plots.formatting import standard_ax_formating
from skillcornerviz.utils._fonts import load_shentox_fonts
from skillcornerviz.utils.constants import AVERAGE_STRINGS
from skillcornerviz.utils import skillcorner_utils

def plot_scatter(df,
                 x_metric, y_metric, z_metric=None, x_label=None, y_label=None, z_label=None,
                 x_annotation=None, y_annotation=None, custom_annotation=None, annotation_fontsize=6,
                 x_unit=None, y_unit=None,
                 x_sd_highlight=None, y_sd_highlight=None, include_below_average=False,
                 primary_highlight_group=None, secondary_highlight_group=None,
                 primary_highlight_color=PRIMARY_HIGHLIGHT_COLOR, secondary_highlight_color=SECONDARY_HIGHLIGHT_COLOR,
                 base_color=BASE_COLOR,
                 text_color=TEXT_COLOR,
                 data_point_id='player_name', data_point_label='player_name',
                 plot_title=None,
                 avg_line=True,
                 regression_line=False,
                 y_equals_x_line=False,
                 show_left_spine=False,
                 figsize=(8, 4),
                 language='ENG',
                 dark_mode=False):
    """
    Plots a scatter plot based on the provided data and configuration.

    Parameters:
        df (DataFrame): The data to be plotted.
        x_metric (str): The column name of the x-axis values.
        y_metric (str): The column name of the y-axis values.
        z_metric (str, optional): The column name of the z-axis values. Defaults to None.
        x_label (str, optional): The label for the x-axis. Defaults to None.
        y_label (str, optional): The label for the y-axis. Defaults to None.
        z_label (str, optional): The label for the z-axis. Defaults to None.
        x_annotation (str, optional): The annotation for the x-axis corners. Defaults to None.
        y_annotation (str, optional): The annotation for the y-axis corners. Defaults to None.
        custom_annotation (list, optional). A list of 4 annotations clockwise from bottom left. Defaults to None
        annotation_fontsize (int, optional). Font size for annotation, Defaults to 6.
        x_unit (str, optional): The unit of measurement for the x-axis. Defaults to None.
        y_unit (str, optional): The unit of measurement for the y-axis. Defaults to None.
        x_sd_highlight (float, optional): The standard deviation factor for x-axis filtering. Defaults to None.
        y_sd_highlight (float, optional): The standard deviation factor for y-axis filtering. Defaults to None.
        include_below_average (bool, optional): Whether to include datapoints below the average in the label group.
        primary_highlight_group (list, optional): A list of player IDs to highlight as primary. Defaults to None.
        secondary_highlight_group (list, optional): A list of player IDs to highlight as secondary. Defaults to None.
        primary_highlight_color (str, optional): The color for primary highlighted players.
        secondary_highlight_color (str, optional): The color for secondary highlighted players.
        data_point_id (str, optional): The column name for identifying data points. Defaults to 'player_name'.
        data_point_label (str, optional): The column name for labeling data points. Defaults to 'player_name'.
        base_color (str, optional): The base color for the scatter plot.
        text_color (str, optional): The base color used for text
        plot_title (str, Optional): Set a title for your plot. Defaults to None.
        avg_line (bool, optional): Whether to display average lines. Defaults to True.
        regression_line (bool, optional): Whether to display regression line. Defaults to False.
        show_left_spine (bool, optional): Whether to display left spine. Defaults to False.
        figsize (tuple, optional): The figure size of the plot. Defaults to (8, 4).
        language: The language for fixed string on the plot ("Population Average").
    Returns:
        fig, ax: The Matplotlib figure and axis objects.

    """
    load_shentox_fonts()
    plt.rcParams['font.family'] = 'Shentox'
    if x_label is None:
        x_label = x_metric

    if y_label is None:
        y_label = y_metric

    if secondary_highlight_group is None:
        secondary_highlight_group = []
    if primary_highlight_group is None:
        primary_highlight_group = []

    facecolor = TEXT_COLOR if dark_mode else 'white'
    if dark_mode:
        base_color = DARK_BASE_COLOR
        primary_highlight_color = DARK_PRIMARY_HIGHLIGHT_COLOR
        secondary_highlight_color = DARK_SECONDARY_HIGHLIGHT_COLOR
        text_color = 'white'

    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(facecolor)
    ax.set_facecolor(facecolor)

    if z_metric == 'sum_minutes_played':
        sum_minutes_played = (df['minutes_played_per_match'] * df['count_match']) / 10
        df = df.assign(sum_minutes_played=sum_minutes_played)
    if z_metric is not None:
        old_max = df[z_metric].max()
        old_min = df[z_metric].min()
        new_max = 300
        new_min = 50

        old_range = (old_max - old_min)
        new_range = (new_max - new_min)

        sizes = (((df[z_metric] - old_min) * new_range) / old_range) + new_min
        df = df.assign(size=sizes)
    else:
        df = df.assign(size=100)

    if z_metric is not None and z_label is None:
        z_label = z_metric

    label_group = []
    if x_sd_highlight is not None:
        label_group.append(df[(df[x_metric] > df[x_metric].mean() + (x_sd_highlight * df[x_metric].std()))])
        if include_below_average:
            label_group.append(df[(df[x_metric] < df[x_metric].mean() - (x_sd_highlight * df[x_metric].std()))])
    if y_sd_highlight is not None:
        label_group.append(df[(df[y_metric] > df[y_metric].mean() + (y_sd_highlight * df[y_metric].std()))])
        if include_below_average:
            label_group.append(df[(df[y_metric] < df[y_metric].mean() - (y_sd_highlight * df[y_metric].std()))])

    label_group.append(df[(df[data_point_id].isin(secondary_highlight_group)) |
                          (df[data_point_id].isin(primary_highlight_group))])

    label_group = pd.concat(label_group, ignore_index=True).drop_duplicates()

    label_group = label_group.assign(colour=BASE_COLOR)
    label_group.loc[label_group[data_point_id].isin(secondary_highlight_group), 'colour'] = secondary_highlight_color
    label_group.loc[label_group[data_point_id].isin(primary_highlight_group), 'colour'] = primary_highlight_color
    if len(primary_highlight_group) == 0 and len(secondary_highlight_group) == 0:
        label_group = label_group.assign(colour=primary_highlight_color)

    label_group = label_group.assign(fontweight='bold')
    label_group.loc[label_group[data_point_id].isin(secondary_highlight_group), 'fontweight'] = 'bold'
    label_group.loc[label_group[data_point_id].isin(primary_highlight_group), 'fontweight'] = 'bold'

    ax.scatter(df[x_metric],
               df[y_metric],
               c=base_color,
               edgecolor=None if dark_mode else 'white',
               alpha=0.5,
               lw=0.5,
               s=df['size'],
               zorder=3)

    ax.scatter(label_group[x_metric],
               label_group[y_metric],
               c=label_group['colour'],
               edgecolor=None if dark_mode else 'white',
               alpha=1,
               lw=0.5,
               s=label_group['size'],
               zorder=5)

    if len(label_group) > 0:
        texts = [ax.text(label_group[x_metric].iloc[i],
                         label_group[y_metric].iloc[i],
                         str(label_group[data_point_label].iloc[i]),
                         color=text_color,
                         fontsize=6,
                         fontweight=label_group['fontweight'].iloc[i],
                         zorder=6,
                         path_effects=[pe.withStroke(linewidth=1.5,
                                                     foreground=TEXT_COLOR if dark_mode else 'white',
                                                     alpha=1)]
                         ) for i in range(len(label_group))]

        adjust_text(texts, ax=ax, expand_points=(1.5, 1.5),
                    force_text=.5,
                    force_points=.5,
                    ha='left',
                    arrowprops=dict(arrowstyle="-",
                                    color=text_color,
                                    alpha=1,
                                    lw=0.5, zorder=6))

    if avg_line:
        ax.axvline(df[x_metric].mean(),
                   color=text_color, alpha=0.6, lw=1, linestyle='--', zorder=3,
                   label=skillcorner_utils.split_string_with_new_line(AVERAGE_STRINGS[language]['Sample Average']))
        ax.axhline(df[y_metric].mean(),
                   color=text_color, alpha=0.6, lw=1, linestyle='--', zorder=3)

    if regression_line:
        m, b, r_value, p_value, std_err = scipy.stats.linregress(df[x_metric], df[y_metric])
        ax.plot(df[x_metric], m * df[x_metric] + b,
                color=PRIMARY_HIGHLIGHT_COLOR, alpha=1, lw=1.5, linestyle='-', zorder=3,
                label="$r^2$=" + str("{:.2f}".format(r_value ** 2)))

        ax.scatter([], [], c=facecolor, label='Correlation: ' + str(round(df[x_metric].corr(df[y_metric]), 2)))

    if y_equals_x_line:
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        ax.axline((max([xmin, ymin]), max([xmin, ymin])), slope=1, color=SECONDARY_HIGHLIGHT_COLOR, ls='--', label="$y=x$")

    hidden_color = TEXT_COLOR if dark_mode else 'white'
    if z_metric is not None:
        ax.scatter([], [], c=hidden_color, s=5,
                   lw=0.5, edgecolor=hidden_color, zorder=3,
                   label=' ')
        ax.scatter([], [], c=hidden_color if dark_mode else 'white', s=5,
                   lw=0.5, edgecolor=hidden_color, zorder=3,
                   label=z_label + ':\n')
        ax.scatter([], [], c=DARK_BASE_COLOR if dark_mode else 'white', s=df['size'].mean() + (1.5 * df['size'].std()),
                   lw=0.5, edgecolor='white' if dark_mode else 'black', zorder=3,
                   label='High')
        ax.scatter([], [], c=DARK_BASE_COLOR if dark_mode else 'white', s=df['size'].mean(),
                   lw=0.5, edgecolor='white' if dark_mode else 'black', zorder=3,
                   label='Average')
        ax.scatter([], [], c=DARK_BASE_COLOR if dark_mode else 'white', s=df['size'].mean() - (1.5 * df['size'].std()),
                   lw=0.5, edgecolor='white' if dark_mode else 'black', zorder=3,
                   label='Low')

    standard_ax_formating(ax=ax,
                          x_label=x_label,
                          y_label=y_label,
                          x_unit=x_unit,
                          y_unit=y_unit,
                          show_left_spine=show_left_spine,
                          dark_mode=dark_mode)

    if (x_annotation is not None and y_annotation is not None) or (custom_annotation is not None):
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()

        ax.scatter([xmin, xmin, xmax, xmax],
                   [ymin, ymax, ymin, ymax],
                   color=TEXT_COLOR if dark_mode else 'white',
                   zorder=1)

        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()

        if custom_annotation is not None:
            custom_annotation = [i.replace(' ', r"\ ") for i in custom_annotation]
            bot_left_text = r"$\bf{" + custom_annotation[0] + r"}$"
            top_left_text = r"$\bf{" + custom_annotation[1] + r"}$"
            top_right_text = r"$\bf{" + custom_annotation[2] + r"}$"
            bot_right_text = r"$\bf{" + custom_annotation[3] + r"}$"
        else:
            bot_left_text = r" $\bf{Low}$ " + y_annotation + '\n' + r" $\bf{Low}$ " + x_annotation
            top_left_text = r" $\bf{High}$ " + y_annotation + '\n' + r" $\bf{Low}$ " + x_annotation
            top_right_text = r"$\bf{High}$ " + y_annotation + '\n' + r"$\bf{High}$ " + x_annotation
            bot_right_text = r"$\bf{Low}$ " + y_annotation + '\n' + r"$\bf{High}$ " + x_annotation

        ax.text(xmin, ymin,
                bot_left_text,
                ha='left', va='bottom',
                color=text_color, fontsize=annotation_fontsize, fontweight='regular',
                path_effects=[pe.withStroke(linewidth=1.5,
                                            foreground=TEXT_COLOR if dark_mode else 'white',
                                            alpha=1)])
        ax.text(xmin, ymax,
                top_left_text,
                ha='left', va='top',
                color=text_color, fontsize=annotation_fontsize, fontweight='regular',
                path_effects=[pe.withStroke(linewidth=1.5,
                                            foreground=TEXT_COLOR if dark_mode else 'white',
                                            alpha=1)])
        ax.text(xmax, ymin,
                bot_right_text,
                ha='right', va='bottom',
                color=text_color, fontsize=annotation_fontsize, fontweight='regular',
                path_effects=[pe.withStroke(linewidth=1.5,
                                            foreground=TEXT_COLOR if dark_mode else 'white',
                                            alpha=1)])
        ax.text(xmax, ymax,
                top_right_text,
                ha='right', va='top',
                color=text_color, fontsize=annotation_fontsize,
                path_effects=[pe.withStroke(linewidth=1.5,
                                            foreground=TEXT_COLOR if dark_mode else 'white',
                                            alpha=1)])

    ax.grid(axis='both', color=text_color, alpha=0.2, lw=.5, linestyle='--')

    if plot_title is not None:
        ax.set_title(plot_title, weight='bold', color=text_color, pad=15)

    plt.tight_layout()
    plt.show()

    return fig, ax
