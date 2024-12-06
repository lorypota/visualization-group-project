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
            bounds={"west": MAP_CONFIGS['bounding_boxes']["lon"][0], "east": MAP_CONFIGS['bounding_boxes']["lon"][1],
                    "south": MAP_CONFIGS['bounding_boxes']["lat"][0], "north": MAP_CONFIGS['bounding_boxes']["lat"][1]},
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        uirevision='fixed',
    )
    return fig


def marker_properties():
    return dict(size=4,
                opacity=0.4,
                color='red')


def update_figure_data(fig, data):
    
    # If no trace exists, add one
    if not fig.data:
        fig.add_scattermapbox(
            lat=data["Latitude"].tolist() if len(data) else [],
            lon=data["Longitude"].tolist() if len(data) else [],
            hovertext=data["DATETIME"].astype(str).tolist() if len(data) else [],
            mode='markers',
            marker=marker_properties(),
        )
    else:
        # Update the existing scatter trace
        fig.update_traces(
            lat=data["Latitude"].tolist() if len(data) else [],
            lon=data["Longitude"].tolist() if len(data) else [],
            hovertext=data["DATETIME"].astype(str).tolist() if len(data) else [],
            marker=marker_properties(),
            selector=dict(type='scattermapbox')
        )
    print(fig.layout)
