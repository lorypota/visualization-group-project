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
        # Update the figure data for the map
        update_figure_data(st.session_state.fig, map_data, selected_filter)

        # Display the map visualization
        map(st.session_state.fig, map_data, selected_filter)

    # Define containers
    controls_container, output_container = st.columns(2)

    with controls_container:
        st.subheader("Controls")
        st.write("Select the type of plot to display:")

        # Initialize session state for plot choice
        if "plot_choice" not in st.session_state:
            st.session_state.plot_choice = "Bar Graph"

        # Custom button-like options for plot selection
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📊 Bar Graph"):
                st.session_state.plot_choice = "Bar Graph"
        with col2:
            if st.button("🔵 Scatter Plot"):
                st.session_state.plot_choice = "Scatter Plot"
        with col3:
            if st.button("📈 Time Series"):
                st.session_state.plot_choice = "Time Series"

    with output_container:
        st.subheader("Visualization")
        st.write("This is the output container where the selected plot is displayed.")

        # Display the selected plot based on session state
        if st.session_state.plot_choice == "Bar Graph":
            plot_bar_graph(map_data[selected_filter])
        elif st.session_state.plot_choice == "Scatter Plot":
            plot_scatter_plot(map_data[selected_filter])
        elif st.session_state.plot_choice == "Time Series":
            plot_timeseries(map_data[selected_filter])


if __name__ == "__main__":
    main()
