import pandas as pd
from datetime import datetime


def merge_sc_dataframes(off_ball_runs_df=pd.DataFrame(),
                        passes_df=pd.DataFrame(),
                        pressure_df=pd.DataFrame(),
                        physical_df=pd.DataFrame(),
                        group_by_str='player,team,competition,season,group,position'):
    """
    Merges SkillCorner dataframes based on the specified grouping condition.

    Args:
        off_ball_runs_df (pandas.DataFrame, optional): Dataframe containing off-ball runs data.
        passes_df (pandas.DataFrame, optional): Dataframe containing passes data.
        pressure_df (pandas.DataFrame, optional): Dataframe containing pressure data.
        physical_df (pandas.DataFrame, optional): Dataframe containing physical data.
        group_by_str (str, optional): Grouping condition.

    Returns:
        merged_df (pandas.DataFrame): Merged dataframe.
    """

    group_keys = group_by_str.split(',')
    merge_keys = []
    for key in group_keys:
        if key == 'player':
            merge_keys.append('player_name')
            merge_keys.append('player_id')
            merge_keys.append('player_birthdate')
        elif key != 'group' and key != 'position':
            merge_keys.append(key + '_id')
            if key != 'competition':
                merge_keys.append(key + '_name')
        else:
            merge_keys.append(key)

    suffixes = ['_runs', '_passes', '_pressures', '_physical']

    df_list = [off_ball_runs_df, passes_df, pressure_df, physical_df]
    df_list = [df for df in df_list if not df.empty]

    if len(df_list) == 0:
        return pd.DataFrame()
    if len(df_list) == 1:
        return df_list[0]

    merged_df = pd.merge(df_list[0], df_list[1], on=merge_keys, suffixes=(suffixes[0], suffixes[1]))
    for i in range(2, len(df_list)):
        merged_df = pd.merge(merged_df, df_list[i], on=merge_keys, suffixes=('', suffixes[i]))

    return merged_df


def get_player_age(df):
    """
    Calculate and add player ages based on birthdates to the DataFrame.

    Parameters:
    - df (DataFrame): DataFrame containing player information with 'player_birthdate' column.

    Returns:
    - df (DataFrame): The modified DataFrame with an 'age' column added.
    """
    today = datetime.today()
    df['age'] = today - pd.to_datetime(df['player_birthdate'])
    df['age'] = df['age'].dt.days
    df['age'] = (df['age'].astype(int) / 365)
    return df


def save_fig(name, fig, transparent=True):
    """
    Save a Matplotlib figure as a PNG image.

    Parameters:
    - name (str): The filename to save the image.
    - fig (Figure): The Matplotlib Figure object to save.
    - transparent (bool): If True, the image will have a transparent background.
    """
    fig.savefig(name,
                format='png',
                transparent=transparent,
                dpi=300)


def add_percentile_values(df, metrics):
    """
    Add percentile values for specified metrics to the DataFrame.

    Parameters:
    - df (DataFrame): The DataFrame to add percentile values to.
    - metrics (list): List of metric names to compute percentiles.

    Returns:
    - df (DataFrame): The modified DataFrame with percentile columns added.
    """
    for metric in metrics:
        df[metric + '_pct'] = (df[metric].rank(pct=True, na_option='keep') * 100).round()
    return df


def add_data_point_id(df, split_by_selection):
    """
    Add a unique data point identifier based on grouping conditions to the DataFrame.

    Parameters:
    - df (DataFrame): The DataFrame to add data point identifiers to.
    - split_by_selection (list): List of column names used for grouping.

    Returns:
    - df (DataFrame): The modified DataFrame with a 'data_point_id' column added.
    """
    df['data_point_id'] = df[split_by_selection[0]]
    if len(split_by_selection) > 1:
        for s in split_by_selection:
            if s != split_by_selection[0]:
                df['data_point_id'] = df['data_point_id'] + ' | ' + df[s]
    return df


def split_string_with_new_line(string):
    """
    Split a long string into two lines in the middle.

    Parameters:
    - string (str): The input string to split.

    Returns:
    - new_string (str): The modified string with a line break in the middle.
    """
    whitespaces = [i for i, ltr in enumerate(string) if ltr == ' ']
    if len(whitespaces) > 0:
        string_middle = len(string) / 2
        middle_white_space = min(whitespaces, key=lambda x: abs(x - string_middle))
        new_string = ''.join((string[:middle_white_space], '\n', string[middle_white_space + 1:]))
        return new_string
    else:
        return string
