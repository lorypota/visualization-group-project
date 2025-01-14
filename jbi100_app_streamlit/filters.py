import pandas as pd
from constants import STATE_CODES, TYPE_DESCRIPTIONS, VIS_DESCRIPTIONS, WEATHER_DESCRIPTIONS, TRACK_DESCRIPTIONS, INJURED_BUCKETS, COSTS_BUCKETS
import streamlit as st
import math


def filter_by_date(data, start_date, end_date):
    """Filter map data based on selected date range."""
    return data[
        (data['DATETIME'] >= pd.to_datetime(start_date)) &
        (data['DATETIME'] <= pd.to_datetime(end_date))
    ]


def filter_by_temperature(data, start_temp, end_temp):
    """Filter map data based on selected temperature range"""
    return data[
        (data['TEMP'] >= start_temp & data['TEMP'] <= end_temp)
    ]


def filter_by_states(data, selected_states):
    """Filter map data based on selected states."""
    reverse_state_codes = {v: k for k, v in STATE_CODES.items()}
    selected_state_codes = [reverse_state_codes[state]
                            for state, selected in selected_states.items() if selected]
    return data[data['STATE'].isin(selected_state_codes)]


def filter_by_types(data, selected_types):
    """Filter map data based on selected incident types."""
    selected_type_codes = [int(code) for code, description in TYPE_DESCRIPTIONS.items()
                           if selected_types.get(description, False)]
    return data[data['TYPE'].isin(selected_type_codes)]


def filter_by_visibility(data, selected_vis):
    """Filter map data based on selected visibility categories"""
    selected_vis_codes =[int(code) for code, description in VIS_DESCRIPTIONS.items()
                         if selected_vis.get(description, False)]
    return data[data['VISIBLTY'].isin(selected_vis_codes)]


def filter_by_weather(data, selected_weather):
    """Filter map data based on selected weather categories"""
    selected_weather_codes = [int(code) for code, description in WEATHER_DESCRIPTIONS.items()
                              if selected_weather.get(description, False)]
    return data[data['WEATHER'].isin(selected_weather_codes)]


def filter_by_region(data, region):
    """
    Split data into Alaska and Continental USA regions.
    Returns the appropriate dataset based on selected region.
    """
    if region == "Alaska":
        return data[(data['Latitude'] > 50) & (data['Longitude'] < -130)]
    else:  # Continental USA
        return data[~((data['Latitude'] > 50) & (data['Longitude'] < -130))]


def bucket_to_numeric(bucket, data):
    if bucket == "0":
        return 0
    elif bucket == "0.25 million":
        return 250000       
    elif bucket == "0.5 million":
        return 500000
    elif bucket == "1 million":
        return 1000000
    elif bucket == "2 million":
        return 2000000
    elif bucket == "5 million":
        return 5000000
    elif bucket == "10 million":
        return 10000000
    elif bucket == "20 million":
        return 20000000
    elif bucket == "20+ million":
        return int(math.ceil(data['ACCDMG'].max()))
    

def bucket_to_numeric_injured(bucket, data):
    if bucket == "100+":
        return int(math.ceil(data['TOTINJ'].max()))  # Use infinity for open-ended range
    return bucket  # Return numeric values as is


