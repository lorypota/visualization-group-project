import plotly.express as px
from config import MAPBOX_ACCESS_TOKEN, MAP_CONFIGS


def create_base_figure():
    config = MAP_CONFIGS["Continental USA"]
    fig = px.scatter_mapbox(
        lat=[],
        lon=[],
        zoom=config["zoom_level"],
        center=config["center_coords"],
    )
    fig.update_layout(
        mapbox=dict(
            accesstoken=MAPBOX_ACCESS_TOKEN,
            style="mapbox://styles/mapbox/streets-v12",
        ),
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        uirevision='fixed',
        title="Map: Continental USA"
    )
    return fig


def update_figure_data(fig, data):
    # If no trace exists, add one
    if not fig.data:
        fig.add_scattermapbox(
            lat=data["Latitude"].tolist() if len(data) else [],
            lon=data["Longitude"].tolist() if len(data) else [],
            hovertext=data["DATETIME"].astype(str).tolist() if len(data) else [],
            mode='markers',
            marker=dict(size=8)
        )
    else:
        # Update the existing scatter trace
        fig.update_traces(
            lat=data["Latitude"].tolist() if len(data) else [],
            lon=data["Longitude"].tolist() if len(data) else [],
            hovertext=data["DATETIME"].astype(str).tolist() if len(data) else [],
            selector=dict(type='scattermapbox')
        )
