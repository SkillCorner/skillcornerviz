"""
Liam Bailey
12/06/2024
Summary Table
The plot_summary_table function is used to generate a summary table based on the given data.
It accepts various parameters such as the DataFrame (df) containing the metric data,
the names that are given to each column (metric_col_names), the size of the summary table (fig_size),
the metadata columns to include in the summary table (meta), and the format which the summary table will
be presented in (mode).
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from skillcornerviz.utils.constants import GREEN_TO_RED_SCALE, DARK_GREEN_TO_RED_SCALE, \
    DARK_PRIMARY_HIGHLIGHT_COLOR
from skillcornerviz.utils.constants import TEXT_COLOR, DARK_BASE_COLOR
from skillcornerviz.utils import skillcorner_utils as skcu
from skillcornerviz.utils._fonts import load_shentox_fonts
import pandas as pd

def _ordinal_suffix(n: int) -> str:
    """Return the correct ordinal suffix for n (handles 11th, 12th, 13th edge cases)."""
    if 11 <= (n % 100) <= 13:
        return 'th'
    return {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')


def plot_summary_table(df,
                       metrics,
                       metric_col_names,
                       highlight_group,
                       meta=None,
                       mode='values+rank',
                       percentiles_mode=False,
                       invert_percentile_metrics=None,
                       fontsize=None,
                       dividing_lines=None,
                       metric_col_space=None,
                       data_point_id='player_name',
                       data_point_label='player_name',
                       column_order=None,
                       split_column_names=True,
                       dark_mode=False,
                       rotate_column_names=False,
                       split_metric_names=True,
                       metrics_in_caps=False,
                       figsize=(10, 4)):
    """
    Plot a summary table with a dimension as a column.

    Parameters:
    - df (DataFrame): The data to be visualized in the table.
    - metrics (list): List of metric names to display.
    - metric_col_names (list): List of column names for metrics.
    - highlight_group (list): List of names to include in the table.
    - figsize (tuple): Figure size (width, height).
    - meta (list): List of metadata columns.
    - mode (str): Display mode ('values+rank', 'rank', 'values').
    - percentiles_mode (bool): Whether to use percentiles for ranking.
    - fontsize (float): Font size for the table.
    - dividing_lines (list): Positions to add dividing lines.
    - metric_col_space (float): Space between metric columns.
    - data_point_id (str): The data point identifier column.
    - data_point_label (str): The label for data points.
    - column_order (list): Custom order of data_point_id columns.
    - split_column_names (bool): Split long column names.
    - dark_mode (bool): Enable dark mode (True) or light mode (False).
    - rotate_column_names (bool): Rotate column names if True.
    - split_metric_names (bool): Split long metric names.

    Returns:
    - fig (Figure): The Matplotlib Figure object.
    - ax (Axes): The Matplotlib Axes object.
    """

    load_shentox_fonts()
    plt.rcParams['font.family'] = 'Shentox'
    if dividing_lines is None:
        dividing_lines = []
    if meta is None:
        meta = [data_point_id]
    if invert_percentile_metrics is None:
        invert_percentile_metrics = []

    if fontsize is None:
        if len(highlight_group) <= 9:
            fontsize = 7
        elif len(highlight_group) <= 12:
            fontsize = 6.5
        else:
            fontsize = 6

    if metric_col_space is None:
        if len(highlight_group) <= 4:
            metric_col_space = 1.5
        elif len(highlight_group) <= 7:
            metric_col_space = 2.5
        elif len(highlight_group) <= 14:
            metric_col_space = 3
        else:
            metric_col_space = 3.5

    if split_metric_names:
        metric_col_names = [skcu.split_string_with_new_line(s) if len(s) > 25 else s for s in metric_col_names]

    column_name_fontsize = fontsize * 1

    plot_df = df.copy()

    for m in metrics:
        plot_df[m] = plot_df[m].round(2)

    if not percentiles_mode:
        pct_bins = [0, 10, 20, 80, 90]
        bin_names = ['Very Low', 'Low', 'Average', 'High', 'Very High']
        for bin, name in zip(pct_bins, bin_names):
            for m in metrics:
                if m in invert_percentile_metrics:
                    plot_df.loc[
                        (plot_df[m].rank(pct=True, na_option='keep', ascending=False) * 100).round(2) >= int(bin),
                        m + '_pct'] = name
                else:
                    plot_df.loc[(plot_df[m].rank(pct=True, na_option='keep') * 100).round(2) >= int(bin),
                                m + '_pct'] = name
    else:
        for m in metrics:
            if m in invert_percentile_metrics:
                plot_df[m + '_pct'] = (plot_df[m].rank(pct=True, na_option='keep', ascending=False) * 100).round(2)
            else:
                plot_df[m + '_pct'] = (plot_df[m].rank(pct=True, na_option='keep', ascending=True) * 100).round(2)

    plot_df = plot_df[plot_df[data_point_id].isin(highlight_group)]

    if column_order is None:
        plot_df[data_point_id] = pd.Categorical(plot_df[data_point_id], categories=highlight_group, ordered=True)
        plot_df = plot_df.sort_values(data_point_id)
        columns = ['index'] + highlight_group
    else:
        plot_df[data_point_id] = pd.Categorical(plot_df[data_point_id], categories=column_order, ordered=True)
        plot_df = plot_df.sort_values(data_point_id)
        columns = ['index'] + column_order

    highlight_group = list(plot_df[data_point_id])
    highlight_labels = list(plot_df[data_point_label])

    text_color = 'white' if dark_mode else TEXT_COLOR
    facecolor = TEXT_COLOR if dark_mode else 'white'

    red_highlight = DARK_GREEN_TO_RED_SCALE[1] if dark_mode else GREEN_TO_RED_SCALE[0]
    green_highlight = DARK_GREEN_TO_RED_SCALE[3] if dark_mode else GREEN_TO_RED_SCALE[4]

    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(facecolor)
    ax.set_facecolor(facecolor)

    for i in metrics:
        plot_df[i] = plot_df[i].astype(str) + ' ' + plot_df[i + '_pct'].astype(str)
    plot_df = plot_df[meta + metrics]
    meta_names = [i.replace('_', ' ').capitalize() for i in meta]
    plot_df.columns = meta_names + metric_col_names

    plot_df = plot_df.set_index(data_point_id.replace('_', ' ').capitalize()).T.reset_index()
    plot_df = plot_df.iloc[::-1].reset_index(drop=True)

    if split_column_names:
        column_names = [''] + [skcu.split_string_with_new_line(i) if i[1] != '.' else i for i in highlight_labels]
    else:
        column_names = [''] + highlight_labels

    positions = [0.0] + [(i + metric_col_space) * 2 for i in range(0, len(highlight_group))]
    nrows = plot_df.shape[0]

    ax.set_xlim(0, max(positions) + 1)
    ax.set_ylim(0, nrows + 1)

    for i in range(nrows):
        for j, column in enumerate(columns):
            if j == 0:
                ha = 'left'
            else:
                ha = 'center'

            if j != 0:
                col_name = plot_df['index'].iloc[i].lower().replace('\n', ' ')
                if 'ratio ' in ' ' + col_name + ' ' or \
                        ' percentage ' in ' ' + col_name + ' ' or \
                        ' % ' in ' ' + col_name + ' ' or \
                        ' ratio' in ' ' + col_name:
                    appendix = ' %'
                elif ' velocity ' in ' ' + col_name + ' ' or \
                        ' psv-99 ' in ' ' + col_name + ' ':
                    appendix = ' km/h'
                elif ' distance ' in ' ' + col_name + ' ':
                    appendix = 'm'
                elif 'meters per minute' in ' ' + col_name + ' ':
                    appendix = 'm'
                elif ' threat ' in ' ' + col_name + ' ':
                    appendix = ''
                elif ' passes ' in ' ' + col_name + ' ' or \
                        ' pass ' in ' ' + col_name + ' ':
                    appendix = ' Passes'
                elif ' runs ' in ' ' + col_name + ' ':
                    appendix = ' Runs'
                else:
                    appendix = ''
            else:
                appendix = ''

            rank_label = ''
            weight = 'normal'

            if column == 'index':
                text_label = f'{plot_df[column].iloc[i]}'
                text_label = text_label.upper() if metrics_in_caps else text_label
                weight = 'bold'
                annotation_text = text_label + appendix
            elif plot_df['index'][i] in meta_names:
                text_label = f'{plot_df[column].iloc[i]}'
                if len(text_label.split(' ')) > 1:
                    text_label = skcu.split_string_with_new_line(text_label)
                weight = 'normal'
                annotation_text = text_label
            else:
                text_label = f'{plot_df[column].iloc[i]}'
                split_text_label = text_label.split(" ", 1)
                text_label = split_text_label[0]
                rank_label = split_text_label[1].split('.')[0]
                weight = 'normal'
                if mode == 'values+rank':
                    annotation_text = text_label + appendix + '\n' + rank_label
                elif mode == 'rank':
                    annotation_text = rank_label
                elif mode == 'values':
                    annotation_text = text_label + appendix
                else:
                    annotation_text = ''

            if 'nan' not in str(plot_df[column].iloc[i]):
                if not percentiles_mode or column == 'index':
                    if 'High' in rank_label:
                        colour = green_highlight
                        weight = 'bold'
                    elif 'Low' in rank_label:
                        colour = red_highlight
                        weight = 'bold'
                    else:
                        colour = text_color
                elif percentiles_mode:
                    if rank_label != '':
                        if float(rank_label) > 79:
                            colour = green_highlight
                            weight = 'bold'
                            bar_color = colour
                        elif float(rank_label) < 21:
                            colour = red_highlight
                            weight = 'bold'
                            bar_color = colour
                        else:
                            colour = text_color
                            bar_color = DARK_BASE_COLOR
                    else:
                        colour = text_color
                        bar_color = DARK_BASE_COLOR

                    if mode in ('values+rank', 'rank'):
                        if rank_label != '':
                            annotation_text = annotation_text + _ordinal_suffix(int(float(rank_label)))

                    if column != 'index':
                        if rank_label != '':
                            ax.add_patch(
                                Rectangle((positions[j] - 1, i), 2 * float(rank_label) / 100, 1, fc=bar_color,
                                          edgecolor=DARK_BASE_COLOR if dark_mode else 'black',
                                          alpha=0.5 if dark_mode else 0.1))
                else:
                    colour = TEXT_COLOR

                ax.annotate(
                    xy=(positions[j], i + .5),
                    text=annotation_text,
                    ha=ha,
                    va='center',
                    weight=weight,
                    color=colour,
                    fontsize=fontsize,
                    zorder=10
                )
            else:
                ax.annotate(
                    xy=(positions[j], i + .5),
                    text='No Data',
                    ha=ha,
                    va='center',
                    weight=weight,
                    color=TEXT_COLOR,
                    fontsize=fontsize,
                    zorder=10)

                if percentiles_mode:
                    ax.add_patch(
                        Rectangle((positions[j] - 1, i), 2 * float(100) / 100, 1, fc='white',
                                  edgecolor=DARK_BASE_COLOR if dark_mode else 'black',
                                  alpha=0.5 if dark_mode else 0.1))

    text_objects = []
    for index, c in enumerate(column_names):
        if index == 0:
            ha = 'left'
        else:
            ha = 'center'

        rotation = 30 if rotate_column_names else 0
        text_objects.append(ax.annotate(
            xy=(positions[index], nrows + .25),
            text=column_names[index],
            ha=ha,
            va='bottom',
            weight='bold',
            color=text_color,
            fontsize=column_name_fontsize,
            rotation=rotation))

    overlapping_col_name = False
    for i in range(len(text_objects)):
        if i != len(text_objects) - 1:
            bbox = text_objects[i].get_window_extent()
            x_end, _ = ax.transData.inverted().transform((bbox.x1, bbox.y1))
            next_bbox = text_objects[i + 1].get_window_extent()
            x_start, _ = ax.transData.inverted().transform((next_bbox.x0, next_bbox.y0))

            if x_end >= x_start:
                overlapping_col_name = True

    if overlapping_col_name:
        for text_object in text_objects:
            text_object.set_rotation(30)
            text_object.set_ha('left')

    ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [nrows, nrows], lw=1.5,
            color=DARK_PRIMARY_HIGHLIGHT_COLOR if dark_mode else text_color, marker='', zorder=4)
    ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [0, 0], lw=1.5,
            color=DARK_PRIMARY_HIGHLIGHT_COLOR if dark_mode else text_color, marker='', zorder=4)

    for i in dividing_lines:
        ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [i, i], lw=1.5, color=DARK_BASE_COLOR, marker='', zorder=4)

    for x in range(1, nrows):
        ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [x, x], lw=.5, color=DARK_BASE_COLOR, alpha=0.5, ls='-',
                zorder=3, marker='')

    ax.set_axis_off()
    plt.tight_layout()
    plt.show()

    return fig, ax
