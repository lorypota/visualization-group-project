import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import numpy as np
# Load environment variables
load_dotenv()
MAPBOX_ACCESS_TOKEN = os.getenv('MAPBOX_TOKEN')

# Mapbox styles
DEFAULT_STYLE = "mapbox://styles/mapbox/streets-v12"
STYLE = "mapbox://styles/mggiordano/cm4iq6416000601s89eyagmeu" # currently not used

# File paths
DATA_PATH = 'Railroad_Incidents/CleanedDataset.csv'

# Map configurations
MAP_CONFIGS = {
    "Continental USA": {
        "center_coords": {"lat": 39.8, "lon": -98.6},
        "zoom_level": 3.5
    },
    'bounding_boxes': {
        "lat": [21, 52],  # Min and max latitudes
        "lon": [-150.0, -40]    # Min and max longitudes
    }
}

# State codes
STATE_CODES = {
    1: 'AL', 2: 'AK', 4: 'AZ', 5: 'AR', 6: 'CA', 8: 'CO', 9: 'CT', 10: 'DE',
    11: 'DC', 12: 'FL', 13: 'GA', 15: 'HI', 16: 'ID', 17: 'IL', 18: 'IN', 19: 'IA',
    20: 'KS', 21: 'KY', 22: 'LA', 23: 'ME', 24: 'MD', 25: 'MA', 26: 'MI', 27: 'MN',
    28: 'MS', 29: 'MO', 30: 'MT', 31: 'NE', 32: 'NV', 33: 'NH', 34: 'NJ', 35: 'NM',
    36: 'NY', 37: 'NC', 38: 'ND', 39: 'OH', 40: 'OK', 41: 'OR', 42: 'PA', 44: 'RI',
    45: 'SC', 46: 'SD', 47: 'TN', 48: 'TX', 49: 'UT', 50: 'VT', 51: 'VA', 53: 'WA',
    54: 'WV', 55: 'WI', 56: 'WY'
}

