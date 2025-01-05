import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import plotly.express as px

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

VARIABLES = {
    "Incident Type": ["Number of Accidents", "Year", "Speed", "Total Damage Costs"],
    "Weather": ["Number of Accidents", "Year", "Speed", "Total Damage Costs"],
    "Visibility": ["Number of Accidents", "Year", "Speed", "Total Damage Costs"],
    "Track Type": ["Number of Accidents", "Year", "Speed", "Total Damage Costs"],
    "Year": ["Number of Accidents", "Incident Type", "Speed", "Temperature", "Track Type", "Weather", "Visibility", "Total Damage Costs"],
    "Temperature": ["Number of Accidents", "Incident Type", "Speed", "Year", "Track Type", "Weather", "Visibility", "Total Damage Costs"],
    "Speed": ["Number of Accidents", "Incident Type", "Speed", "Year", "Track Type", "Weather", "Visibility", "Total Damage Costs"],
    
}

VARNAMES_TO_DATASET = {
    "Number of Accidents": "Number of Accidents" ,
    "Weather": "WEATHER",
    "Visibility": "VISIBLTY",
    "Track Type": "TYPTRK",
    "Year": "YEAR",
    "Speed" : "TRNSPD",
    "Temperature" : "TEMP",
    "State": "STATE",
    "Incident Type": "TYPE",
    "Total Damage Costs": "ACCDMG"
}


def plot_bar_chart(data, categorical_var, numerical_var):
    cat_var_data = VARNAMES_TO_DATASET[categorical_var]
    num_var_data = VARNAMES_TO_DATASET[numerical_var]
    
    if num_var_data == "Number of Accidents":
        grouped_data = data.groupby(cat_var_data).size().reset_index(name='Counts')
        fig = px.bar(
            grouped_data,
            x=cat_var_data,
            y='Counts',
            title=f"{categorical_var} vs Number of Accidents",
            labels={cat_var_data: categorical_var, 'Counts': 'Number of Accidents'}
        )
    else:
        grouped_data = data.groupby(cat_var_data)[num_var_data].mean().reset_index()
        fig = px.bar(
            grouped_data,
            x=cat_var_data,
            y=num_var_data,
            title=f"{categorical_var} vs {numerical_var}",
            labels={cat_var_data: categorical_var, num_var_data: numerical_var}
        )
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



PLOT_FUNCTIONS = { ("Weather", "Number of Accidents"): plot_bar_chart, 
                  ("Visibility", "Number of Accidents"): plot_bar_chart,
                  ("Track Type", "Number of Accidents"): plot_bar_chart,
                  ("Incident Type", "Number of Accidents"): plot_bar_chart,
                  ("Year", "Number of Accidents"): plot_line_chart,
                  ("Speed", "Number of Accidents"): plot_line_chart,
                  ("Temperature", "Number of Accidents"): plot_line_chart,
                  ("Year", "Speed"): plot_scatter,
                  ("Year", "Total Damage Costs") : plot_scatter,
                  ("Speed", "Total Damage Costs") : plot_scatter,
                  ("Track Type", "Speed"): plot_bar_chart,
                  ("Visibility", "Speed"): plot_bar_chart,
                  ("Weather", "Speed"): plot_bar_chart,
                  ("Incident Type", "Speed"): plot_bar_chart,
                  ("Track Type", "Total Damage Costs"): plot_bar_chart,
                  ("Visibility", "Total Damage Costs" ): plot_bar_chart,
                  ("Weather", "Total Damage Costs"): plot_bar_chart,
                  ("Incident Type", "Total Damage Costs"): plot_bar_chart

}
