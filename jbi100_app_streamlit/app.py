import streamlit as st
from filters import setup_filters
from map_visualization import update_figure_data, map, initialize_data, initialize_figure, check_single_event
from styles import CSS_STYLE
from config import VARIABLES, PLOT_FUNCTIONS

st.set_page_config(layout="wide")
st.markdown(CSS_STYLE, unsafe_allow_html=True)

# Name and logo
st.sidebar.write("<div style='text-align:center;'><h1>RailAlert!</h1></div>", unsafe_allow_html=True)
col1, col2, col3 = st.sidebar.columns([1, 2, 1])
with col2:
    st.image("jbi100_app_streamlit/assets/RailAlertLogoNoBckg.png",
             use_container_width=True)

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

   
    # example containers
    # check if only 1 event is selected on the map:
    if check_single_event():
        # st.success("Meta-information displayed for the selected accident.")
        pass
    else:
        padding_left, container1, container2, padding_right = st.columns([0.1, 1, 5, 0.1], gap="large")

        with container1:
            st.divider()
            st.write("Select the variables you want to analyze.") 

            # Compact dropdown menus
            selected_variable = st.selectbox(
                "First Variable of Interest:",
                options=list(VARIABLES.keys()),
                key="first_variable"
            )

            second_selected_var = None
            if selected_variable:
                second_selected_var = st.selectbox(
                    f"Second Variable of Interest (for {selected_variable}):",
                    options=VARIABLES[selected_variable],
                    key=f"dropdown_{selected_variable}"
                )
    
        with container2:

            if selected_variable and second_selected_var:
                key = (selected_variable, second_selected_var)
                print(key)
                if key in PLOT_FUNCTIONS:
                    # Generate and display the corresponding plot
                    plot_func = PLOT_FUNCTIONS[key]
                    fig = plot_func(map_data[selected_filter], selected_variable, second_selected_var)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.write("No predefined plot available for this selection.")


if __name__ == "__main__":
    main()
