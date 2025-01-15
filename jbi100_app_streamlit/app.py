

import streamlit as st
from filters import setup_filters
from map_visualization import update_figure_data, map, initialize_data, initialize_figure, check_single_event,  simple_graph, parallel_coord_plot
from styles import CSS_STYLE
from constants import VARIABLES, PLOT_FUNCTIONS
import plotly.express as px

st.set_page_config(layout="wide", page_icon="🚆", page_title="RailAlert!")
st.markdown(CSS_STYLE, unsafe_allow_html=True)

# Name and logo
st.sidebar.write("<div style='text-align:center;'><h1>RailAlert!</h1></div>", unsafe_allow_html=True)
col1, col2, col3 = st.sidebar.columns([1, 2, 1])
with col2:
    st.image("jbi100_app_streamlit/assets/RailAlertLogoNoBckg.png", use_container_width=True)

def main():
    initialize_data()
    initialize_figure()
    map_data = st.session_state.map_data
    selected_filter = setup_filters(map_data)

    if 'callback_data' not in st.session_state:
        st.session_state.callback_data = {}
    
    if isinstance(selected_filter, str):
        st.error(selected_filter)
    else:
        # Update the figure data for the map
        update_figure_data(st.session_state.fig, map_data, selected_filter)

        # Display the map visualization
        map(st.session_state.fig, map_data, selected_filter)

    # If not viewing a single event, show additional visualizations
    if not check_single_event():
        _, container1, _ = st.columns([0.02, 1, 0.02], gap="large")

        with container1:
            st.title("Explore the Data")
            st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
            _, box1, _, box2, _ = st.columns([1, 2, 0.5, 2, 1])

            with box1:
                # First variable selection
                selected_variable = st.selectbox(
                    "First Variable of Interest:",
                    options=list(VARIABLES.keys()),
                    key="first_variable"
                )

            with box2:
                second_selected_var = None
                if selected_variable:
                    second_selected_var = st.selectbox(
                        f"Second Variable of Interest (for {selected_variable}):",
                        options=VARIABLES[selected_variable],
                        key=f"dropdown_{selected_variable}"
                    )

        _, container2, _ = st.columns([0.1, 1, 0.1], gap="large")

        with container2:
            if selected_variable and second_selected_var:
                key = (selected_variable, second_selected_var)
                if key in PLOT_FUNCTIONS:
                    simple_graph(key, selected_filter, selected_variable, second_selected_var)
                else:
                    st.write("No predefined plot available for this selection.")

        padding_left3, container3, padding_right3 = st.columns([0.02, 1, 0.02], gap="large")

        with container3:
            st.title("Combine!")
            st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
            _, box3, _, box4, _, box5, _, box6, _ = st.columns([1, 2, 0.3, 2, 0.3, 2, 0.3, 2, 1])
            st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)

            # Define the available variables for the parallel coordinate plot
            parallel_plot_variables = ["🌡️ Temperature", "🌥️ Weather", "🌫️ Visibility",
                                       "🚄 Speed", "🚊 Track Type", "🛤️ Track Class", "💸 Total Damage Costs", "🪨 Weight", 
                                       "🍷 Alcohol", "💉 Drugs", 
                                       "🤕 Total People Injured", "🪦 Total People Killed"]
            
            parallel_plot_variables2 = ["-- empty --", 
                                        "🌡️ Temperature", "🌥️ Weather", "🌫️ Visibility",
                                        "🚄 Speed", "🚊 Track Type", "🛤️ Track Class", "💸 Total Damage Costs", "🪨 Weight",
                                        "🍷 Alcohol", "💉 Drugs", 
                                        "🤕 Total People Injured", "🪦 Total People Killed"]
            
            with box3:
                par_plot_var_1 = st.selectbox(
                    "First variable",
                    options=parallel_plot_variables,
                    index=0
                )

            with box4:
                par_plot_var_2 = None
                if par_plot_var_1:
                    par_plot_var_2 = st.selectbox(
                        "Second variable",
                        options=parallel_plot_variables,
                        index=1
                    )

            with box5:
                par_plot_var_3 = None
                if par_plot_var_2:
                    par_plot_var_3 = st.selectbox(
                        "Third variable",
                        options=parallel_plot_variables2,
                        index=4
                    )

            with box6:
                par_plot_var_4 = None
                if par_plot_var_3:
                    par_plot_var_4 = st.selectbox(
                        "Fourth variable",
                        options=parallel_plot_variables2,
                        index=5
                    )

        padding_left4, container4, padding_right4 = st.columns([0.05, 1, 0.05], gap="medium")
        par_plot_vars = [par_plot_var_1, par_plot_var_2, par_plot_var_3, par_plot_var_4]
        vars_set = set(par_plot_vars)

        padding_left5, container5, padding_right5 = st.columns([3, 1, 2], gap="large")
        with container5:
            binning_toggle = st.checkbox("Enable Binning", value=True)

        with container4:
            st.write("")
            if len(vars_set) >= 2:
                parallel_coord_plot(selected_filter, par_plot_vars, binning_toggle)
            else:
                st.write("Please select at least two distinct variables to display the parallel coordinate plot.")

if __name__ == "__main__":
    main()
