import pandas as pd
from config import STATE_CODES


def filter_by_date(data, start_date, end_date):
    """Filter map data based on selected date range."""
    return data[
        (data['DATETIME'] >= pd.to_datetime(start_date)) &
        (data['DATETIME'] <= pd.to_datetime(end_date))
    ]


def filter_by_states(data, selected_states):
    """Filter map data based on selected states."""
    reverse_state_codes = {v: k for k, v in STATE_CODES.items()}
    selected_state_codes = [reverse_state_codes[state]
                            for state, selected in selected_states.items() if selected]
    return data[data['STATE'].isin(selected_state_codes)]


def filter_by_region(data, region):
    """
    Split data into Alaska and Continental USA regions.
    Returns the appropriate dataset based on selected region.
    """
    if region == "Alaska":
        return data[(data['Latitude'] > 50) & (data['Longitude'] < -130)]
    else:  # Continental USA
        return data[~((data['Latitude'] > 50) & (data['Longitude'] < -130))]
