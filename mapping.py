from typing import Literal

import branca
import folium
import geopandas as gpd
from folium.plugins import Geocoder
from streamlit_folium import st_folium

from utils import title_case_columns


def create_colormap(data: gpd.GeoDataFrame, target_column: str, colormap_caption: str, colormap_colors: list = ["red", "orange", "lightblue", "green", "darkgreen"]) -> branca.colormap.LinearColormap:
    """Create a colormap for a choropleth map.

    Args:
        data (gpd.GeoDataFrame): A GeoDataFrame containing the data to be mapped.

        target_column (str): The column in the GeoDataFrame the colormap will be based on.

        colormap_colors (list): A list of colors to be used in the colormap. Can be hex codes, named colors, HTML color names, or RGB tuples.

        colormap_caption (str): The caption for the colormap to be shown on the map legend.

    Returns:
        branca.colormap.LinearColormap: A colormap to be used in a choropleth map.
    """

    # Define the colormap
    colormap = branca.colormap.LinearColormap(
        vmin=data[target_column].quantile(0.0),
        vmax=data[target_column].quantile(1),
        colors=colormap_colors,
        caption=colormap_caption
    )
    return colormap


def add_map_plugins(m):
    # Add a geocoder so users can search for locations
    Geocoder(position="bottomright").add_to(m)

    # Add different tile layer to the map
    folium.TileLayer('OpenStreetMap').add_to(m)

    folium.LayerControl(position="bottomleft").add_to(m)

    return m


def create_choropleth(data: gpd.GeoDataFrame, target_column: str, height: int = 500, aliases: list = None, colormap_caption: str = None) -> dict:

    # Create the folium map
    m = folium.Map(location=[37.8, -96],
                   zoom_start=5, tiles='CartoDB positron', scrollWheelZoom=False)

    # Define the colormap
    colormap = create_colormap(data=data,
                               colormap_caption=colormap_caption,
                               target_column=target_column)

    # Non geometry columns
    non_geometry_columns = data.drop(columns=["geometry"]).columns.to_list()

    # Create popups
    popup = folium.GeoJsonPopup(
        fields=non_geometry_columns,
        aliases=title_case_columns(
            non_geometry_columns) if aliases is None else aliases,
        localize=True,
        labels=True,
        style="background-color: yellow;",
    )

    # Create tooltips
    tooltip = folium.GeoJsonTooltip(
        fields=non_geometry_columns,
        aliases=title_case_columns(
            non_geometry_columns) if aliases is None else aliases,
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: (240, 239, 239, .1);
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """
    )

    # Create the GeoJson
    g = folium.GeoJson(
        data,
        style_function=lambda x: {
            "fillColor": colormap(x["properties"][target_column])
            if x["properties"][target_column] is not None
            else "transparent",
            "color": "black",
            "fillOpacity": 0.4,
        },
        tooltip=tooltip,
        popup=popup,
        name="Toggle Choropleth"
    )

    # Add the GeoJson to the map
    g.add_to(m)

    # Add the colorbar to the map
    colormap.add_to(m)

    # Add plugins to the map
    add_map_plugins(m)

    map = st_folium(m, use_container_width=True,
                    height=height, returned_objects=[])

    return map
