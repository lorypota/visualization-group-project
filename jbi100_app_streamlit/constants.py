import plotly.express as px
import numpy as np

def plot_line_chart(data, x_var, y_var):
    """
    Creates a line chart comparing an x-axis variable and a y-axis variable.
    :param data: (pd.DataFrame) The dataset containing the variables to be plotted.
    :param x_var: (str) The name of the variable to be plotted on the x-axis.
    :param y_var: (str) The name of the variable to be plotted on the y-axis.
    :return: A line chart visualizing the relationship between the x-axis and y-axis variables.        
    """
    x_var_data = VARNAMES_TO_DATASET[x_var]
    y_var_data = VARNAMES_TO_DATASET[y_var]

    if y_var_data == "🔢 Number of Accidents":
        grouped_data = data.groupby(
            x_var_data).size().reset_index(name='Counts')
        fig = px.line(
            grouped_data,
            x=x_var_data,
            y='Counts',
            title=f"{x_var} vs 🔢 Number of Accidents",
            markers=True,
            labels={x_var_data: x_var, 'Counts': '🔢 Number of Accidents'}
        )
    else:
        grouped_data = data.groupby(
            x_var_data)[y_var_data].mean().reset_index()
        fig = px.line(
            grouped_data,
            x=x_var_data,
            y=y_var_data,
            title=f"{x_var} vs {y_var}",
            markers=True,
            labels={x_var_data: x_var, y_var_data: y_var}
        )

    # Pass only metadata as customdata
    fig.update_traces(customdata=[[x_var, y_var]] * len(data))
    return fig


def plot_bar_chart(data, categorical_var, numerical_var):
    """
    Creates a bar chart comparing a categorical variable and a numerical variable.
    :param data: (pd.DataFrame) The dataset containing the variables to be plotted.
    :param categorical_var: (str) The name of the categorical variable to group data by.
    :param numerical_var: (str) The name of the numerical variable to aggregate data.
    :return: A bar chart showing the relationship between the categorical and numerical variables.
    """
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
    if num_var_data == "🔢 Number of Accidents":
        grouped_data = data.groupby(
            cat_var_data).size().reset_index(name='Counts')
    else:
        grouped_data = data.groupby(cat_var_data)[
            num_var_data].mean().reset_index()

    # Create the bar chart
    fig = px.bar(
        grouped_data,
        x=selected_type_description,
        y='Counts' if num_var_data == "🔢 Number of Accidents" else num_var_data,
        title=f"{categorical_var} vs {numerical_var}",
        labels={cat_var_data: categorical_var, 'Counts': '🔢 Number of Accidents' if num_var_data ==
                "🔢 Number of Accidents" else num_var_data}
    )

    # Add custom data (latitude and longitude) to each bar
    fig.update_traces(
        customdata=[[categorical_var, numerical_var]] * len(data))

    # Return the figure
    return fig


def plot_scatter(data, x_var, y_var):
    """
    Creates a scatter plot showing the relationship between two variables.
    :param data: (pd.DataFrame) The dataset containing the variables to be plotted.
    :param x_var: (str) The name of the variable to be plotted on the x-axis.
    :param y_var: (str) The name of the variable to be plotted on the y-axis.
    :return: A scatter plot visualizing the relationship between the x-axis and y-axis variables.
    """
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

    # Pass only metadata as customdata
    fig.update_traces(customdata=[[x_var, y_var]] * len(data))
    return fig


def plot_year_month_heatmap(data, x_var, y_var):
    df = data.copy()
    df['YEAR'] = df['DATETIME'].dt.year
    df['MONTH'] = df['DATETIME'].dt.month
    grouped = df.groupby(['YEAR', 'MONTH']).size().reset_index(name='counts')
    pivoted = grouped.pivot(index='YEAR', columns='MONTH',
                            values='counts').fillna(0)

    fig = px.imshow(
        pivoted,
        labels={'x': 'Month', 'y': 'Year', 'color': 'Incidents'},
        x=pivoted.columns,
        y=pivoted.index,
        color_continuous_scale='Blues',
        aspect='auto'
    )
    fig.update_layout(title='Year-Month Heatmap of Incidents')
    return fig


