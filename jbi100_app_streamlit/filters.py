import pandas as pd
from config import STATE_CODES, TYPE_DESCRIPTIONS
import streamlit as st


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


def filter_by_types(data, selected_types):
    """Filter map data based on selected incident types."""
    selected_type_codes = [int(code) for code, description in TYPE_DESCRIPTIONS.items()
                           if selected_types.get(description, False)]
    return data[data['TYPE'].isin(selected_type_codes)]


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
        (map_data['TYPE'].isin(
            [int(code) for code, description in TYPE_DESCRIPTIONS.items()
             if selected_types.get(description, False)]
        )) &
        (map_data['STATE'].isin(
            [reverse_state_codes[state]
                for state, selected in selected_states.items() if selected]
        ))
    )

    return selected_filter
