import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os
from streamlit_plotly_events import plotly_events


class ChoroplethMap:
    def __init__(self, df):
        self.df = df
        self.state_codes = {
            1: 'AL', 2: 'AK', 4: 'AZ', 5: 'AR', 6: 'CA', 8: 'CO', 9: 'CT', 10: 'DE',
            11: 'DC', 12: 'FL', 13: 'GA', 15: 'HI', 16: 'ID', 17: 'IL', 18: 'IN', 19: 'IA',
            20: 'KS', 21: 'KY', 22: 'LA', 23: 'ME', 24: 'MD', 25: 'MA', 26: 'MI', 27: 'MN',
            28: 'MS', 29: 'MO', 30: 'MT', 31: 'NE', 32: 'NV', 33: 'NH', 34: 'NJ', 35: 'NM',
            36: 'NY', 37: 'NC', 38: 'ND', 39: 'OH', 40: 'OK', 41: 'OR', 42: 'PA', 44: 'RI',
            45: 'SC', 46: 'SD', 47: 'TN', 48: 'TX', 49: 'UT', 50: 'VT', 51: 'VA', 53: 'WA',
            54: 'WV', 55: 'WI', 56: 'WY'
        }

    def get_figure(self):
        # base choropleth layer
        state_counts = self.df.groupby(
            ['STATE']).size().reset_index(name='count')
        state_counts['STATE'] = state_counts['STATE'].map(self.state_codes)

        fig = go.Figure()

        # Add choropleth layer
        fig.add_trace(go.Choropleth(
            locations=state_counts['STATE'],
            z=state_counts['count'],
            locationmode="USA-states",
            colorscale="YlOrRd",
            zmin=state_counts['count'].min(),
            zmax=state_counts['count'].max(),
            name="State Incidents",
            colorbar_title="Number of Incidents"
        ))

        # Add scatter points for individual incidents
        fig.add_trace(go.Scattergeo(
            lon=self.df['Longitude'],
            lat=self.df['Latitude'],
            mode='markers',
            marker=dict(
                size=4,
                color='blue',
                opacity=0.6
            ),
            name="Incident Locations",
            hovertext=self.df.apply(
                lambda row: f"State: {self.state_codes.get(
                    row['STATE'], 'Unknown')}<br>"
                f"Date: {row.get('DATE', 'Unknown')}<br>"
                f"Location: ({row['Latitude']:.2f}, {row['Longitude']:.2f})",
                axis=1
            ),
            hoverinfo="text"
        ))

        # Update layout
        fig.update_layout(
            height=600,
            margin={"r": 20, "t": 30, "l": 20, "b": 20},
            geo=dict(
                scope='usa',
                projection=dict(type='albers usa'),
                showlakes=True,
                lakecolor='rgb(255, 255, 255)',
                showland=True,
                landcolor='rgb(240, 240, 240)',
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='black'),
            legend=dict(
                x=0,
                y=1,
                bgcolor='rgba(255, 255, 255, 0.7)'
            )
        )

        return fig


def main():
    st.set_page_config(layout="wide")

    # Import railroad data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(
        current_dir, 'Railroad_Incidents', 'CleanedDataset.csv')
    df_railroad = pd.read_csv(data_path, delimiter=',', low_memory=False)

    # Sidebar (Menu)
    st.sidebar.title("Example Dashboard")
    st.sidebar.write("JBI100 visualization project")


    # Main content
    # Choropleth Map with Points
    choropleth = ChoroplethMap(df_railroad)
    st.subheader("Railroad Incidents by State with Location Points")
    st.plotly_chart(choropleth.get_figure(), use_container_width=True)

    # Create the bottom panel
    st.divider()  # Optional visual separator
    st.subheader("Bottom Panel: Graphs and Meta-Information")
    
    # bottom_col1, bottom_col2 = st.columns([1, 2])  # Split the bottom panel into two columns
    st.markdown("### Additional Graphs")
    st.write("Bar Chart of Incidents per State")
    bar_chart_data = df_railroad.groupby('STATE').size().reset_index(name='Count')
    state_codes = ChoroplethMap(df_railroad).state_codes
    bar_chart_data['STATE'] = bar_chart_data['STATE'].map(state_codes)

    fig_bar = px.bar(
        bar_chart_data,
        x='STATE',
        y='Count',
        title="Incidents per State",
        labels={'STATE': 'State', 'Count': 'Number of Incidents'},
    )
    st.plotly_chart(fig_bar, use_container_width=True)
if __name__ == '__main__':
    main()
