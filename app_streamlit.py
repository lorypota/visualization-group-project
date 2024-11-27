import streamlit as st
import plotly.express as px
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
        # Count records per state and convert state codes to abbreviations
        state_counts = self.df.groupby(
            ['STATE']).size().reset_index(name='count')
        state_counts['STATE'] = state_counts['STATE'].map(self.state_codes)

        fig = px.choropleth(
            state_counts,
            locations='STATE',
            locationmode="USA-states",
            color='count',
            scope="usa",
            color_continuous_scale="YlOrRd",
            range_color=[state_counts['count'].min(
            ), state_counts['count'].max()],
        )

        fig.update_layout(
            height=600,
            margin={"r": 20, "t": 30, "l": 20, "b": 20},
            coloraxis_colorbar_title="Number of Incidents",
            geo=dict(
                scope='usa',
                projection=dict(type='albers usa'),
                showlakes=True,
                lakecolor='rgb(255, 255, 255)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='black'),
        )

        return fig


def main():
    st.set_page_config(layout="wide")

    # Import railroad data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'Railroad_Incidents', 'Dataset.csv')
    df_railroad = pd.read_csv(data_path, delimiter=',', low_memory=False)

    # Sidebar (Menu)
    st.sidebar.title("Example Dashboard")
    st.sidebar.write("JBI100 visualization project")

    # Main content
    # Choropleth Map
    choropleth = ChoroplethMap(df_railroad)
    st.subheader("Railroad Incidents by State")
    st.plotly_chart(choropleth.get_figure(), use_container_width=True)


if __name__ == '__main__':
    main()
