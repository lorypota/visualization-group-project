import streamlit as st
from filters import setup_filters
from map_visualization import update_figure_data, map, initialize_data, initialize_figure
from styles import CSS_STYLE
import pandas as pd
from plots import *
from filters import filter_by_date, filter_by_types, filter_by_states
from map_visualization import create_base_figure, update_figure_data, map
from config import STATE_CODES, TYPE_DESCRIPTIONS, DATA_PATH

st.set_page_config(layout="wide")
st.markdown(CSS_STYLE, unsafe_allow_html=True)

def main():
    initialize_data()
    initialize_figure()
    map_data = st.session_state.map_data
    selected_filter = setup_filters(map_data)

    if isinstance(selected_filter, str):
        st.error(selected_filter)
    else:
        # Update the figure data
        update_figure_data(st.session_state.fig, map_data, selected_filter)

        # Display the figure
        map(st.session_state.fig, map_data, selected_filter)
    
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