# Type descriptions
TYPE_DESCRIPTIONS = {
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

VIS_DESCRIPTIONS = {
    '1': 'Dawn',
    '2': 'Day',
    '3': 'Dusk',
    '4': 'Dark'
}

WEATHER_DESCRIPTIONS = {
    '1': 'Clear',
    '2': 'Cloudy',
    '3': 'Rain',
    '4': 'Fog',
    '5': 'Sleet',
    '6': 'Snow'
}

TRACK_DESCRIPTIONS = {
    '1': 'Main',
    '2': 'Yard',
    '3': 'Siding',
    '4': 'Industry',
}



INJURED_BUCKETS = [
    0,
    5,
    10,
    20,
    50,
    75,
    100,
    "100+"
]


INJURED_BUCKETS2 = {
    "0": lambda x: x == 0,
    "1-5": lambda x: (x > 0) & (x < 6),
    "6-10": lambda x: (x > 5) & (x < 11),
    "11-20": lambda x: (x > 10) & (x < 21),
    "21-50": lambda x: (x > 20) & (x < 51),
    "51-75": lambda x: (x > 50) & (x < 76),
    "76-99": lambda x: (x > 75) & (x < 100),
    "100+": lambda x: x > 99
}

COSTS_BUCKETS = [
    "0",
    "0.25 million",
    "0.5 million",
    "1 million",
    "2 million",
    "5 million",
    "10 million",
    "20 million",
    "20+ million"
]

VARIABLES = {
    "💥 Incident Type": ["Number of Accidents", "🗓️ Year", "🚄 Speed", "💸 Total Damage Costs", "Total People Injured", "Total People Killed"],
    "🌥️ Weather": ["Number of Accidents", "🗓️ Year", "🚄 Speed", "💸 Total Damage Costs", "Total People Injured", "Total People Killed"],
    "🌫️ Visibility": ["Number of Accidents", "🗓️ Year", "🚄 Speed", "💸 Total Damage Costs", "Total People Injured", "Total People Killed"],
    "🚊 Track Type": ["Number of Accidents", "🗓️ Year", "🚄 Speed", "💸 Total Damage Costs", "Total People Injured", "Total People Killed"],
    "🗓️ Year": ["Number of Accidents", "💥 Incident Type", "🚄 Speed", "🌡️ Temperature", "🚊 Track Type", "🌥️ Weather", "🌫️ Visibility", "💸 Total Damage Costs", "Total People Injured", "Total People Killed"],
    "🌡️ Temperature": ["Number of Accidents", "💥 Incident Type", "🚄 Speed", "🗓️ Year", "🚊 Track Type", "🌥️ Weather", "🌫️ Visibility", "💸 Total Damage Costs", "Total People Injured", "Total People Killed"],
    "🚄 Speed": ["Number of Accidents", "💥 Incident Type", "🚄 Speed", "🗓️ Year", "🚊 Track Type", "🌥️ Weather", "🌫️ Visibility", "💸 Total Damage Costs", "Total People Injured", "Total People Killed"],
    "Total People Injured" : ["Number of Accidents", "💥 Incident Type", "🚄 Speed", "🌡️ Temperature", "Total People Killed", "🚊 Track Type", "🌥️ Weather", "🌫️ Visibility", "💸 Total Damage Costs"],
    "Total People Killed": ["Number of Accidents", "💥 Incident Type","🚄 Speed", "🌡️ Temperature", "Total People Injured", "🚊 Track Type", "🌥️ Weather", "🌫️ Visibility", "💸 Total Damage Costs"]
}

VARNAMES_TO_DATASET = {
    "Number of Accidents": "Number of Accidents" ,
    "🌥️ Weather": "WEATHER",
    "🌫️ Visibility": "VISIBLTY",
    "🚊 Track Type": "TYPTRK",
    "🗓️ Year": "YEAR",
    "🚄 Speed" : "TRNSPD",
    "🌡️ Temperature" : "TEMP",
    "🇺🇸 State": "STATE",
    "💥 Incident Type": "TYPE",
    "💸 Total Damage Costs": "ACCDMG",
    "Total People Killed": "TOTKLD",
    "Total People Injured": "TOTINJ"
}


DESCRIPTION_MAPPINGS = {
    "🌥️ Weather": WEATHER_DESCRIPTIONS,
    "🌫️ Visibility": VIS_DESCRIPTIONS,
    "🚊 Track Type": TRACK_DESCRIPTIONS,
    "💥 Incident Type": TYPE_DESCRIPTIONS,
}


def plot_bar_chart(data, categorical_var, numerical_var):
    cat_var_data = VARNAMES_TO_DATASET[categorical_var]
    num_var_data = VARNAMES_TO_DATASET[numerical_var]
    # Get axis labels
    unique_cat_var_labels = np.array(data[cat_var_data].unique(), dtype=int)
    cat_var_descriptions = DESCRIPTION_MAPPINGS[categorical_var]

    # Match unique labels with their descriptions
    selected_type_description = [
    description for code, description in cat_var_descriptions.items()
    if int(code) in unique_cat_var_labels
    ]   
        
    # Group the data by the categorical variable
    if num_var_data == "Number of Accidents":
        grouped_data = data.groupby(cat_var_data).size().reset_index(name='Counts')
    else:
        
        grouped_data = data.groupby(cat_var_data)[num_var_data].mean().reset_index()

    # Create a list of latitude and longitude for each category
    custom_data = []
    for category in grouped_data[cat_var_data]:
        category_data = data[data[cat_var_data] == category]
        lat_lon_pairs = list(zip(category_data['Latitude'], category_data['Longitude']))
        custom_data.append(lat_lon_pairs)
    
    
    # Create the bar chart
    fig = px.bar(
        grouped_data,
        x=selected_type_description,
        y='Counts' if num_var_data == "Number of Accidents" else num_var_data,
        title=f"{categorical_var} vs {numerical_var}",
        labels={cat_var_data: categorical_var, 'Counts': 'Number of Accidents' if num_var_data == "Number of Accidents" else num_var_data}
    )
    
    # Add custom data (latitude and longitude) to each bar
    fig.update_traces(customdata=custom_data)
    
    # Return the figure
    return fig


def plot_line_chart(data, x_var, y_var):
    x_var_data = VARNAMES_TO_DATASET[x_var]
    y_var_data = VARNAMES_TO_DATASET[y_var]
    
    if y_var_data == "Number of Accidents":
        grouped_data = data.groupby(x_var_data).size().reset_index(name='Counts')
        fig = px.line(
            grouped_data,
            x=x_var_data,
            y='Counts',
            title=f"{x_var} vs Number of Accidents",
            labels={x_var_data: x_var, 'Counts': 'Number of Accidents'}
        )
    else:
        grouped_data = data.groupby(x_var_data)[y_var_data].mean().reset_index()
        fig = px.line(
            grouped_data,
            x=x_var_data,
            y=y_var_data,
            title=f"{x_var} vs {y_var}",
            labels={x_var_data: x_var, y_var_data: y_var}
        )
    return fig


def plot_scatter(data, x_var, y_var):
    x_var_data = VARNAMES_TO_DATASET[x_var]
    y_var_data = VARNAMES_TO_DATASET[y_var]
    
    fig = px.scatter(
        data,
        x=x_var_data,
        y=y_var_data,
        title=f"{x_var} vs {y_var}",
        labels={x_var_data: x_var, y_var_data: y_var},
        opacity=0.7
    )
    return fig


# def plot_bubble(data, x_var, y_var):
#     x_var_data = VARNAMES_TO_DATASET[x_var]
#     y_var_data = VARNAMES_TO_DATASET[y_var]

#     data["speed_bin"] = pd.cut(data[x_var_data], bins=np.arange(0, 135, 20))  # Adjust bin range/size
#     data["temperature_bin"] = pd.cut(data[y_var_data], bins=np.arange(-30, 118, 10))  # Adjust bin range/size
    
#     binned_data = data.groupby(["speed_bin", "temperature_bin"]).size().reset_index(name="incident_count")
#     binned_data["speed_bin"] = binned_data["speed_bin"].astype(str)
#     binned_data["temperature_bin"] = binned_data["temperature_bin"].astype(str)
    
#     fig = px.scatter(
#         binned_data,
#         x="speed_bin",
#         y="temperature_bin",
#         size="incident_count",  
#         title="Bubble Plot: Discretized Speed vs Temperature vs Number of Incidents",
#         opacity=0.7,
#         color_continuous_scale=px.colors.sequential.Viridis,
#         labels={
#             "speed_bin": "Speed (Binned)",
#             "temperature_bin": "Temperature (Binned)",
#             "incident_count": "Number of Incidents"
#         }
#     )
#   return fig


def parallel_plot(data, x_var, y_var):
    x_var_data = VARNAMES_TO_DATASET[x_var]
    y_var_data = VARNAMES_TO_DATASET[y_var]

    # Quantize temperature and speed into 10 bins
    data["temperature_bin"] = pd.cut(data[x_var_data], bins=10, precision=1, duplicates="drop")
    data["speed_bin"] = pd.cut(data[y_var_data], bins=10, precision=1, duplicates="drop")

    # Map binned intervals to numeric values for compatibility with parallel coordinates
    data["temperature_bin_numeric"] = data["temperature_bin"].cat.codes
    data["speed_bin_numeric"] = data["speed_bin"].cat.codes

    # Parallel Coordinates Plot
    fig = px.parallel_coordinates(
        data,
        dimensions=[
            "temperature_bin_numeric",
            "speed_bin_numeric",
            VARNAMES_TO_DATASET["🌫️ Visibility"]
        ],  # Include the axes
        color=VARNAMES_TO_DATASET["🌫️ Visibility"],  # Use visibility for coloring
        color_continuous_scale=px.colors.sequential.Viridis,
        labels={
            "temperature_bin_numeric": "Temperature (Binned)",
            "speed_bin_numeric": "Speed (Binned)",
            VARNAMES_TO_DATASET["🌫️ Visibility"]: "Visibility (miles)",
        },
        title="Parallel Coordinates Plot: Temperature, Speed, Visibility"
    )

    return fig


PLOT_FUNCTIONS = { ("🌥️ Weather", "Number of Accidents"): plot_bar_chart, 
                  ("🌫️ Visibility", "Number of Accidents"): plot_bar_chart,
                  ("🚊 Track Type", "Number of Accidents"): plot_bar_chart,
                  ("💥 Incident Type", "Number of Accidents"): plot_bar_chart,
                  ("🗓️ Year", "Number of Accidents"): plot_line_chart,
                  ("🚄 Speed", "Number of Accidents"): plot_line_chart,
                  ("🌡️ Temperature", "Number of Accidents"): plot_line_chart,
                  ("Total People Killed", "Number of Accidents"): plot_line_chart, #NOT COMPLETELY CONTINUOUS 
                  ("Total People Injured", "Number of Accidents"): plot_line_chart, #NOT COMPLETELY CONTINUOUS
                  ("🗓️ Year", "🚄 Speed"): plot_scatter,
                  ("🗓️ Year", "💸 Total Damage Costs") : plot_scatter,
                  ("🗓️ Year", "Total People Killed") : plot_scatter,
                  ("🗓️ Year", "Total People Injured") : plot_scatter,
                  ("🗓️ Year", "🌡️ Temperature") : plot_scatter,
                  ("🚄 Speed", "💸 Total Damage Costs") : plot_scatter,
                  ("🚄 Speed", "Total People Killed") : plot_scatter,
                  ("🚄 Speed", "Total People Injured") : plot_scatter,  
                  ("🚄 Speed", "🌡️ Temperature") : plot_scatter,
                  ("💸 Total Damage Costs", "🚄 Speed") : plot_scatter,
                  ("💸 Total Damage Costs", "Total People Killed") : plot_scatter,
                  ("💸 Total Damage Costs", "Total People Injured") : plot_scatter,
                  ("💸 Total Damage Costs", "🌡️ Temperature") : plot_scatter,
                  ("Total People Killed", "💸 Total Damage Costs") : plot_scatter,
                  ("Total People Killed", "🚄 Speed") : plot_scatter,
                  ("Total People Killed", "Total People Injured") : plot_scatter,
                  ("Total People Killed", "🌡️ Temperature") : plot_scatter,
                  ("Total People Injured", "💸 Total Damage Costs") : plot_scatter,
                  ("Total People Injured", "🚄 Speed") : plot_scatter,
                  ("Total People Injured", "Total People Killed") : plot_scatter,
                  ("Total People Injured", "🌡️ Temperature") : plot_scatter,
                  ("🚊 Track Type", "🚄 Speed"): plot_bar_chart,
                  ("🌫️ Visibility", "🚄 Speed"): plot_bar_chart,
                  ("🌥️ Weather", "🚄 Speed"): plot_bar_chart,
                  ("💥 Incident Type", "🚄 Speed"): plot_bar_chart,
                  ("🚊 Track Type", "💸 Total Damage Costs"): plot_bar_chart,
                  ("🌫️ Visibility", "💸 Total Damage Costs" ): plot_bar_chart,
                  ("🌥️ Weather", "💸 Total Damage Costs"): plot_bar_chart,
                  ("💥 Incident Type", "💸 Total Damage Costs"): plot_bar_chart,
                  ("🚊 Track Type", "Total People Injured"): plot_bar_chart,
                  ("🌫️ Visibility", "Total People Injured"): plot_bar_chart,
                  ("🌥️ Weather", "Total People Injured"): plot_bar_chart,
                  ("💥 Incident Type", "Total People Injured"): plot_bar_chart,
                  ("🚊 Track Type", "Total People Killed"): plot_bar_chart,
                  ("🌫️ Visibility", "Total People Killed"): plot_bar_chart,
                  ("🌥️ Weather", "Total People Killed"): plot_bar_chart,
                  ("💥 Incident Type", "Total People Killed"): plot_bar_chart,
                  ("test"): parallel_plot,

}
