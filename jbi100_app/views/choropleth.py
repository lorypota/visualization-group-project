from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go


class ChoroplethMap(html.Div):
    def __init__(self, df):
        self.df = df
        self.html_id = "choropleth-map"

        # State code to abbreviation mapping
        self.state_codes = {
            1: 'AL', 2: 'AK', 4: 'AZ', 5: 'AR', 6: 'CA', 8: 'CO', 9: 'CT', 10: 'DE',
            11: 'DC', 12: 'FL', 13: 'GA', 15: 'HI', 16: 'ID', 17: 'IL', 18: 'IN', 19: 'IA',
            20: 'KS', 21: 'KY', 22: 'LA', 23: 'ME', 24: 'MD', 25: 'MA', 26: 'MI', 27: 'MN',
            28: 'MS', 29: 'MO', 30: 'MT', 31: 'NE', 32: 'NV', 33: 'NH', 34: 'NJ', 35: 'NM',
            36: 'NY', 37: 'NC', 38: 'ND', 39: 'OH', 40: 'OK', 41: 'OR', 42: 'PA', 44: 'RI',
            45: 'SC', 46: 'SD', 47: 'TN', 48: 'TX', 49: 'UT', 50: 'VT', 51: 'VA', 53: 'WA',
            54: 'WV', 55: 'WI', 56: 'WY'
        }

        # Initialize the figure
        self.fig = self.get_figure()

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6("Railroad Incidents by State"),
                dcc.Graph(
                    id=self.html_id,
                    figure=self.fig,
                    style={'height': '600px', 'width': '100%'}
                )
            ],
        )

    def get_figure(self):
        # Count records per state and convert state codes to abbreviations
        state_counts = self.df.groupby(
            ['STATE']).size().reset_index(name='count')
        state_counts['STATE'] = state_counts['STATE'].map(self.state_codes)

        # Create base figure using plotly.express
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
            width=1000,
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

    def update(self, *args):
        """
        Currently doesn't modify the plot but could be used for future interactivity.
        """
        return self.fig
