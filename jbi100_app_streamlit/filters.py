import pandas as pd
from config import STATE_CODES, TYPE_DESCRIPTIONS, VIS_DESCRIPTIONS, WEATHER_DESCRIPTIONS, TRACK_DESCRIPTIONS, KILL_BUCKETS, INJURED_BUCKETS, COSTS_BUCKETS
import streamlit as st


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
    min_temp = map_data['TEMP'].min()
    max_temp = map_data['TEMP'].max()
    temp_range = st.sidebar.slider(
            "Temperature Range (F)",
            min_value=float(min_temp),
            max_value=float(max_temp),
            value=(float(min_temp), float(max_temp))
        )
    
    # Speed Slider
    min_speed = map_data['TRNSPD'].min()
    max_speed = map_data['TRNSPD'].max()
    speed_range = st.sidebar.slider(
            "Speed Range (mph)",
            min_value=float(min_speed),
            max_value=float(max_speed),
            value=(float(min_speed), float(max_speed))
        )
    
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
    
    # TOT KILLED buckets
    with st.sidebar.expander("Total People Killed", expanded=False):
        cols = st.columns(2)
        kill_per_col = -(-len(KILL_BUCKETS) // 2)  # Divide into two columns

        # Select All/Deselect All buttons
        col1, col2 = st.columns([1, 1])
        if col1.button("Select All", key="select_all_killed"):
            for bucket in KILL_BUCKETS.keys():
                st.session_state[f"kill_{bucket}"] = True
        if col2.button("Deselect All", key="deselect_all_killed"):
            for bucket in KILL_BUCKETS.keys():
                st.session_state[f"kill_{bucket}"] = False

        # Render checkboxes for each bucket
        selected_killed = {}
        for i, bucket in enumerate(KILL_BUCKETS.keys()):  # Use bucket keys for labels
            col_index = i // kill_per_col  # Determine column index
            key = f"kill_{bucket}"
            if key not in st.session_state:
                st.session_state[key] = True  # Default to selected
            selected_killed[bucket] = cols[col_index].checkbox(
                f"{bucket}", value=st.session_state[key], key=key
            )

    # TOT INJURED buckets
    with st.sidebar.expander("Total People Injured", expanded=False):
        cols = st.columns(2)
        injured_per_col = -(-len(INJURED_BUCKETS) // 2)  # Divide into two columns

        # Select All/Deselect All buttons
        col1, col2 = st.columns([1, 1])
        if col1.button("Select All", key="select_all_injured"):
            for bucket in INJURED_BUCKETS.keys():
                st.session_state[f"injured_{bucket}"] = True
        if col2.button("Deselect All", key="deselect_all_injured"):
            for bucket in INJURED_BUCKETS.keys():
                st.session_state[f"injured_{bucket}"] = False

        # Render checkboxes for each bucket
        selected_injured = {}
        for i, bucket in enumerate(INJURED_BUCKETS.keys()):  # Use bucket keys for labels
            col_index = i // injured_per_col  # Determine column index
            key = f"injured_{bucket}"
            if key not in st.session_state:
                st.session_state[key] = True  # Default to selected
            selected_injured[bucket] = cols[col_index].checkbox(
                f"{bucket}", value=st.session_state[key], key=key
            )


    # TOT COSTS buckets
    with st.sidebar.expander("Damage Costs", expanded=False):
        cols = st.columns(2)
        costs_per_col = -(-len(COSTS_BUCKETS) // 2)  # Divide into two columns

        # Select All/Deselect All buttons
        col1, col2 = st.columns([1, 1])
        if col1.button("Select All", key="select_all_costs"):
            for bucket in COSTS_BUCKETS.keys():
                st.session_state[f"costs_{bucket}"] = True
        if col2.button("Deselect All", key="deselect_all_costs"):
            for bucket in COSTS_BUCKETS.keys():
                st.session_state[f"costs_{bucket}"] = False

        # Render checkboxes for each bucket
        selected_costs = {}
        for i, bucket in enumerate(COSTS_BUCKETS.keys()):  # Use bucket keys for labels
            col_index = i // costs_per_col  # Determine column index
            key = f"costs_{bucket}"
            if key not in st.session_state:
                st.session_state[key] = True  # Default to selected
            selected_costs[bucket] = cols[col_index].checkbox(
                f"{bucket}", value=st.session_state[key], key=key
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
        )) &
        (map_data['TOTKLD'].apply(
            lambda x: any(
                condition(x) for bucket, condition in KILL_BUCKETS.items()
                if selected_killed.get(bucket, False)
            )
        )) &
        (map_data['TOTINJ'].apply(
            lambda x: any(
                condition(x) for bucket, condition in INJURED_BUCKETS.items()
                if selected_injured.get(bucket, False)
            )
        ))&
        (map_data['ACCDMG'].apply(
            lambda x: any(
                condition(x) for bucket, condition in COSTS_BUCKETS.items()
                if selected_costs.get(bucket, False)
            )
        ))
        
    )

    return selected_filter
