import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def plot_bar_graph(data):
    # Example bar graph
    fig, ax = plt.subplots()
    data['TYPE'].value_counts().plot(kind='bar', ax=ax)
    ax.set_title('Incident Type Distribution')
    st.pyplot(fig)


def plot_scatter_plot(data):
    # Example scatter plot
    fig, ax = plt.subplots()
    sns.scatterplot(x='STATE', y='TYPE', data=data, ax=ax)
    ax.set_title('Incident Type by State (Scatter Plot)')
    ax.set_xlabel('State')
    ax.set_ylabel('Incident Type')
    st.pyplot(fig)


def plot_timeseries(data):
    # Example timeseries plot
    fig, ax = plt.subplots()
    data.groupby(data['DATETIME'].dt.date)['TYPE'].count().plot(kind='line', ax=ax)
    ax.set_title('Incident Count Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Incident Count')
    st.pyplot(fig)
