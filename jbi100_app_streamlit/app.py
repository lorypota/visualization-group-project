import streamlit as st
from filters import filter_by_date, filter_by_states, filter_by_region
from map_visualization import create_map
from config import STATE_CODES, DATA_PATH
import pandas as pd

# Page configuration
st.set_page_config(layout="wide")

# Custom CSS for sidebar
st.markdown(
    """
    <style>
        [data-testid="stSidebar"][aria-expanded="true"]{
            min-width: 330px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

def main():

    # Load preprocessed data
    data = pd.read_csv(DATA_PATH)
    map_data = data[(data['Latitude'] != 0) & (data['Longitude'] != 0)].copy()
    map_data['DATETIME'] = pd.to_datetime(map_data['DATETIME'])

    # Sidebar filters
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

    # Map region selection
    map_choice = st.sidebar.radio(
        "Choose Map Region:",
        ("Continental USA", "Alaska"),
    )

    # Create checkboxes for states
    with st.sidebar.expander("State Filters", expanded=True):
        # Create 4 columns for state checkboxes
        cols = st.columns(4)

        # Calculate states per column (ceil division to ensure all states are included)
        states_per_col = -(-len(STATE_CODES) // 4)  # Ceiling division

        # Create checkboxes for states
        selected_states = {}
        for i, (code, state) in enumerate(STATE_CODES.items()):
            # Determine which column this state should go in
            col_index = i // states_per_col
            # Ensure we don't exceed our column list
            col_index = min(col_index, 3)
            selected_states[state] = cols[col_index].checkbox(
                state, value=True)

    # Apply filters
    filtered_data = filter_by_date(map_data, start_date, end_date)
    filtered_data = filter_by_states(filtered_data, selected_states)
    filtered_data = filter_by_region(filtered_data, map_choice)

    # Create and display map
    map_fig = create_map(filtered_data, map_choice)
    st.plotly_chart(map_fig, use_container_width=True)


if __name__ == "__main__":
    main()
