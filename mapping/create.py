from typing import Literal

import branca
import folium
import geopandas as gpd
import pydeck as pdk
import streamlit as st
from folium.plugins import Geocoder
from streamlit_folium import st_folium

from utils import title_case_columns


def create_colormap(data: gpd.GeoDataFrame, target_column: str, colormap_caption: str, colormap_colors: list = ['#ffffff', '#f9e3e3', '#f4c6c6', '#eeaaaa', '#e88e8e', '#e27272', '#dd5555', '#d73939']) -> branca.colormap.LinearColormap:
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
        colors=colormap_colors,
        vmin=data[target_column].quantile(0.0),
        vmax=data[target_column].quantile(1),
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
    m = folium.Map(location=[35.3, -97.6], zoom_start=4,
                   tiles='CartoDB positron', scrollWheelZoom=True)

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
            "fillOpacity": 1,
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


def create_3d_map(data: gpd.GeoDataFrame, target_column: str, geographic_granularity: Literal["cbsa", "zcta"] = "cbsa") -> None:
    # Get the min and max values for setting elevation and fill color
    min_value = data[target_column].min()
    max_value = data[target_column].max()

    # Normalize to a range between 0 and 1
    normalized_elevation = f"({target_column} - {min_value}) / ({max_value - min_value})"
    elevation = f"200000 * {normalized_elevation}"
    fill_color_scaler = f"{normalized_elevation}"

    # Create GeoJsonLayer using Pydeck
    geojson_layer = pdk.Layer(
        "GeoJsonLayer",
        data=data,
        opacity=1,
        stroked=True,
        filled=True,
        extruded=True,
        wireframe=True,
        get_elevation=elevation,
        get_fill_color=f"[255, 255 - {fill_color_scaler} * 255, 255 - {fill_color_scaler} * 255]",
        get_line_color=[255, 255, 255],
        pickable=True
    )

    # Define the viewport for the map
    view_state = pdk.ViewState(
        latitude=35.3,
        longitude=-97.6,
        zoom=4,
        pitch=45
    )
    # Create the Pydeck Deck
    r = pdk.Deck(layers=[geojson_layer],
                 initial_view_state=view_state,
                 tooltip={
        "html": f"<b>{geographic_granularity.upper()}: {{{geographic_granularity}}}</b><br/><b>Median Rent Price ($)</b> {{{target_column}}}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    },
        map_style="light"
    )

    # Render the map in Streamlit
    return st.pydeck_chart(r)
