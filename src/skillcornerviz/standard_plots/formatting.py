"""
Michael Nanopoulos
Simple function that takes an ax, x , and y
"""

from matplotlib.ticker import EngFormatter
from skillcornerviz.utils.constants import TEXT_COLOR


def standard_ax_formating(ax,
                          x_label,
                          y_label,
                          x_unit=None,
                          y_unit=None,
                          labelsize=7,
                          fontsize=7,
                          show_legend=True,
                          legend_fontsize=6,
                          show_left_spine=False,
                          dark_mode=False):
    """
    Format the appearance of a matplotlib axis in a standardized way.

    Args:
        ax (matplotlib.axis.Axis): The axis object to be formatted.
        x_label (str): The label for the x-axis.
        y_label (str): The label for the y-axis.
        x_unit (str, optional): The unit for the values on the x-axis.
        y_unit (str, optional): The unit for the values on the y-axis.
        labelsize (int, optional): The font size of the axis labels.
        fontsize (int, optional): The font size of the tick labels on the axes.
        show_legend (bool, optional): Whether to show the legend on the plot.
        legend_fontsize (int, optional): The font size of the legend labels.
        show_left_spine (bool, optional): Whether to show the left spine of the plot.
        dark_mode (bool, optional): Whether to use dark mode colors.
    """

    color = 'white' if dark_mode else TEXT_COLOR
    ax.set_xlabel(x_label, fontweight='bold', fontsize=labelsize, color=color)
    ax.set_ylabel(y_label, fontweight='bold', fontsize=labelsize, color=color)

    ax.spines['bottom'].set_color(color)
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    if show_left_spine:
        ax.spines['left'].set_color(color)

    ax.tick_params(axis='x', colors=color, labelsize=fontsize)
    ax.tick_params(axis='y', colors=color, labelsize=fontsize, length=0)

    if show_legend:
        ax.legend(facecolor=TEXT_COLOR if dark_mode else 'white',
                  edgecolor=TEXT_COLOR if dark_mode else 'white',
                  framealpha=0.6,
                  labelcolor=color,
                  fontsize=legend_fontsize,
                  loc='center left',
                  bbox_to_anchor=(1.01, 0.5))

    if x_unit is not None:
        formatter0 = EngFormatter(unit=x_unit)
        ax.xaxis.set_major_formatter(formatter0)

    if y_unit is not None:
        formatter1 = EngFormatter(unit=y_unit)
        ax.yaxis.set_major_formatter(formatter1)


def prep_label_for_radar(x):
    label = x.lower().replace('count_', '').replace('_p90', '').replace(' P90', ''). \
        replace('_per_30_tip', ' ').replace('runs', '').replace('opportunities_to_pass_to_', '').replace('_', ' '). \
        strip().upper()
    return label


def simplify_label(x):
    label = x.lower().replace('carrera a ', '').replace('carrera de ', '').replace('carrera para ', '').replace(
        'carrera', '').replace(' por ', '\n'). \
        replace('course pour ', '').replace('course de ', '').replace('course', ''). \
        replace('être à la', '').replace('dans la ', '').replace('dans le ', ''). \
        replace('corsa ', ''). \
        replace('runs', ''). \
        strip().upper()
    return label
