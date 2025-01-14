import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from constants import VARNAMES_TO_DATASET, WEATHER_DESCRIPTIONS, VIS_DESCRIPTIONS
import pandas as pd
import plotly.graph_objects as go


def plot_bar_graph(data):
    # Prepare the data for plotting
    bar_data = data['TYPE'].value_counts().reset_index()
    bar_data.columns = ['Incident Type', 'Count']  # Rename columns for clarity

    # Create the bar plot
    fig = px.bar(
        bar_data,
        x='Incident Type',
        y='Count',
        labels={'Incident Type': 'Incident Type', 'Count': 'Count'},
        title='Incident Type Distribution'
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_scatter_plot(data):
    # Prepare the data for the scatter plot
    fig = px.scatter(
        data,
        x='STATE',
        y='TYPE',
        title='Incident Type by State (Scatter Plot)',
        labels={'STATE': 'State', 'TYPE': 'Incident Type'},
        hover_data=['STATE', 'TYPE']
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_timeseries(data):
    # Prepare the data for the time series plot
    time_series = data.groupby(data['DATETIME'].dt.date)[
        'TYPE'].count().reset_index()
    # Rename columns for clarity
    time_series.columns = ['Date', 'Incident Count']

    # Create the interactive time series plot
    fig = px.line(
        time_series,
        x='Date',
        y='Incident Count',
        title='Incident Count Over Time',
        labels={'Date': 'Date', 'Incident Count': 'Count'}
    )
    st.plotly_chart(fig, use_container_width=True)


def make_bins(var, data, dims, labs, binning):
    """
    Creates bins for a specified variable and updates the dimensions for a parallel plot.
    :param var: (str) The name of the variable to be binned.
    :param data: (pd.DataFrame) The dataset containing the variable.
    :param dims: (list) The list of dimensions to update for the parallel plot.
    :param labs: (dict) A dictionary to store labels for the parallel plot.
    :param binning: (bool) A flag indicating whether to apply binning or use raw values.
    :return: The name of the numeric column created for the binned variable or None if no numeric column was created.
    """
    if var in ["🌡️ Temperature", "🚄 Speed", "💸 Total Damage Costs", "🪨 Weight"]:
        # Define bin names and units
        non_negative = False
        if var == "🌡️ Temperature":
            name = "temperature_bin"
            unit = "°F"
        elif var == "🚄 Speed":
            name = "speed_bin"
            unit = "mph"
            non_negative = True
        elif var == "💸 Total Damage Costs":
            name = "costs_bin"
            unit = "$"
            non_negative = True
        elif var == "🪨 Weight":
            name = "weight_bin"
            unit = "tons"
            non_negative = True

        name_numeric = name + "_numeric"
        labs[name_numeric] = var

        # Create bins for the variable
        var_column = VARNAMES_TO_DATASET[var]
        data[name] = pd.cut(data[var_column], bins=10,
                            precision=1, duplicates="drop")
        data[name_numeric] = data[name].cat.codes

        # Adjust tick labels for non-negative variables to remove negative ranges
        if non_negative:
            ticktext = [str(interval)
                        for interval in data[name].cat.categories]
            tokens = ticktext[0].split(",")
            tokens[0] = "(0.0"
            new_interval = ",".join(tokens)
            ticktext[0] = new_interval
        else:
            ticktext = [str(interval)
                        for interval in data[name].cat.categories]

        # Add dimension to the parallel coordinates plot
        if binning:
            dims.append({
                "label": f"{var} ({unit})",
                "values": data[name_numeric],
                "tickvals": list(range(len(data[name].cat.categories))),
                "ticktext": ticktext
            })
        else:
            dims.append({
                "label": f"{var} ({unit})",
                "values": data[var_column]
            })

        return name_numeric
    else:
        # For non-binned categorical variables
        labs[VARNAMES_TO_DATASET[var]] = var
        var_column = VARNAMES_TO_DATASET[var]

        # Add specific formatting for certain categorical variables
        if var == "🍷 Alcohol":
            dims.append({
                "label": f"{var} (# of positive tests)",
                "values": data[var_column],
                "tickvals": [-1, 0, 1],
                "ticktext": ["No data", "0", "1"]
            })
        elif var == "💉 Drugs":
            dims.append({
                "label": f"{var} (# of positive tests)",
                "values": data[var_column],
                "tickvals": [-1, 0, 1, 2, 3],
                "ticktext": ["No data", "0", "1", "2", "3"]
            })
        elif var == "🚊 Track Type":
            dims.append({
                "label": var,
                "values": data[var_column],
                "tickvals": [1, 2, 3, 4],
                "ticktext": ["Main", "Yard", "Siding", "Industry"]
            })
        elif var == "🌥️ Weather":
            dims.append({
                "label": var,
                "values": data[var_column],
                "tickvals": list(WEATHER_DESCRIPTIONS.keys()),
                "ticktext": list(WEATHER_DESCRIPTIONS.values())
            })
        elif var == "🌫️ Visibility":
            dims.append({
                "label": var,
                "values": data[var_column],
                "tickvals": list(VIS_DESCRIPTIONS.keys()),
                "ticktext": list(VIS_DESCRIPTIONS.values())
            })
        else:
            dims.append({
                "label": var,
                "values": data[var_column]
            })
        return None


def parallel_plot(data, selected_vars, binning):
    """
    Create a parallel coordinates plot based on the selected variables.
    :param data: The dataset to use for the plot
    :param selected_vars: The selected variables to plot
    :param binning: Whether to bin the continuous variables
    :return: The parallel coordinates plot
    """
    dims = []
    labs = {}

    # Process each selected variable: create bins for continuous variables and add dimensions
    for var in selected_vars:
        if var != "-- empty --":
            make_bins(var, data, dims, labs, binning)

    # Determine the first variable for coloring
    if selected_vars and selected_vars[0] != "-- empty --":
        first_var = selected_vars[0]
        # Map the variable to the dataset column
        color_column = VARNAMES_TO_DATASET[first_var]
    else:
        color_column = None

    # Create the parallel coordinates plot
    fig = go.Figure(data=go.Parcoords(
        line=dict(
            color=data[color_column] if color_column else [0] *
            len(data),  # Default to black if no variable
            colorscale="Viridis",
            showscale=True,  # Show the color bar
            cmin=data[color_column].min() if color_column else 0,
            cmax=data[color_column].max() if color_column else 1,
            colorbar=dict(
                title=f"{first_var} (Scale)",  # Dynamic colorbar title
                tickfont=dict(size=12, color="black"),
                titlefont=dict(size=14, color="black")
            )
        ),
        dimensions=dims,
        labelfont=dict(size=14, color="black"),
        tickfont=dict(size=12, color="black")
    ))

    fig.update_layout(margin=dict(l=100, r=50, t=50, b=50))
    return fig