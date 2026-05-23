"""
Liam Michael Bailey
Helper functions for SkillCorner physical data.
"""
import pandas as pd


def add_p90(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Add P90 values for a column.

    Parameters:
        df (DataFrame): The DataFrame containing the original metrics.
        column_name (str): The column name which the P90 values will be generated for.

    Returns:
        df (DataFrame): The DataFrame with the P90 column added.
    """
    df[column_name + '_per_90'] = df[column_name + '_full_all'] / (df['minutes_full_all'] / 90)
    df[column_name + '_per_90'] = df[column_name + '_per_90'].round(1)
    return df


def add_p60_bip(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Add BIP per 60 minutes values for a column.

    Parameters:
        df (DataFrame): The DataFrame containing the original metrics.
        column (str): The column which the BIP per 60 value will be generated for.

    Returns:
        df (DataFrame): The DataFrame with the per-60-BIP column added.
    """
    df[column + '_per_60_bip'] = ((df[column + '_full_tip'] + df[column + '_full_otip']) /
                                  (df['minutes_full_tip'] + df['minutes_full_otip'])) * 60
    return df


def add_p30_tip(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Add TIP per 30 minutes values for a column.

    Parameters:
        df (DataFrame): The DataFrame containing the original metrics.
        column (str): The column which the TIP per 30 value will be generated for.

    Returns:
        df (DataFrame): The DataFrame with the per-30-TIP column added.
    """
    df[column + '_per_30_tip'] = (df[column + '_full_tip'] / df['minutes_full_tip']) * 30
    return df


def add_p30_otip(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Add OTIP per 30 minutes values for a column.

    Parameters:
        df (DataFrame): The DataFrame containing the original metrics.
        column (str): The column which the OTIP per 30 value will be generated for.

    Returns:
        df (DataFrame): The DataFrame with the per-30-OTIP column added.
    """
    df[column + '_per_30_otip'] = (df[column + '_full_otip'] / df['minutes_full_otip']) * 30
    return df


def add_standard_metrics(df: pd.DataFrame) -> list:
    """
    Add standard metrics to the DataFrame.

    Calculates and adds per-90, per-60 BIP, per-30 TIP, per-30 OTIP values, high-intensity
    metrics, and several other performance metrics normalized per minute and per sprint.

    Parameters:
        df (DataFrame): The DataFrame containing the original metrics.

    Returns:
        list: A list of the names of the newly added or modified metrics.
    """

    df['minutes_full_bip'] = df['minutes_full_tip'] + df['minutes_full_otip']

    metrics = []
    metrics.append('minutes_full_all')
    metrics.append('minutes_full_bip')
    metrics.append('minutes_full_tip')
    metrics.append('minutes_full_otip')

    df['accel_count_full_all'] = df['medaccel_count_full_all'] + df['highaccel_count_full_all']
    df['accel_count_full_tip'] = df['medaccel_count_full_tip'] + df['highaccel_count_full_tip']
    df['accel_count_full_otip'] = df['medaccel_count_full_otip'] + df['highaccel_count_full_otip']

    df['decel_count_full_all'] = df['meddecel_count_full_all'] + df['highdecel_count_full_all']
    df['decel_count_full_tip'] = df['meddecel_count_full_tip'] + df['highdecel_count_full_tip']
    df['decel_count_full_otip'] = df['meddecel_count_full_otip'] + df['highdecel_count_full_otip']

    raw_metrics = ['total_distance',
                   'running_distance',
                   'hsr_distance',
                   'sprint_distance',
                   'hi_distance',
                   'hsr_count',
                   'sprint_count',
                   'hi_count',
                   'accel_count',
                   'highaccel_count',
                   'medaccel_count',
                   'decel_count',
                   'highdecel_count',
                   'meddecel_count']

    for m in raw_metrics:
        add_p90(df, m)
        add_p60_bip(df, m)
        add_p30_tip(df, m)
        add_p30_otip(df, m)

        df[m + '_full_bip'] = df[m + '_full_tip'] + df[m + '_full_otip']

        metrics.append(m)
        metrics.append(m + '_per_90')
        metrics.append(m + '_full_bip')
        metrics.append(m + '_per_60_bip')
        metrics.append(m + '_full_tip')
        metrics.append(m + '_per_30_tip')
        metrics.append(m + '_full_otip')
        metrics.append(m + '_per_30_otip')

    df['meters_per_minute'] = df['total_distance_full_all'] / df['minutes_full_all']
    df['meters_per_minute_bip'] = df['total_distance_full_bip'] / df['minutes_full_bip']
    df['meters_per_minute_tip'] = df['total_distance_full_tip'] / df['minutes_full_tip']
    df['meters_per_minute_otip'] = df['total_distance_full_otip'] / df['minutes_full_otip']
    metrics.append('meters_per_minute')
    metrics.append('meters_per_minute_bip')
    metrics.append('meters_per_minute_tip')
    metrics.append('meters_per_minute_otip')

    df['hi_meters_per_minute'] = df['hi_distance_full_all'] / df['minutes_full_all']
    df['hi_meters_per_minute_bip'] = df['hi_distance_full_bip'] / df['minutes_full_bip']
    df['hi_meters_per_minute_tip'] = df['hi_distance_full_tip'] / df['minutes_full_tip']
    df['hi_meters_per_minute_otip'] = df['hi_distance_full_otip'] / df['minutes_full_otip']
    metrics.append('hi_meters_per_minute')
    metrics.append('hi_meters_per_minute_bip')
    metrics.append('hi_meters_per_minute_tip')
    metrics.append('hi_meters_per_minute_otip')

    df['distance_per_sprint'] = df['sprint_distance_full_all'] / df['sprint_count_full_all']
    df['distance_per_sprint_bip'] = df['sprint_distance_full_bip'] / df['sprint_count_full_bip']
    df['distance_per_sprint_tip'] = df['sprint_distance_full_tip'] / df['sprint_count_full_tip']
    df['distance_per_sprint_otip'] = df['sprint_distance_full_otip'] / df['sprint_count_full_otip']
    metrics.append('distance_per_sprint')
    metrics.append('distance_per_sprint_bip')
    metrics.append('distance_per_sprint_tip')
    metrics.append('distance_per_sprint_otip')

    metrics.append('psv99')

    df['minutes_played_per_match'] = df['minutes_full_all']

    return metrics
