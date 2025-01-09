import streamlit as st
import plotly.express as px
import pandas as pd
import json
from config import MAPBOX_ACCESS_TOKEN, MAP_CONFIGS, DATA_PATH, DEFAULT_STYLE, PLOT_FUNCTIONS

selected_data = None
unselected_data = None

def create_base_figure():
    config = MAP_CONFIGS["Continental USA"]
    fig = px.scatter_mapbox(
        lat=[],
        lon=[],
        zoom=config["zoom_level"],
        center=config["center_coords"],
    )
    fig.update_layout(
        mapbox=dict(
            accesstoken=MAPBOX_ACCESS_TOKEN,
            style=DEFAULT_STYLE,
            bounds={"west": MAP_CONFIGS['bounding_boxes']["lon"][0], "east": MAP_CONFIGS['bounding_boxes']["lon"][1],
                    "south": MAP_CONFIGS['bounding_boxes']["lat"][0], "north": MAP_CONFIGS['bounding_boxes']["lat"][1]},
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        uirevision='fixed',
        showlegend=False,
    )
    return fig

def initialize_data():
    if 'map_data' not in st.session_state:
        data = pd.read_csv(DATA_PATH, low_memory=False)
        data['DATETIME'] = pd.to_datetime(data['DATETIME'])
        st.session_state.map_data = data

def initialize_figure():
    if 'fig' not in st.session_state:
        st.session_state.fig = create_base_figure()

def map(fig, data, selected_filter):
    selected_markers = st.plotly_chart(
        st.session_state.fig,
        key="main_map",
        use_container_width=True,
        config={
            'displayModeBar': True,
            'scrollZoom': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['resetScale2d']
        },
        class_name="full-screen-map",
        on_select="rerun",
    )
    selected_markers = json.dumps(selected_markers)
    

    if selected_markers:
        # Extract latitudes and longitudes from selected_markers
        selection = json.loads(selected_markers)['selection']
        selected_coords = {
            (point['lat'], point['lon'])
            for point in selection['points']
        }

        global selected_data
        global unselected_data

        # Identify rows in the dataset that match selected markers
        selected_data = data[data.apply(
            lambda row: (row['Latitude'], row['Longitude']) in selected_coords, axis=1
        )].copy()

        unselected_data = data[data.apply(
            lambda row: (row['Latitude'], row['Longitude']) not in selected_coords, axis=1
        )].copy()

def marker_properties_selected():
    return dict(size=6, opacity=0.8, color='red')

def marker_properties_unselected():
    return dict(size=6, opacity=0.5, color='#FFCCCB')

def update_figure_data(fig, data, selected_filter, selected_markers=None):
    # Separate selected and unselected data
    global selected_data
    global unselected_data
    selected_data = data[selected_filter].copy()
    unselected_data = data[~selected_filter].copy()

    # Remove existing traces
    fig.data = []

    # Add the unselected trace first
    fig.add_scattermapbox(
        lat=unselected_data["Latitude"].tolist(),
        lon=unselected_data["Longitude"].tolist(),
        hovertext=(
            unselected_data["DATETIME"].dt.strftime('%Y-%m-%d %H:%M') + 
            "<br>Lat: " + unselected_data["Latitude"].astype(str) + 
            "<br>Lon: " + unselected_data["Longitude"].astype(str)
        ).tolist(),
        mode='markers',
        marker=marker_properties_unselected(),
        selected=dict(marker=marker_properties_unselected()),
        unselected=dict(marker=marker_properties_unselected()),
        hovertemplate="%{hovertext}<extra></extra>",
        name="Unselected",
    )

    # Add the selected trace second
    fig.add_scattermapbox(
        lat=selected_data["Latitude"].tolist(),
        lon=selected_data["Longitude"].tolist(),
        hovertext=(
            selected_data["DATETIME"].dt.strftime('%Y-%m-%d %H:%M') + 
            "<br>Lat: " + selected_data["Latitude"].astype(str) + 
            "<br>Lon: " + selected_data["Longitude"].astype(str)
        ).tolist(),
        mode='markers',
        marker=marker_properties_selected(),
        selected=dict(marker=marker_properties_selected()),
        unselected=dict(marker=marker_properties_unselected()),
        hovertemplate="%{hovertext}<extra></extra>",
        name="Selected",
    )



def check_single_event():
    global selected_data
    
    # Debugging: Print the length and columns of the selected data
    # print('This is the length of selected data:', len(selected_data))
    
    # Check if only one event is selected
    if len(selected_data) == 1:
        padding_left, content, padding_right = st.columns([0.05, 1, 0.05], gap="small")
        with content:
            # Display meta-information in a structured format
            col1, col2 = st.columns(2)
            st.subheader("Meta-Information for Selected Accident")
            
            # Extract the single row of data
            accident_data = selected_data.iloc[0]
        
            
            # Location Information
            with col1:
                st.subheader("Location Information")
                st.write(f"**State:** {accident_data['STATE']}")
                st.write(f"**County:** {accident_data['COUNTY']}")
                st.write(f"**Latitude:** {accident_data['Latitude']}")
                st.write(f"**Longitude:** {accident_data['Longitude']}")
                st.write(f"**Milepost:** {accident_data['MILEPOST']}")
            
            # Timing Information
            with col2:
                st.subheader("Timing Information")
                st.write(f"**Year:** {accident_data['YEAR']}")
                st.write(f"**Month:** {accident_data['MONTH']}")
                st.write(f"**Day:** {accident_data['DAY']}")
                st.write(f"**Time:** {accident_data['TIMEHR']}:{accident_data['TIMEMIN']} {accident_data['AMPM']}")
            
            # Expanders for additional information
            with st.expander("Damage Details"):
                st.write(f"**Cars Damaged:** {accident_data['CARSDMG']}")
                st.write(f"**Track Damage:** {accident_data['TRKDMG']}")
                st.write(f"**Total Damage:** {accident_data['ACCDMG']}")
                st.write(f"**Equipment Damage:** {accident_data['EQPDMG']}")
            
            with st.expander("Casualties"):
                st.write(f"**Total Injuries:** {accident_data['TOTINJ']}")
                st.write(f"**Total Killed:** {accident_data['TOTKLD']}")
                st.write(f"**Passenger Injuries:** {accident_data['PASSINJ']}")
                st.write(f"**Passenger Killed:** {accident_data['PASSKLD']}")
                st.write(f"**Other Injuries:** {accident_data['OTHERINJ']}")
                st.write(f"**Other Killed:** {accident_data['OTHERKLD']}")
            
            with st.expander("Train Information"):
                st.write(f"**Train Speed:** {accident_data['TRNSPD']} km/h")
                st.write(f"**Type Speed:** {accident_data['TYPSPD']} km/h")
                st.write(f"**Train Number:** {accident_data['TRNNBR']}")
                st.write(f"**Train Direction:** {accident_data['TRNDIR']}")
                st.write(f"**Tons:** {accident_data['TONS']}")
            
            # Display Narration
            st.subheader("Accident Narration")
            st.write(f"**Narration:** {accident_data['NARR']}")

        return True
    
    return False


def bar_callback():
    if st.session_state.bar:
        # Access the selected points from the bar chart
        selected_points = st.session_state.bar['selection']['points']
        # Extract relevant information from the selected points (e.g., 'x', 'y', 'customdata')
        for point in selected_points:
            print(point['x'])
            # Ensure customdata contains the correct tuple format (latitude, longitude)
            lat_lon = point['customdata'] # This should be a tuple (latitude, longitude)
            df = pd.DataFrame(lat_lon)

            # Rename columns to latitude and longitude
            df.columns = ['latitude', 'longitude']

        
def update_bottom_panel(key, selected_filter, selected_variable, second_selected_var):  
    if key in PLOT_FUNCTIONS:
        global selected_data
        plot_func = PLOT_FUNCTIONS[key]
        
        if len(selected_data) == 0:
            selected_data = st.session_state.map_data[selected_filter].copy()
        # Now pass the filtered data to the plot function
        fig = plot_func(selected_data[selected_filter], selected_variable, second_selected_var)
        # Display the plot
        st.plotly_chart(fig, on_select=bar_callback, key="bar", use_container_width=True)
    else:
        st.write("No predefined plot available for this selection.")

    