def setup_filters(map_data):
    st.sidebar.header("Filters")

    # Date filters
    start_date = st.sidebar.date_input(
        "Start Date",
        map_data['DATETIME'].min().date(),
        min_value=map_data['DATETIME'].min().date(),
        max_value=map_data['DATETIME'].max().date()
    )
    end_date = st.sidebar.date_input(
        "End Date",
        map_data['DATETIME'].max().date(),
        min_value=map_data['DATETIME'].min().date(),
        max_value=map_data['DATETIME'].max().date()
    )

    if start_date > end_date:
        return "Start date cannot be after end date." # Error message
    
    # Temperature Slider
    min_temp = int(math.floor(map_data['TEMP'].min()))
    max_temp = int(math.ceil(map_data['TEMP'].max()))
    temp_range = st.sidebar.slider(
            "Temperature Range (F)",
            min_value=min_temp,
            max_value=max_temp,
            value=(min_temp, max_temp),
            step=1
        )
    
    # Speed Slider
    min_speed = int(math.floor(map_data['TRNSPD'].min()))
    max_speed = int(math.ceil(map_data['TRNSPD'].max()))
    speed_range = st.sidebar.slider(
            "Speed Range (mph)",
            min_value=min_speed,
            max_value=max_speed,
            value=(min_speed, max_speed),
            step=1
        )
    
    # Kill Slider
    min_kill = int(math.floor(map_data['TOTKLD'].min()))
    max_kill = int(math.ceil(map_data['TOTKLD'].max()))
    kill_range = st.sidebar.slider(
            "Total People Killed",
            min_value=min_kill,
            max_value=max_kill,
            value=(min_kill, max_kill),
            step=1
        )

    # Sidebar slider for Damage Costs
    min_costs = int(math.floor(map_data['ACCDMG'].min()))
    max_costs = int(math.ceil(map_data['ACCDMG'].max()))
    cost_range = st.sidebar.select_slider(
        "Select Damage Cost Range:",
        options=COSTS_BUCKETS,
        value=(COSTS_BUCKETS[0], COSTS_BUCKETS[-1]), # Default to full range
        format_func=lambda x: x
        )
    min_costs = bucket_to_numeric(cost_range[0], map_data)
    max_costs = bucket_to_numeric(cost_range[1], map_data)

    # Sidebar slider for Total Injured
    inj_range = st.sidebar.select_slider(
        "Select Total Injured Range:",
        options=INJURED_BUCKETS,
        value=(INJURED_BUCKETS[0], INJURED_BUCKETS[-1]), # Default to full range
        format_func=lambda x: str(x)
        )
    min_inj = bucket_to_numeric_injured(inj_range[0], map_data)
    max_inj = bucket_to_numeric_injured(inj_range[1], map_data)

    # Incident Type filters
    with st.sidebar.expander("Incident Types", expanded=False):
        cols = st.columns(2)
        types_per_col = -(-len(TYPE_DESCRIPTIONS) // 2)

        # Select All/Deselect All buttons
        col1, col2 = st.columns([1, 1])
        if col1.button("Select All", key="select_all_types"):
            for code in TYPE_DESCRIPTIONS.keys():
                st.session_state[f"type_{code}"] = True
        if col2.button("Deselect All", key="deselect_all_types"):
            for code in TYPE_DESCRIPTIONS.keys():
                st.session_state[f"type_{code}"] = False

        selected_types = {}
        for i, (code, description) in enumerate(TYPE_DESCRIPTIONS.items()):
            col_index = i // types_per_col
            key = f"type_{code}"
            if key not in st.session_state:
                st.session_state[key] = True  # Default to selected
            selected_types[description] = cols[col_index].checkbox(
                description, value=st.session_state[key], key=key
            )


    # Visibility filters
    with st.sidebar.expander("Visibility", expanded=False):
        cols = st.columns(2)
        vis_per_col = -(-len(VIS_DESCRIPTIONS) // 2)

        # Select All/Deselect All buttons
        col1, col2 = st.columns([1, 1])
        if col1.button("Select All", key="select_all_vis"):
            for code in VIS_DESCRIPTIONS.keys():
                st.session_state[f"vis_{code}"] = True
        if col2.button("Deselect All", key="deselect_all_vis"):
            for code in VIS_DESCRIPTIONS.keys():
                st.session_state[f"vis_{code}"] = False

        selected_vis = {}
        for i, (code, description) in enumerate(VIS_DESCRIPTIONS.items()):
            col_index = i // vis_per_col
            key = f"vis_{code}"
            if key not in st.session_state:
                st.session_state[key] = True  # Default to selected
            selected_vis[description] = cols[col_index].checkbox(
                description, value=st.session_state[key], key=key
            )
    

    # Weather filters
    with st.sidebar.expander("Weather", expanded=False):
        cols = st.columns(2)
        weather_per_col = -(-len(WEATHER_DESCRIPTIONS) // 2)

        # Select All/Deselect All buttons
        col1, col2 = st.columns([1, 1])
        if col1.button("Select All", key="select_all_weather"):
            for code in WEATHER_DESCRIPTIONS.keys():
                st.session_state[f"weather_{code}"] = True
        if col2.button("Deselect All", key="deselect_all_weather"):
            for code in WEATHER_DESCRIPTIONS.keys():
                st.session_state[f"weather_{code}"] = False

        selected_weather = {}
        for i, (code, description) in enumerate(WEATHER_DESCRIPTIONS.items()):
            col_index = i // weather_per_col
            key = f"weather_{code}"
            if key not in st.session_state:
                st.session_state[key] = True  # Default to selected
            selected_weather[description] = cols[col_index].checkbox(
                description, value=st.session_state[key], key=key
            )

     # Track type filters
    with st.sidebar.expander("Track Type", expanded=False):
        cols = st.columns(2)
        track_per_col = -(-len(TRACK_DESCRIPTIONS) // 2)

        # Select All/Deselect All buttons
        col1, col2 = st.columns([1, 1])
        if col1.button("Select All", key="select_all_track"):
            for code in TRACK_DESCRIPTIONS.keys():
                st.session_state[f"track_{code}"] = True
        if col2.button("Deselect All", key="deselect_all_track"):
            for code in TRACK_DESCRIPTIONS.keys():
                st.session_state[f"track_{code}"] = False

        selected_track = {}
        for i, (code, description) in enumerate(TRACK_DESCRIPTIONS.items()):
            col_index = i // track_per_col
            key = f"track_{code}"
            if key not in st.session_state:
                st.session_state[key] = True  # Default to selected
            selected_track[description] = cols[col_index].checkbox(
                description, value=st.session_state[key], key=key
            )


    # State filters
    with st.sidebar.expander("States", expanded=False):
        cols = st.columns(4)
        states_per_col = -(-len(STATE_CODES) // 4)

        # Select All/Deselect All buttons
        col1, col2 = st.columns([1, 1])
        if col1.button("Select All"):
            for state in STATE_CODES.values():
                st.session_state[f"state_{state}"] = True
        if col2.button("Deselect All"):
            for state in STATE_CODES.values():
                st.session_state[f"state_{state}"] = False

        selected_states = {}
        for i, (code, state) in enumerate(STATE_CODES.items()):
            col_index = i // states_per_col
            key = f"state_{state}"
            if key not in st.session_state:
                st.session_state[key] = True  # Default to selected
            selected_states[state] = cols[col_index].checkbox(
                state, value=st.session_state[key], key=key
            )

    # Apply filters
    reverse_state_codes = {v: k for k, v in STATE_CODES.items()}
    selected_filter = (
        (map_data['DATETIME'] >= pd.to_datetime(start_date)) &
        (map_data['DATETIME'] <= pd.to_datetime(end_date)) &
        (map_data['TEMP']>= temp_range[0]) & 
        (map_data['TEMP'] <= temp_range[1]) &
        (map_data['TRNSPD'] >= speed_range[0]) &
        (map_data['TRNSPD'] <= speed_range[1]) &
        (map_data['ACCDMG'] >= min_costs) &
        (map_data['ACCDMG'] <= max_costs) &
        (map_data['TOTKLD'] >= kill_range[0]) &
        (map_data['TOTKLD'] <= kill_range[1]) &
        (map_data['TOTINJ'] >= min_inj) & 
        (map_data['TOTINJ'] <= max_inj) &
        (map_data['TYPE'].isin(
            [int(code) for code, description in TYPE_DESCRIPTIONS.items()
             if selected_types.get(description, False)]
        )) &
        (map_data['VISIBLTY'].isin(
            [int(code) for code, description in VIS_DESCRIPTIONS.items()
             if selected_vis.get(description, False)]
        )) &
        (map_data['WEATHER'].isin(
            [int(code) for code, description in WEATHER_DESCRIPTIONS.items()
             if selected_weather.get(description, False)]
        )) &
        (map_data['TYPTRK'].isin(
            [int(code) for code, description in TRACK_DESCRIPTIONS.items()
             if selected_track.get(description, False)]
        )) &
        (map_data['STATE'].isin(
            [reverse_state_codes[state]
                for state, selected in selected_states.items() if selected]
        ))   
    )

    return selected_filter