STATE_CODES = {
    1: 'AL', 2: 'AK', 4: 'AZ', 5: 'AR', 6: 'CA', 8: 'CO', 9: 'CT', 10: 'DE',
    11: 'DC', 12: 'FL', 13: 'GA', 15: 'HI', 16: 'ID', 17: 'IL', 18: 'IN', 19: 'IA',
    20: 'KS', 21: 'KY', 22: 'LA', 23: 'ME', 24: 'MD', 25: 'MA', 26: 'MI', 27: 'MN',
    28: 'MS', 29: 'MO', 30: 'MT', 31: 'NE', 32: 'NV', 33: 'NH', 34: 'NJ', 35: 'NM',
    36: 'NY', 37: 'NC', 38: 'ND', 39: 'OH', 40: 'OK', 41: 'OR', 42: 'PA', 44: 'RI',
    45: 'SC', 46: 'SD', 47: 'TN', 48: 'TX', 49: 'UT', 50: 'VT', 51: 'VA', 53: 'WA',
    54: 'WV', 55: 'WI', 56: 'WY'
}

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

# Variables and their corresponding related variables for plots
VARIABLES = {
    "💥 Incident Type": ["🔢 Number of Accidents", "🗓️ Date", "🚄 Speed", "💸 Total Damage Costs", "🤕 Total People Injured", "🪦 Total People Killed"],
    "🌥️ Weather": ["🔢 Number of Accidents", "🗓️ Date", "🚄 Speed", "💸 Total Damage Costs", "🤕 Total People Injured", "🪦 Total People Killed"],
    "🌫️ Visibility": ["🔢 Number of Accidents", "🗓️ Date", "🚄 Speed", "💸 Total Damage Costs", "🤕 Total People Injured", "🪦 Total People Killed"],
    "🚊 Track Type": ["🔢 Number of Accidents", "🗓️ Date", "🚄 Speed", "💸 Total Damage Costs", "🤕 Total People Injured", "🪦 Total People Killed"],
    "🗓️ Date": ["🔢 Number of Accidents", "💥 Incident Type", "🚄 Speed", "🌡️ Temperature", "🚊 Track Type", "🌥️ Weather", "🌫️ Visibility", "💸 Total Damage Costs", "🤕 Total People Injured", "🪦 Total People Killed"],
    "🌡️ Temperature": ["🔢 Number of Accidents", "💥 Incident Type", "🚄 Speed", "🗓️ Date", "🚊 Track Type", "🌥️ Weather", "🌫️ Visibility", "💸 Total Damage Costs", "🤕 Total People Injured", "🪦 Total People Killed"],
    "🚄 Speed": ["🔢 Number of Accidents", "💥 Incident Type", "🚄 Speed", "🗓️ Date", "🚊 Track Type", "🌥️ Weather", "🌫️ Visibility", "💸 Total Damage Costs", "🤕 Total People Injured", "🪦 Total People Killed"],
    "🤕 Total People Injured": ["🔢 Number of Accidents", "💥 Incident Type", "🚄 Speed", "🌡️ Temperature", "🪦 Total People Killed", "🚊 Track Type", "🌥️ Weather", "🌫️ Visibility", "💸 Total Damage Costs"],
    "🪦 Total People Killed": ["🔢 Number of Accidents", "💥 Incident Type", "🚄 Speed", "🌡️ Temperature", "🤕 Total People Injured", "🚊 Track Type", "🌥️ Weather", "🌫️ Visibility", "💸 Total Damage Costs"]
}

