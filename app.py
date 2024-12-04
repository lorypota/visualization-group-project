from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.choropleth import ChoroplethMap

from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import os

if __name__ == '__main__':
    # Create data
    df = px.data.iris()

    # Import railroad data
    pd.set_option('display.max_columns', None)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'Railroad_Incidents', 'Dataset.csv')
    df_railroad = pd.read_csv(data_path, delimiter=',', low_memory=False)

    # Instantiate custom views
    scatterplot1 = Scatterplot("Scatterplot 1", 'sepal_length', 'sepal_width', df)
    scatterplot2 = Scatterplot("Scatterplot 2", 'petal_length', 'petal_width', df)
    choropleth = ChoroplethMap(df_railroad)

    # app.layout = html.Div(
    #     id="app-container",
    #     children=[
    #         # Left column
    #         html.Div(
    #             id="left-column",
    #             className="three columns",
    #             children=make_menu_layout()
    #         ),

            # Right column
            html.Div(
                id="right-column",
                className="nine columns",
                children=[
                    html.Div(
                        choropleth,
                        style={'marginBottom': '20px'}
                    ),
                    scatterplot1,
                    scatterplot2
                ],
            ),
        ],
    )

    # Define interactions
    # @app.callback(
    #     Output(scatterplot1.html_id, "figure"), [
    #     Input("select-color-scatter-1", "value"),
    #     Input(scatterplot2.html_id, 'selectedData')
    # ])
    # def update_scatter_1(selected_color, selected_data):
    #     return scatterplot1.update(selected_color, selected_data)

    @app.callback(
        Output(scatterplot2.html_id, "figure"), [
        Input("select-color-scatter-2", "value"),
        Input(scatterplot1.html_id, 'selectedData')
    ])
    def update_scatter_2(selected_color, selected_data):
        return scatterplot2.update(selected_color, selected_data)



    app.run_server(debug=False, dev_tools_ui=False)