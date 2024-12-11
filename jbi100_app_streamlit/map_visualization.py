import plotly.express as px
from config import MAPBOX_ACCESS_TOKEN, MAP_CONFIGS

DEFAULT_STYLE = "mapbox://styles/mapbox/streets-v12"
STYLE = "mapbox://styles/mggiordano/cm4iq6416000601s89eyagmeu"


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
            style=DEFAULT_STYLE,
            bounds={"west": MAP_CONFIGS['bounding_boxes']["lon"][0], "east": MAP_CONFIGS['bounding_boxes']["lon"][1],
                    "south": MAP_CONFIGS['bounding_boxes']["lat"][0], "north": MAP_CONFIGS['bounding_boxes']["lat"][1]},
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        uirevision='fixed',
        showlegend=False
    )
    return fig


def marker_properties_selected():
    return dict(size=6, opacity=0.8, color='red')


def marker_properties_unselected():
    return dict(size=5, opacity=0.4, color='#FFCCCB')


def update_figure_data(fig, data, selected_filter):
    # Separate selected and unselected data
    selected_data = data[selected_filter].copy()
    unselected_data = data[~selected_filter].copy()

    # Add hover labels without mutating the original DataFrame
    selected_data['hover_label'] = 'Selected'
    unselected_data['hover_label'] = 'Unselected'

    # Update the traces directly; ensure the selector name matches the trace name
    try:
        fig.update_traces(
            lat=selected_data["Latitude"].tolist(),
            lon=selected_data["Longitude"].tolist(),
            hovertext=(selected_data["DATETIME"].astype(
                str) + " - " + selected_data["hover_label"]).tolist(),
            marker=marker_properties_selected(),
            selector=dict(name="Selected"),
        )
    except Exception as e:
        print("Error updating 'Selected' trace:", e)

    try:
        fig.update_traces(
            lat=unselected_data["Latitude"].tolist(),
            lon=unselected_data["Longitude"].tolist(),
            hovertext=(unselected_data["DATETIME"].astype(
                str) + " - " + unselected_data["hover_label"]).tolist(),
            marker=marker_properties_unselected(),
            selector=dict(name="Unselected"),
        )
    except Exception as e:
        print("Error updating 'Unselected' trace:", e)

    # If traces for "Selected" and "Unselected" do not exist, add them
    existing_trace_names = [trace.name for trace in fig.data]
    if "Selected" not in existing_trace_names:
        fig.add_scattermapbox(
            lat=selected_data["Latitude"].tolist(),
            lon=selected_data["Longitude"].tolist(),
            hovertext=(selected_data["DATETIME"].astype(
                str) + " - " + selected_data["hover_label"]).tolist(),
            mode='markers',
            marker=marker_properties_selected(),
            name="Selected",
        )
    if "Unselected" not in existing_trace_names:
        fig.add_scattermapbox(
            lat=unselected_data["Latitude"].tolist(),
            lon=unselected_data["Longitude"].tolist(),
            hovertext=(unselected_data["DATETIME"].astype(
                str) + " - " + unselected_data["hover_label"]).tolist(),
            mode='markers',
            marker=marker_properties_unselected(),
            name="Unselected",
        )
