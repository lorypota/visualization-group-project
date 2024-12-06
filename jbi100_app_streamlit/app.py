import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

load_dotenv()
MAPBOX_ACCESS_TOKEN = os.getenv('MAPBOX_TOKEN')

# File path to the dataset
file_path = '../Railroad_Incidents/CleanedDataset.csv'
data = pd.read_csv(file_path)

# Filter data to exclude rows with missing or zero lat/long and convert to datetime format
map_data = data[(data['Latitude'] != 0) & (data['Longitude'] != 0)].copy() # To move in clean_dataset.py
map_data['DATETIME'] = pd.to_datetime(map_data['DATETIME'])

# TYPE
type_colors = px.colors.qualitative.Set3
type_descriptions = {
    '01': 'Derailment',
    '02': 'Head on collision',
    '03': 'Rearend collision',
    '04': 'Side collision',
    '05': 'Raking collision',
    '06': 'Broken train collision',
    '07': 'Hwy-rail crossing',
    '08': 'RR Grad crossing',
    '09': 'Obstruction',
    '10': 'Explosive-detonation',
    '11': 'Fire/violent rupture',
    '12': 'Other impacts',
    '13': 'Other'
}

# State codes
state_codes = {
    1: 'AL', 2: 'AK', 4: 'AZ', 5: 'AR', 6: 'CA', 8: 'CO', 9: 'CT', 10: 'DE',
    11: 'DC', 12: 'FL', 13: 'GA', 15: 'HI', 16: 'ID', 17: 'IL', 18: 'IN', 19: 'IA',
    20: 'KS', 21: 'KY', 22: 'LA', 23: 'ME', 24: 'MD', 25: 'MA', 26: 'MI', 27: 'MN',
    28: 'MS', 29: 'MO', 30: 'MT', 31: 'NE', 32: 'NV', 33: 'NH', 34: 'NJ', 35: 'NM',
    36: 'NY', 37: 'NC', 38: 'ND', 39: 'OH', 40: 'OK', 41: 'OR', 42: 'PA', 44: 'RI',
    45: 'SC', 46: 'SD', 47: 'TN', 48: 'TX', 49: 'UT', 50: 'VT', 51: 'VA', 53: 'WA',
    54: 'WV', 55: 'WI', 56: 'WY'
}


# Streamlit layout
st.set_page_config(layout="wide")

st.sidebar.header("Filters")
start_date = st.sidebar.date_input(
    "Start Date",
    map_data['DATETIME'].min().date(),
    min_value=map_data['DATETIME'].min().date(),
    max_value=map_data['DATETIME'].max().date()
)
end_date = st.sidebar.date_input(
    "End Date",
    map_data['DATETIME'].max().date(),
    min_value=map_data['DATETIME'].min().date(),
    max_value=map_data['DATETIME'].max().date()
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
        ),
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
    )

    # Display the map
    st.plotly_chart(map_fig, use_container_width=True)