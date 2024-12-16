import streamlit as st
import pandas as pd
from plots import *
from filters import filter_by_date, filter_by_types, filter_by_states
from map_visualization import create_base_figure, update_figure_data, map
from config import STATE_CODES, TYPE_DESCRIPTIONS, DATA_PATH

st.set_page_config(layout="wide")

st.markdown(
    """ 
    <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            overflow: hidden; /* Prevent unwanted scrolling */
        }
        [data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 330px;
        }
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .full-screen-map {
            height: calc(100vh); /* Full viewport height minus Streamlit padding */
            margin: 0;
            padding: 0;
            top: 0;
        }
        .block-container {
            padding: 0 !important;
        }
        .stMainBlockContainer .stVerticalBlock {
            gap: 0rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


def initialize_data():
    if 'map_data' not in st.session_state:
        data = pd.read_csv(DATA_PATH, low_memory=False)
        data['DATETIME'] = pd.to_datetime(data['DATETIME'])
        st.session_state.map_data = data


def initialize_figure():
    if 'fig' not in st.session_state:
        st.session_state.fig = create_base_figure()


def main():
    initialize_data()
    initialize_figure()

    st.sidebar.header("Filters")

    # Date filters
    start_date = st.sidebar.date_input(
        "Start Date",
        st.session_state.map_data['DATETIME'].min().date(),
        min_value=st.session_state.map_data['DATETIME'].min().date(),
        max_value=st.session_state.map_data['DATETIME'].max().date()
    )
    end_date = st.sidebar.date_input(
        "End Date",
        st.session_state.map_data['DATETIME'].max().date(),
        min_value=st.session_state.map_data['DATETIME'].min().date(),
        max_value=st.session_state.map_data['DATETIME'].max().date()
    )

    # Incident Type filters
    with st.sidebar.expander("Incident Types", expanded=False):
        cols = st.columns(2)  # Using 2 columns for incident types
        types_per_col = -(-len(TYPE_DESCRIPTIONS) // 2)

        # Add Select All/Deselect All buttons
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
                st.session_state[key] = True  # Default: all selected
            selected_types[description] = cols[col_index].checkbox(
                description, value=st.session_state[key], key=key)

    # State filters
    with st.sidebar.expander("States", expanded=False):
        cols = st.columns(4)
        states_per_col = -(-len(STATE_CODES) // 4)

        # Add Select All/Deselect All buttons
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
                st.session_state[key] = True  # Default: all selected
            selected_states[state] = cols[col_index].checkbox(
                state, value=st.session_state[key], key=key
            )

    # Apply filters to create a selected_filter mask
    reverse_state_codes = {v: k for k, v in STATE_CODES.items()}
    selected_filter = (
        (st.session_state.map_data['DATETIME'] >= pd.to_datetime(start_date)) &
        (st.session_state.map_data['DATETIME'] <= pd.to_datetime(end_date)) &
        (st.session_state.map_data['TYPE'].isin(
            [int(code) for code, description in TYPE_DESCRIPTIONS.items()
             if selected_types.get(description, False)]
        )) &
        (st.session_state.map_data['STATE'].isin(
            [reverse_state_codes[state]
                for state, selected in selected_states.items() if selected]
        ))
    )

    # Update the figure data
    update_figure_data(st.session_state.fig,
                       st.session_state.map_data, selected_filter)

    # Display the figure
    map(st.session_state.fig,
        st.session_state.map_data, selected_filter)
    
    # example containers
    container1, container2 = st.columns(2)
    with container1:
        st.subheader("Container 1")
        st.write("This is the first container.")
        # Dropdown menu for plot selection
        plot_choice = st.selectbox(
            "Select a Plot Type",
            ["Bar Graph", "Scatter Plot", "Time Series Plot"]
        )

    with container2:
        st.subheader("Container 2")
        st.write("This is the second container.")

        # Display the selected plot
        if plot_choice == "Bar Graph":
            plot_bar_graph(st.session_state.map_data[selected_filter])
        elif plot_choice == "Scatter Plot":
            plot_scatter_plot(st.session_state.map_data[selected_filter])
        elif plot_choice == "Time Series Plot":
            plot_timeseries(st.session_state.map_data[selected_filter])


if __name__ == "__main__":
    main()
