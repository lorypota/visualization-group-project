import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os
from streamlit_plotly_events import plotly_events
import numpy as np


class ChoroplethMap:
    def __init__(self, df):
        self.df = df

        # STATE
        self.state_codes = {
            1: 'AL', 2: 'AK', 4: 'AZ', 5: 'AR', 6: 'CA', 8: 'CO', 9: 'CT', 10: 'DE',
            11: 'DC', 12: 'FL', 13: 'GA', 15: 'HI', 16: 'ID', 17: 'IL', 18: 'IN', 19: 'IA',
            20: 'KS', 21: 'KY', 22: 'LA', 23: 'ME', 24: 'MD', 25: 'MA', 26: 'MI', 27: 'MN',
            28: 'MS', 29: 'MO', 30: 'MT', 31: 'NE', 32: 'NV', 33: 'NH', 34: 'NJ', 35: 'NM',
            36: 'NY', 37: 'NC', 38: 'ND', 39: 'OH', 40: 'OK', 41: 'OR', 42: 'PA', 44: 'RI',
            45: 'SC', 46: 'SD', 47: 'TN', 48: 'TX', 49: 'UT', 50: 'VT', 51: 'VA', 53: 'WA',
            54: 'WV', 55: 'WI', 56: 'WY'
        }

        # TYPE
        self.type_colors = px.colors.qualitative.Set3
        self.type_descriptions = {
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

    def get_figure(self):
        # base choropleth layer
        state_counts = self.df.groupby(['STATE']).size().reset_index(name='count')
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

        # Get unique incident types and assign colors
        incident_types = [t for t in self.df['TYPE'].unique() if pd.notnull(t)]  # Filter out nan
        incident_types.sort()  # Sort to ensure consistent color assignment
        color_dict = {}
        for idx, inc_type in enumerate(incident_types):
            color_dict[float(inc_type)] = self.type_colors[idx % len(self.type_colors)]
        # Add a color for Unknown/NaN values
        color_dict[np.nan] = self.type_colors[-1]  # Use last color for Unknown



        # Add scatter points for each incident type
        for incident_type in self.df['TYPE'].unique():  # Include all types including NaN
            mask = self.df['TYPE'] == incident_type
            df_type = self.df[mask]
            
            if pd.isna(incident_type):
                display_name = "Unknown"
                color = color_dict[np.nan]
            else:
                display_name = f"Type {int(incident_type)}: {self.type_descriptions.get(f'{int(incident_type):02d}', 'Unknown')}"
                color = color_dict[float(incident_type)]

            fig.add_trace(go.Scattergeo(
                lon=df_type['Longitud'],
                lat=df_type['Latitude'],
                mode='markers',
                marker=dict(
                    size=3,
                    opacity=0.8,
                    symbol='circle',
                    color=color
                ),
                name=display_name,
                hovertext=df_type.apply(
                    lambda row: f"Type: {self.type_descriptions.get(f'{int(row.TYPE):02d}', 'Unknown') if pd.notnull(row.TYPE) else 'Unknown'}<br>"
                    f"State: {self.state_codes.get(row['STATE'], 'Unknown')}<br>"
                    f"Date: {row.get('DATE', 'Unknown')}<br>"
                    f"Location: ({row['Latitude']:.2f}, {row['Longitud']:.2f})",
                    axis=1
                ),
                hoverinfo="text",
                showlegend=True
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
                bgcolor='rgba(255, 255, 255, 0.7)',
                bordercolor='rgba(0,0,0,0.2)',
                borderwidth=1
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

    print("Unique TYPE values:", df_railroad['TYPE'].unique())
    print("TYPE column dtype:", df_railroad['TYPE'].dtype)

    # Sidebar (Menu)
    st.sidebar.title("Example Dashboard")
    st.sidebar.write("JBI100 visualization project")

    # Main content
    # Choropleth Map with Points
    choropleth = ChoroplethMap(df_railroad)
    st.subheader("Railroad Incidents by State with Location Points")
    st.plotly_chart(choropleth.get_figure(), use_container_width=True)


if __name__ == '__main__':
    main()
