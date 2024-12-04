import streamlit as st
import pandas as pd
import plotly.express as px

# Mapbox token
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoibWdnaW9yZGFubyIsImEiOiJjbTNweXYycXIwOWJ6MmxzZDVwM3I3eTF1In0.0MLyHVjtBOB7HP_dk7DTsw"

# File path to the dataset
file_path = '/Users/matteogennarogiordano/ProgrammingProjects/Visualization_Project/Railroad_Incidents/CleanedDataset.csv'  # Replace with the correct path to your file
data = pd.read_csv(file_path)

# Filter data to exclude rows with missing or zero lat/long
map_data = data[(data['Latitude'] != 0) & (data['Longitude'] != 0)].copy()

# Convert DATETIME to datetime format
map_data['DATETIME'] = pd.to_datetime(map_data['DATETIME'])

# Streamlit layout
st.set_page_config(layout="wide")

# Sidebar for date filter
st.sidebar.header("Filters")
start_date = st.sidebar.date_input(
    "Start Date", map_data['DATETIME'].min().date()
)
end_date = st.sidebar.date_input(
    "End Date", map_data['DATETIME'].max().date()
)

# Toggle for map selection
map_choice = st.sidebar.radio(
    "Choose Map Region:",
    ("Continental USA", "Alaska"),
)

# Ensure valid date range
if start_date > end_date:
    st.sidebar.error("Start date must be before end date.")
else:
    # Filter data based on selected date range
    filtered_data = map_data[
        (map_data['DATETIME'] >= pd.to_datetime(start_date)) &
        (map_data['DATETIME'] <= pd.to_datetime(end_date))
    ]

    # Filter data for Alaska and Continental USA
    alaska_data = filtered_data[(filtered_data['Latitude'] > 50) & (filtered_data['Longitude'] < -130)]
    usa_data = filtered_data[~((filtered_data['Latitude'] > 50) & (filtered_data['Longitude'] < -130))]

    # Determine which map to display
    if map_choice == "Continental USA":
        map_data = usa_data
        center_coords = {"lat": 39.8, "lon": -98.6}
        zoom_level = 3.5
        title = "Map: Continental USA"
    else:  # "Alaska"
        map_data = alaska_data
        center_coords = {"lat": 64.2, "lon": -150}
        zoom_level = 3.5
        title = "Map: Alaska"

    # Plot the selected map
    map_fig = px.scatter_mapbox(
        map_data,
        lat="Latitude",
        lon="Longitude",
        hover_name="DATETIME",
        zoom=zoom_level,
        center=center_coords,
        title=title,
    )

    map_fig.update_layout(
        mapbox=dict(
            accesstoken=MAPBOX_ACCESS_TOKEN,
            style="mapbox://styles/mapbox/streets-v12",
            filter=["!=", "class", "motorway"],
            paint={"line-opacity": 0}
        ),
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
    )

    # Display the map
    st.plotly_chart(map_fig, use_container_width=True)