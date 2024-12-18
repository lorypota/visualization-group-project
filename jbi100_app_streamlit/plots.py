import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

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
    time_series = data.groupby(data['DATETIME'].dt.date)['TYPE'].count().reset_index()
    time_series.columns = ['Date', 'Incident Count']  # Rename columns for clarity

    # Create the interactive time series plot
    fig = px.line(
        time_series,
        x='Date',
        y='Incident Count',
        title='Incident Count Over Time',
        labels={'Date': 'Date', 'Incident Count': 'Count'}
    )
    st.plotly_chart(fig, use_container_width=True)

