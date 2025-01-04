import streamlit as st
from filters import setup_filters
from map_visualization import update_figure_data, map, initialize_data, initialize_figure
from styles import CSS_STYLE
from config import VARIABLES, PLOT_FUNCTIONS

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
        st.subheader("Controls")
        st.write("Select the variables you want to analyze.") 
        col1, col2 = st.columns(2)
        with col1:
            st.write("First variable of Interest:")
            selected_variable = None
            selected_variable = st.radio( "Choose one variable", 
                                         options=list(VARIABLES.keys()), 
                                         key="first_variable"
                                                 )
        with col2:
            if selected_variable:
                second_selected_var = "Number of Accidents" #default
                st.write(f"Choose a second Variable of Interest to:{selected_variable}:")
                # Use a radio button for single selection
                options = VARIABLES[selected_variable]
                second_selected_var = st.radio("Choose one variable",
                                               options=options,
                                               key=f"radio_{selected_variable}"
                                                                               )
  

    with container2:
        st.subheader("Visualization")
        st.write("This is the corresponding visualization.")
        if not map_data[selected_filter].empty:
            if selected_variable and second_selected_var:
                key = (selected_variable, second_selected_var)
                if key in PLOT_FUNCTIONS:
                    # Generate and display the corresponding plot
                    plot_func = PLOT_FUNCTIONS[key]
                    fig = plot_func(map_data[selected_filter], selected_variable, second_selected_var)
                    st.pyplot(fig)
                else:
                    st.write("No predefined plot available for this selection.")
        else:
            st.write("You haven't selected any accidents, please check your filters")
if __name__ == "__main__":
    main()
