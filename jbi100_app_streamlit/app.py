import streamlit as st
from filters import setup_filters
from map_visualization import update_figure_data, map, initialize_data, initialize_figure
from styles import CSS_STYLE

st.set_page_config(layout="wide")
st.markdown(CSS_STYLE, unsafe_allow_html=True)

def main():
    initialize_data()
    initialize_figure()
    map_data = st.session_state.map_data
    selected_filter = setup_filters(map_data)

    # Update the figure data
    update_figure_data(st.session_state.fig, map_data, selected_filter)

    # Display the figure
    map(st.session_state.fig, map_data, selected_filter)
    
    # example containers
    container1, container2 = st.columns(2)
    with container1:
        st.subheader("Container 1")
        st.write("This is the first container.")

    with container2:
        st.subheader("Container 2")
        st.write("This is the second container.")

if __name__ == "__main__":
    main()
