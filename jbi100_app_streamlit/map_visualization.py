import plotly.express as px
from config import MAPBOX_ACCESS_TOKEN, MAP_CONFIGS


def create_map(data, region):
    """Create a mapbox scatter plot."""
    config = MAP_CONFIGS[region]

    fig = px.scatter_mapbox(
        data,
        lat="Latitude",
        lon="Longitude",
        hover_name="DATETIME",
        zoom=config["zoom_level"],
        center=config["center_coords"],
        title=f"Map: {region}"
    )

    fig.update_layout(
        mapbox=dict(
            accesstoken=MAPBOX_ACCESS_TOKEN,
            style="mapbox://styles/mapbox/streets-v12",
        ),
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
    )

    return fig
