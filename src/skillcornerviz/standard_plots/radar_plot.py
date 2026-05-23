"""
Markos Bontozoglou
12/06/2024
Radar Plot
The plot_radar function is used to generate a radar plot based on the given data.
It accepts various parameters such as the DataFrame (df), then the list of metrics
to be displayed (metrics), the labels that are given to each metric (metric_labels),
and many stylistic features such as labels, highlighting, theme etc.
"""

from matplotlib import pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
from skillcornerviz.utils.constants import BASE_COLOR, PRIMARY_HIGHLIGHT_COLOR, FIVE_COLORS, \
    DARK_PRIMARY_HIGHLIGHT_COLOR, SECONDARY_HIGHLIGHT_COLOR
from skillcornerviz.utils.constants import TEXT_COLOR
from skillcornerviz.utils.skillcorner_utils import add_percentile_values
from skillcornerviz.standard_plots import formatting
from skillcornerviz.utils._fonts import load_shentox_fonts

def plot_radar(df, label, metrics, plot_title=None, metric_labels=None, simplify_labels=True,
               add_sample_info=False, positions=None, seasons=None, minutes=None, matches=None, competitions=None,
               theme='white', filter_relevant=False, relevant_threshold=0.3, excluded_metrics=None,
               color_groups=None, categorized=None, percentiles_precalculated=True, text_multiplier=1.45,
               rounding=1, suffix='', data_point_id='player_name', secondary_highlight_color=False):
    """
    Create a radar plot to visualize multivariate data using Matplotlib.

    Parameters:
    - df (DataFrame): The input data in the form of a DataFrame.
    - label: The label for the radar plot.
    - metrics: List of metrics to display on the radar plot.
    - plot_title: Title for the radar plot.
    - metric_labels: Labels for the metrics.
    - simplify_labels: If True, simplify metric labels.
    - add_sample_info: If True, add information about data sample.
    - positions, seasons, minutes, matches, competitions: Additional information for the sample.
    - theme: Color theme for the radar plot (e.g., 'white' or 'Dark').
    - filter_relevant: If True, filter out irrelevant metrics.
    - relevant_threshold: Threshold for relevance filtering.
    - excluded_metrics: Metrics to exclude from the plot.
    - color_groups: Custom color groups for metrics.
    - categorized: Categorization of metrics.
    - percentiles_precalculated: If True, use precalculated percentiles.
    - text_multiplier: Multiplier for text size.
    - rounding: Number of decimal places to round the values.
    - suffix: Suffix for values.
    - data_point_id: Identifier for data points.
    - secondary_highlight_color: If True, use a secondary highlight color.

    Returns:
    - fig (Figure): The Matplotlib figure.
    - ax (Axes): The Matplotlib axes.
    """

    load_shentox_fonts()
    plt.rcParams['font.family'] = 'Shentox'
    if theme == 'Dark':
        primary_color = TEXT_COLOR
        secondary_color = "white"
        bar_color = DARK_PRIMARY_HIGHLIGHT_COLOR
    else:
        primary_color = "white"
        secondary_color = TEXT_COLOR
        bar_color = PRIMARY_HIGHLIGHT_COLOR if secondary_highlight_color is False else SECONDARY_HIGHLIGHT_COLOR

    color_std_palette = FIVE_COLORS

    if excluded_metrics is None:
        excluded_metrics = []
    greyed_metrics = excluded_metrics.copy()

    if filter_relevant:
        for i in metrics:
            if len(df[df[i] >= 1]) / len(df) < relevant_threshold:
                greyed_metrics.append(i)

    if color_groups is None:
        radar_color = [BASE_COLOR if i in greyed_metrics else bar_color for i in metrics]
    else:
        radar_color = color_groups

    volume_metrics = [i for i in metrics]
    volume_pct_metrics = [i + '_pct' for i in metrics]

    if not percentiles_precalculated:
        add_percentile_values(df, metrics)

    volume_values = df.loc[df[data_point_id] == label][volume_metrics].astype(float).values.tolist()[0]
    volume_pct = df.loc[df[data_point_id] == label][volume_pct_metrics].astype(float).values.tolist()[0]

    width = 6.28319 / len(metrics)
    theta = np.linspace(0, (2 * np.pi), len(metrics), endpoint=False)
    theta = list(theta)
    theta.insert(0, theta.pop(-1))

    fig = plt.figure(figsize=(10, 10))
    ax = plt.subplot(projection='polar')

    fig.patch.set_facecolor(primary_color)
    ax.set_facecolor(primary_color)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.bar(theta, volume_pct, width=width, bottom=10,
           color=radar_color,
           edgecolor=None,
           lw=2,
           zorder=3,
           alpha=.95)

    ax.bar(theta, volume_pct, width=width, bottom=10, fill=False,
           edgecolor=primary_color,
           lw=2, zorder=5)

    if filter_relevant:
        for bar, name in zip(ax.containers[0], metrics):
            if name in greyed_metrics:
                bar.set_alpha(0.5 if theme == 'white' else 0.1)

    if categorized is not None:
        categories = categorized
        plot_categories = [categories[type] for type in metrics]
        unique_categories = list(set(plot_categories))

        for volume_bar, volume, category in zip(ax.containers[0], volume_values, plot_categories):
            for i in range(len(unique_categories)):
                if category == unique_categories[i]:
                    volume_bar.set_color(color_std_palette[i])

        for i in range(len(unique_categories)):
            ax.scatter([], [], c=color_std_palette[i], s=200,
                       lw=0.5, edgecolor=secondary_color, zorder=3,
                       label=unique_categories[i])

        ax.legend(facecolor=primary_color,
                  edgecolor=primary_color,
                  framealpha=0.6,
                  labelcolor=secondary_color,
                  fontsize=8 * text_multiplier,
                  loc='upper center',
                  bbox_to_anchor=(0.5, 1.06),
                  ncol=3)

    ax.set_ylim(0, 120)
    ax.set_yticks([35, 60, 85, 110])
    ax.set_yticklabels(['', '', '', ''])

    pos = ax.get_rlabel_position()
    ax.set_rlabel_position(pos + 106.5)

    y_pos = [35, 60, 85]
    labels = ['25', '50', '75']
    y_axis_pos = min(theta, key=lambda x: abs(x - 1.8))

    for y, l in zip(y_pos, labels):
        ax.text(y_axis_pos + (width * .5),
                y,
                l,
                ha='center', va='center',
                size=7 * text_multiplier,
                fontweight='bold',
                color=secondary_color,
                zorder=8,
                path_effects=[pe.withStroke(linewidth=3,
                                            foreground=primary_color,
                                            alpha=1)])

    ax.text(y_axis_pos + (width * .5),
            110,
            '100th\nPercentile',
            ha='left', va='center',
            size=7 * text_multiplier,
            color=secondary_color,
            fontweight='bold',
            zorder=8,
            path_effects=[pe.withStroke(linewidth=3,
                                        foreground=primary_color,
                                        alpha=1)])

    ax.set_xticks(theta)

    if metric_labels is not None:
        if not simplify_labels:
            xtick_labels = [metric_labels[i] for i in metrics]
            greyed_metrics_labels = [metric_labels[i] for i in greyed_metrics]
        else:
            xtick_labels = [formatting.simplify_label(metric_labels[i]) for i in metrics]
            greyed_metrics_labels = [formatting.simplify_label(metric_labels[i]) for i in greyed_metrics]
    else:
        xtick_labels = [formatting.prep_label_for_radar(i) for i in metrics]
        greyed_metrics_labels = [formatting.prep_label_for_radar(i) for i in greyed_metrics]

    ax.set_xticklabels(xtick_labels,
                       size=8 * text_multiplier,
                       color=secondary_color)

    labels = []

    for tick_label, run_type, angle, value_pct in zip(ax.get_xticklabels(), metrics, theta, volume_pct):
        x, y = tick_label.get_position()
        lab = ax.text(x, y,
                      tick_label.get_text(),
                      transform=tick_label.get_transform(),
                      ha=tick_label.get_ha(),
                      va=tick_label.get_va())

        if (90 >= (angle * 180 / np.pi) >= 0) | (360 >= (angle * 180 / np.pi) >= 270):
            lab.set_rotation(0 - (angle * 180 / np.pi))
        else:
            lab.set_rotation(180 - (angle * 180 / np.pi))

        lab.set_y(0.08)
        lab.set_fontproperties({'weight': 'bold', 'size': 10 * text_multiplier})
        lab.set_horizontalalignment('center')

        if tick_label.get_text() in greyed_metrics_labels:
            lab.set_color(BASE_COLOR)
        else:
            lab.set_color(bar_color)

        labels.append(lab)

    ax.set_xticklabels([])

    for volume_value, theta, metric in zip(volume_values, theta, volume_metrics):
        volume_text = ax.text(theta,
                              105,
                              str(round(volume_value, rounding)) + suffix,
                              ha='center', va='center',
                              fontweight='bold',
                              color=BASE_COLOR if metric in greyed_metrics else secondary_color,
                              fontsize=8 * text_multiplier,
                              zorder=5,
                              path_effects=[pe.withStroke(linewidth=3,
                                                          foreground=primary_color,
                                                          alpha=1)])

        if (90 >= (theta * 180 / np.pi) >= 0) | (360 >= (theta * 180 / np.pi) >= 270):
            volume_text.set_rotation(0 - (theta * 180 / np.pi))
        else:
            volume_text.set_rotation(180 - (theta * 180 / np.pi))

    ax.xaxis.grid(False)
    ax.yaxis.grid(color=secondary_color, linestyle='--', linewidth=1)
    ax.spines["start"].set_color("none")
    ax.spines["polar"].set_color("none")

    if add_sample_info:
        CREDIT_1 = "Positions: " + positions
        CREDIT_2 = "Seasons: " + seasons
        CREDIT_3 = "Competitions: " + competitions
        CREDIT_4 = "Minimum of " + str(matches) + " matches of at least " + str(minutes) + " minutes"

        ax.text(3.9, 180,
                f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}\n{CREDIT_4}",
                size=8 * text_multiplier,
                color=secondary_color,
                ha="left")

    ax.text(0,
            138,
            label if plot_title is None else plot_title,
            size=14 * text_multiplier,
            color=secondary_color,
            fontweight='bold',
            ha='center')

    if filter_relevant:
        ax.scatter([], [], c=bar_color, s=200,
                   lw=0.5, edgecolor=primary_color, zorder=3,
                   label='Position Relevant')
        ax.scatter([], [], c=BASE_COLOR, s=200, alpha=0.5 if theme == 'white' else 0.1,
                   lw=0.5, edgecolor=primary_color, zorder=3,
                   label='Non-relevant')

        ax.legend(facecolor=primary_color,
                  edgecolor=primary_color,
                  framealpha=0.6,
                  labelcolor=secondary_color,
                  fontsize=8 * text_multiplier,
                  loc='upper center',
                  bbox_to_anchor=(0.5, 1.06),
                  ncol=3)

    plt.tight_layout()
    plt.show()

    return fig, ax
