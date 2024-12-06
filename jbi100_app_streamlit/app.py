import streamlit as st
import pandas as pd
from filters import filter_by_date, filter_by_types, filter_by_states
from map_visualization import create_base_figure, update_figure_data
from config import STATE_CODES, TYPE_DESCRIPTIONS, DATA_PATH

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        [data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 330px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


def initialize_data():
    if 'map_data' not in st.session_state:
        data = pd.read_csv(DATA_PATH, low_memory=False)
        # Filter out invalid coords
        data = data[(data['Latitude'] != 0) & (data['Longitude'] != 0)].copy()
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
    with st.sidebar.expander("Incident Types", expanded=True):
        cols = st.columns(2)  # Using 2 columns for incident types
        types_per_col = -(-len(TYPE_DESCRIPTIONS) // 2)
        selected_types = {}
        for i, (code, description) in enumerate(TYPE_DESCRIPTIONS.items()):
            col_index = i // types_per_col
            key = f"type_{code}"
            selected_types[description] = cols[col_index].checkbox(
                description, value=True, key=key)

    # State filters
    with st.sidebar.expander("States", expanded=True):
        cols = st.columns(4)
        states_per_col = -(-len(STATE_CODES) // 4)
        selected_states = {}
        for i, (code, state) in enumerate(STATE_CODES.items()):
            col_index = i // states_per_col
            key = f"state_{state}"
            selected_states[state] = cols[col_index].checkbox(
                state, value=True, key=key)

    # Apply filters
    filtered_data = filter_by_date(st.session_state.map_data, start_date, end_date)
    filtered_data = filter_by_types(filtered_data, selected_types)
    filtered_data = filter_by_states(filtered_data, selected_states)

    # Update the figure data
    update_figure_data(st.session_state.fig, filtered_data)

    # Display the figure
    st.plotly_chart(
        st.session_state.fig,
        key="main_map",
        use_container_width=True,
        config={
            'displayModeBar': True,
            'scrollZoom': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['resetScale2d']
        }
    )


if __name__ == "__main__":
    main()
