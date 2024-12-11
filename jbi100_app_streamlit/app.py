import streamlit as st
import pandas as pd
from filters import filter_by_date, filter_by_types, filter_by_states
from map_visualization import create_base_figure, update_figure_data
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
            selected_types[description] = cols[col_index].checkbox(
                description, value=True, key=key)

    # State filters
    with st.sidebar.expander("States", expanded=False):  # Start folded
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
                st.session_state[key] = True  # Initialize all checkboxes as True
            selected_states[state] = cols[col_index].checkbox(
                state, value=st.session_state[key], key=key
            )

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
        },
        class_name="full-screen-map"
    )
   

    container1, container2 = st.columns(2)
    with container1:
        st.subheader("Container 1")
        st.write("This is the first container.")
        # Add content for the first container

    with container2:
        st.subheader("Container 2")
        st.write("This is the second container.")
        # Add content for the second container


if __name__ == "__main__":
    main()
