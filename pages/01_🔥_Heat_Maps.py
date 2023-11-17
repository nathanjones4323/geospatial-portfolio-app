import os

import branca
import folium
import geopandas as gpd
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from streamlit_extras.app_logo import add_logo
from streamlit_folium import st_folium

from sidebar import init_sidebar
from utils import init_connection, reduce_top_margin

st.set_page_config(
    page_title="Heat Maps",
    page_icon="🔥",
    layout="wide"
)


def app():
    # Load Environment Variables from this relative path ./data-pipelines/census/.env given our working directory is ./pages
    dotenv_path = os.path.join(os.path.dirname(
        __file__), "../data-pipelines/census/.env")
    load_dotenv(dotenv_path)

    # Remove white space at top of page
    reduce_top_margin()

    # Add logo to sidebar
    add_logo("images/sidebar_logo.png", height=100)

    # Add a title and an explanation for the user
    st.title('🔥 Heat Maps')
    st.markdown(
        """
        Description of the page
        """)

    # Initalize the sidebar
    init_sidebar()

    # Fetch the data (cached for performance)
    conn = init_connection()

    geom_boundaries = gpd.read_postgis(
        """
    select 
        "NAMELSAD"
        , geometry
    from cbsa_boundaries_2021_simplified
    """, con=conn, geom_col="geometry")
    geom_boundaries.rename(columns={"NAMELSAD": "cbsa"}, inplace=True)

    data = pd.read_sql(
        """
        select 
            cbsa
            , est_gross_rent_occupied_units_paying_rent_median_dollars
        from acs_census_2021_cbsa
        """, con=conn)
    # Convert the `est_gross_rent_occupied_units_paying_rent_median_dollars` column to numeric
    data["est_gross_rent_occupied_units_paying_rent_median_dollars"] = pd.to_numeric(
        data["est_gross_rent_occupied_units_paying_rent_median_dollars"], errors="coerce")
    data = geom_boundaries.merge(data, on="cbsa", how="inner")

    m = folium.Map(location=[37.8, -96],
                   zoom_start=5, tiles='CartoDB positron', scrollWheelZoom=False)

    colormap = branca.colormap.LinearColormap(
        vmin=data["est_gross_rent_occupied_units_paying_rent_median_dollars"].quantile(
            0.0),
        vmax=data["est_gross_rent_occupied_units_paying_rent_median_dollars"].quantile(
            1),
        colors=["red", "orange", "lightblue", "green", "darkgreen"],
        caption="Median Rent Price ($)",
    )

    popup = folium.GeoJsonPopup(
        fields=data.drop(columns=["geometry"]).columns.to_list(),
        aliases=["CBSA", "Median Rent Price ($):"],
        localize=True,
        labels=True,
        style="background-color: yellow;",
    )

    tooltip = folium.GeoJsonTooltip(
        fields=data.drop(columns=["geometry"]).columns.to_list(),
        aliases=["CBSA", "Median Rent Price ($):"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )

    g = folium.GeoJson(
        data,
        style_function=lambda x: {
            "fillColor": colormap(x["properties"]["est_gross_rent_occupied_units_paying_rent_median_dollars"])
            if x["properties"]["est_gross_rent_occupied_units_paying_rent_median_dollars"] is not None
            else "transparent",
            "color": "black",
            "fillOpacity": 0.4,
        },
        tooltip=tooltip,
        popup=popup,
    ).add_to(m)

    colormap.add_to(m)

    st_folium(m, use_container_width=True, height=500, returned_objects=[])


app()
