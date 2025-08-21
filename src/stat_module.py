import yaml
import pandas as pd
from typing import Any, Dict, List, Optional
import re


def load_training_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Load training data from a YAML file.

    Parameters
    ----------
    file_path : str
        Path to the YAML file.

    Returns
    -------
    list of dict
        List of weekly data dictionaries.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    return data['data']


def extract_activity_stats(week: Dict[str, Any], activity: str) -> Dict[str, float]:
    """
    Extract summed statistics for a specific activity in a given week.

    Parameters
    ----------
    week : dict
        One week's data.
    activity : str
        The activity/event key to extract.

    Returns
    -------
    dict
        Summed time, distance, elevation, load for the activity.
    """
    sessions = week.get(activity, [])
    total = {'time_min': 0, 'distance_km': 0, 'elevation_m': 0, 'load': 0}

    for s in sessions:
        total['time_min'] += s.get('time_min', 0)
        total['distance_km'] += s.get('distance_km', 0)
        total['elevation_m'] += s.get('elevation_m', 0)
        total['load'] += s.get('load', 0)

    return total


def collect_all_stats(weeks: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Compile weekly and per-activity statistics into a pandas DataFrame.

    Parameters
    ----------
    weeks : list of dict
        Each week's activity dictionary.

    Returns
    -------
    pd.DataFrame
        A dataframe with stats by week and activity.
    """
    # List all found activity types
    activities = set()

    for w in weeks:
        activities.update(k for k in w if k not in ['week_first_day', 'week_comment'])
    activities = sorted(list(activities))

    records = []

    for week in weeks:
        week_data = {'week_first_day': week.get('week_first_day')}
        total_time = 0
        total_distance = 0
        total_elevation = 0
        total_load = 0
        # For each activity, sum stats for this week

        for act in activities:
            stats = extract_activity_stats(week, act)
            week_data[f'{act}_time_min'] = stats['time_min']
            week_data[f'{act}_distance_km'] = stats['distance_km']
            week_data[f'{act}_elevation_m'] = stats['elevation_m']
            week_data[f'{act}_load'] = stats['load']
            total_time += stats['time_min']
            total_distance += stats['distance_km']
            total_elevation += stats['elevation_m']
            total_load += stats['load']
        # Weekly totals
        week_data['week_total_time_min'] = total_time
        week_data['week_total_distance_km'] = total_distance
        week_data['week_total_elevation_m'] = total_elevation
        week_data['week_total_load'] = total_load
        week_data['week_comment'] = week.get('week_comment', "")
        records.append(week_data)
    df = pd.DataFrame(records)

    return df


def per_sport_stats(df: pd.DataFrame, with_total: bool = False) -> pd.DataFrame:
    """
    Compute global statistics (sum) per activity type on all weeks,
    excluding any 'total_*' columns, and optionally adds a TOTAL row.

    Parameters
    ----------
    df : pd.DataFrame
        Output of collect_all_stats().
    with_total : bool, optional
        If True, adds a TOTAL row at the end (default: False)

    Returns
    -------
    pd.DataFrame
        A summary table by type of sport, and optionally a global total.
    """
    # Collect all activity names from <activity>_time_min columns, except if they begin with "week_total_"
    pattern = re.compile(r'^(.*?)_time_min$')
    activity_names = set()

    for col in df.columns:
        if not col.startswith("week_total_"):
            match = pattern.match(col)

            if match:
                activity_names.add(match.group(1))

    summary = []

    for activity in sorted(activity_names):
        rec = {'activity': activity}
        # For each stat type

        for stat in ['time_min', 'distance_km', 'elevation_m', 'load']:
            colname = f"{activity}_{stat}"
            rec[stat] = df[colname].sum() if colname in df else 0
        summary.append(rec)

    res = pd.DataFrame(summary)

    if with_total:
        total_row = {
            'activity': 'TOTAL',
            'time_min': res['time_min'].sum(),
            'distance_km': res['distance_km'].sum(),
            'elevation_m': res['elevation_m'].sum(),
            'load': res['load'].sum()
        }
        res = pd.concat([res, pd.DataFrame([total_row])], ignore_index=True)

    return res


def display_stats_tables(yaml_path: str):
    """
    Top-level function: Load YAML, compute stats,
    and print weekly & per-type sport tables.

    Parameters
    ----------
    yaml_path : str
        Path to the YAML file.
    """
    # Step 1: Load data
    weeks = load_training_data(yaml_path)
    # Step 2: Weekly and activity stats dataframe
    df = collect_all_stats(weeks)
    print("==== STATISTIQUES HEBDOMADAIRES ====")
    print(df.fillna(0).to_string(index=False))
    # Step 3: Global stats by sport type
    print("==== STATISTIQUES GLOBALES PAR TYPE DE SPORT ====")
    print(per_sport_stats(df, with_total=True).to_string(index=False))

# Pour l'utiliser :
# display_stats_tables("data/template.yml")