# Maps the selected variable combination to the corresponding plot function
PLOT_FUNCTIONS = {
    ("🌥️ Weather", "🔢 Number of Accidents"): plot_bar_chart,
    ("🌫️ Visibility", "🔢 Number of Accidents"): plot_bar_chart,
    ("🚊 Track Type", "🔢 Number of Accidents"): plot_bar_chart,
    ("💥 Incident Type", "🔢 Number of Accidents"): plot_bar_chart,
    ("🗓️ Date", "🔢 Number of Accidents"): plot_year_month_heatmap,
    ("🚄 Speed", "🔢 Number of Accidents"): plot_line_chart,
    ("🌡️ Temperature", "🔢 Number of Accidents"): plot_line_chart,
    # NOT COMPLETELY CONTINUOUS
    ("� Total People Killed", "🔢 Number of Accidents"): plot_line_chart,
    # NOT COMPLETELY CONTINUOUS
    ("🤕 Total People Injured", "🔢 Number of Accidents"): plot_line_chart,
    ("🗓️ Date", "🚄 Speed"): plot_scatter,
    ("🗓️ Date", "💸 Total Damage Costs"): plot_scatter,
    ("🗓️ Date", "🪦 Total People Killed"): plot_scatter,
    ("🗓️ Date", "🤕 Total People Injured"): plot_scatter,
    ("🗓️ Date", "🌡️ Temperature"): plot_scatter,
    ("🚄 Speed", "💸 Total Damage Costs"): plot_scatter,
    ("🚄 Speed", "🪦 Total People Killed"): plot_scatter,
    ("🚄 Speed", "🤕 Total People Injured"): plot_scatter,
    ("🚄 Speed", "🌡️ Temperature"): plot_scatter,
    ("💸 Total Damage Costs", "🚄 Speed"): plot_scatter,
    ("💸 Total Damage Costs", "🪦 Total People Killed"): plot_scatter,
    ("💸 Total Damage Costs", "🤕 Total People Injured"): plot_scatter,
    ("💸 Total Damage Costs", "🌡️ Temperature"): plot_scatter,
    ("🪦 Total People Killed", "💸 Total Damage Costs"): plot_scatter,
    ("🪦 Total People Killed", "🚄 Speed"): plot_scatter,
    ("🪦 Total People Killed", "🤕 Total People Injured"): plot_scatter,
    ("🪦 Total People Killed", "🌡️ Temperature"): plot_scatter,
    ("🤕 Total People Injured", "💸 Total Damage Costs"): plot_scatter,
    ("🤕 Total People Injured", "🚄 Speed"): plot_scatter,
    ("🤕 Total People Injured", "🪦 Total People Killed"): plot_scatter,
    ("🤕 Total People Injured", "🌡️ Temperature"): plot_scatter,
    ("🚊 Track Type", "🚄 Speed"): plot_bar_chart,
    ("🌫️ Visibility", "🚄 Speed"): plot_bar_chart,
    ("🌥️ Weather", "🚄 Speed"): plot_bar_chart,
    ("💥 Incident Type", "🚄 Speed"): plot_bar_chart,
    ("🚊 Track Type", "💸 Total Damage Costs"): plot_bar_chart,
    ("🌫️ Visibility", "💸 Total Damage Costs"): plot_bar_chart,
    ("🌥️ Weather", "💸 Total Damage Costs"): plot_bar_chart,
    ("💥 Incident Type", "💸 Total Damage Costs"): plot_bar_chart,
    ("🚊 Track Type", "🤕 Total People Injured"): plot_bar_chart,
    ("🌫️ Visibility", "🤕 Total People Injured"): plot_bar_chart,
    ("🌥️ Weather", "🤕 Total People Injured"): plot_bar_chart,
    ("💥 Incident Type", "🤕 Total People Injured"): plot_bar_chart,
    ("🚊 Track Type", "🪦 Total People Killed"): plot_bar_chart,
    ("🌫️ Visibility", "🪦 Total People Killed"): plot_bar_chart,
    ("🌥️ Weather", "🪦 Total People Killed"): plot_bar_chart,
    ("💥 Incident Type", "🪦 Total People Killed"): plot_bar_chart
}

# Maps variable names to dataset column names
VARNAMES_TO_DATASET = {
    "🔢 Number of Accidents": "🔢 Number of Accidents",
    "🌥️ Weather": "WEATHER",
    "🌫️ Visibility": "VISIBLTY",
    "🚊 Track Type": "TYPTRK",
    "🛤️ Track Class": "TRKCLAS",
    "🗓️ Date": "DATETIME",
    "🚄 Speed": "TRNSPD",
    "🌡️ Temperature": "TEMP",
    "🇺🇸 State": "STATE",
    "💥 Incident Type": "TYPE",
    "💸 Total Damage Costs": "ACCDMG",
    "🪦 Total People Killed": "TOTKLD",
    "🤕 Total People Injured": "TOTINJ",
    "🪨 Weight": "TONS",
    "🍷 Alcohol": "ALCOHOL",
    "💉 Drugs": "DRUG"
}

# Description mappings for variables with specific codes
DESCRIPTION_MAPPINGS = {
    "🌥️ Weather": WEATHER_DESCRIPTIONS,
    "🌫️ Visibility": VIS_DESCRIPTIONS,
    "🚊 Track Type": TRACK_DESCRIPTIONS,
    "💥 Incident Type": TYPE_DESCRIPTIONS,
}
