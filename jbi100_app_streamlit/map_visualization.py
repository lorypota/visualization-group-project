import streamlit as st
import plotly.express as px
import pandas as pd
import json
from datetime import date
from config import *

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

def update_figure_data(fig, data, selected_filter, selected_markers=[]):
    # Separate selected and unselected data
    global selected_data
    global unselected_data
    selected_data = data[selected_filter].copy()
    unselected_data = data[~selected_filter].copy()
    selected_markers = st.session_state.callback_data.get('selected_markers', [])
      
    # Remove existing traces
    fig.data = []
    if len(selected_markers) > 0:
        print("I AM HERE !!")
        selected_data_copy = st.session_state.callback_data.get('selected_data_back', [])
        unselected_data_copy = st.session_state.callback_data.get('unselected_data_back', [])
        
        # Add the unselected trace first
        fig.add_scattermapbox(
            lat=unselected_data_copy["Latitude"].tolist(),
            lon=unselected_data_copy["Longitude"].tolist(),
            hovertext=(
                unselected_data_copy["DATETIME"].dt.strftime('%Y-%m-%d %H:%M') + 
                "<br>Lat: " + unselected_data_copy["Latitude"].astype(str) + 
                "<br>Lon: " + unselected_data_copy["Longitude"].astype(str)
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
            lat=selected_data_copy["Latitude"].tolist(),
            lon=selected_data_copy["Longitude"].tolist(),
            hovertext=(
                selected_data_copy["DATETIME"].dt.strftime('%Y-%m-%d %H:%M') + 
                "<br>Lat: " + selected_data_copy["Latitude"].astype(str) + 
                "<br>Lon: " + selected_data_copy["Longitude"].astype(str)
            ).tolist(),
            mode='markers',
            marker=marker_properties_selected(),
            selected=dict(marker=marker_properties_selected()),
            unselected=dict(marker=marker_properties_unselected()),
            hovertemplate="%{hovertext}<extra></extra>",
            name="Selected",
        )
        
        # Add scattermapbox for selected markers
        print("selected markers.....")
        selected_markers['DATETIME'] = pd.to_datetime(selected_markers['DATETIME'], errors='coerce')
        fig.add_scattermapbox(
            lat=selected_markers["Latitude"].tolist(),
            lon=selected_markers["Longitude"].tolist(),
            mode='markers',
            marker=dict(size=6, opacity=1, color='rgb(255, 255, 0)'),  # Brighter yellow
            selected=dict(marker=marker_properties_unselected()),
            unselected=dict(marker=marker_properties_unselected()),
            hovertext=(
                selected_markers["DATETIME"].dt.strftime('%Y-%m-%d %H:%M') + 
                "<br>Lat: " + selected_markers["Longitude"].astype(str) + 
                "<br>Lon: " + selected_markers["Longitude"].astype(str)
            ).tolist(),
            hovertemplate="%{hovertext}<extra></extra>",

            name="Unselected",
        )
        
    else:
        st.session_state.callback_data['selected_data_back'] = []
        st.session_state.callback_data['unselected_data_back'] = []
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
            st.write("")
            st.write("")
            # Display meta-information in a structured format
            col1, col2 = st.columns(2)
            st.subheader("Meta-Information for Selected Accident")
            
            # Extract the single row of data
            accident_data = selected_data.iloc[0]
            
            # Location Information
            with col1:
                st.subheader("Location Information")
                st.write(f"**State:** {STATE_CODES[accident_data['STATE']]}")
                st.write(f"**County:** {accident_data['COUNTY']}")
                st.write(f"**Latitude:** {accident_data['Latitude']}")
                st.write(f"**Longitude:** {accident_data['Longitude']}")
                st.write(f"**Milepost:** {accident_data['MILEPOST']}")
            
            # Timing Information
            with col2:
                st.subheader("Timing Information")
                st.write(f"**Year:** {accident_data['YEAR']}")
                month = date(1900, accident_data['MONTH'], 1).strftime('%B')
                st.write(f"**Month:** {month}")
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
            st.subheader("Accident Description")
            st.write(f"{accident_data['NARR']}")
            st.write("")
        return True
    
    return False


def bar_callback():
    if st.session_state.bottom_panel:
        # Access the selected points from the bar chart
        selected_points = st.session_state.bottom_panel['selection']['points']
        
        # Check if selected_points is empty
        if not selected_points:
            print("No points selected.")
            return  # Exit the function if no points are selected

        x_values = [item['x'] for item in selected_points]
        print(f"Selected x_values: {x_values}")

        # Extract x_var and y_var from customdata
        x_var, y_var = selected_points[0]['customdata']
        print(f"x_var: {x_var}, y_var: {y_var}")

        # Get the corresponding column name
        x_var_col = VARNAMES_TO_DATASET[x_var]
        print(f"x_var_col: {x_var_col}")

        # Ensure selected_data exists and is valid
        global selected_data
        global unselected_data
        data = selected_data.copy()
        data_unselected = unselected_data.copy()
        if data is None or data.empty:
            print("selected_data is empty or None. Using st.session_state.map_data instead.")
            data = st.session_state.map_data

        print(f"Data for {x_var_col}:")
        print(data[x_var_col])

        # Convert x_values based on the column type
        if x_var_col == 'TYPE':
            # Map the description values in x_values to their corresponding keys and convert to float
            x_values = [float(key) for value in x_values if (key := next((k for k, v in TYPE_DESCRIPTIONS.items() if v == value), None))]
            print(f"Converted x_values to float keys for TYPE: {x_values}")
        
        elif x_var_col == 'VISIBLTY':
            # Map the description values in x_values to their corresponding keys for VIS
            x_values = [float(key) for value in x_values if (key := next((k for k, v in VIS_DESCRIPTIONS.items() if v == value), None))]
            print(f"Converted x_values to float keys for VIS: {x_values}")
        
        elif x_var_col == 'WEATHER':
            # Map the description values in x_values to their corresponding keys for WEATHER
            x_values = [float(key) for value in x_values if (key := next((k for k, v in WEATHER_DESCRIPTIONS.items() if v == value), None))]
            print(f"Converted x_values to float keys for WEATHER: {x_values}")
        
        elif x_var_col == 'TYPTRK':
            # Map the description values in x_values to their corresponding keys for TRACK
            x_values = [float(key) for value in x_values if (key := next((k for k, v in TRACK_DESCRIPTIONS.items() if v == value), None))]
            print(f"Converted x_values to float keys for TRACK: {x_values}")
        
        else:
            print("No conversion to keys for x_values as x_var_col is not 'TYPE', 'VIS', 'WEATHER', or 'TRACK'.")

        if data is not None and not data.empty:
            # Properly filter the DataFrame for all x_values
            x_data = data[data[x_var_col].isin(x_values)]

            # Extract Latitude, Longitude, and DATETIME
            print(data[x_var_col])
            if {'Latitude', 'Longitude', 'DATETIME'}.issubset(data.columns):
                df = x_data[['Latitude', 'Longitude', 'DATETIME', x_var_col]]
                print("Extracted DataFrame:")
                print(df)
            else:
                print("Required columns (Latitude, Longitude, DATETIME) are not in the data.")
        else:
            print("No data available after fallback to st.session_state.map_data.")

        if len(df) > 0:
            st.session_state.callback_data = {
                    'selected_markers': df,
                    'selected_data_back': data,
                    'unselected_data_back': data_unselected,
                    'selected_variable_back': x_var,
                    'second_selected_var_back': y_var
                }
        
        print(f"x_values type: {type(x_values[0])}")
        print(f"TYPE column dtype: {data[x_var_col].dtype}")


def simple_graph(key, selected_filter, selected_variable, second_selected_var):   # ex update_bottom_panel
    st.session_state.callback_data['selected_markers'] = []
    if key in PLOT_FUNCTIONS:
        global selected_data
        global unselected_data
        selected_data_copy = st.session_state.callback_data.get('selected_data_back', [])
        unselected_data_copy = st.session_state.callback_data.get('unselected_data_back', [])
        
        # Check if selected_variable_back and selected_variable are different
        selected_variable_back = st.session_state.callback_data.get('selected_variable_back', None)
        second_selected_var_back = st.session_state.callback_data.get('second_selected_var_back', None)
        
        if selected_variable_back != selected_variable or second_selected_var_back != second_selected_var:
            st.session_state.callback_data['selected_data_back'] = []
            st.session_state.callback_data['unselected_data_back'] = []

        plot_func = PLOT_FUNCTIONS[key]
        
        fig = None
        
        # Check if selected_data_back is available, otherwise use selected_data, and then map_data
        if len(selected_data_copy) > 0:
            selected_data = selected_data_copy[selected_filter].copy()
            unselected_data = unselected_data_copy[selected_filter].copy()
        
        if selected_data is not None and not selected_data.empty:
            data_to_use = selected_data[selected_filter]
        else:
            data_to_use = st.session_state.map_data[selected_filter]
        
        # Use the selected data (or map_data) for plotting
        fig = plot_func(data_to_use, selected_variable, second_selected_var)
        st.plotly_chart(fig, on_select=bar_callback, key="bottom_panel", use_container_width=True)        
    else:
        st.write("No predefined plot available for this selection.")


def parallel_coord_plot(selected_filter, par_plot_vars, binning):
    global selected_data

    if len(selected_data) == 0:
        selected_data = st.session_state.map_data[selected_filter].copy()

    parallel_fig = parallel_plot(selected_data, par_plot_vars, binning)
    st.plotly_chart(parallel_fig, use_container_width=True)
 