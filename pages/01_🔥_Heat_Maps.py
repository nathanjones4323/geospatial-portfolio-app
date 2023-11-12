import os

import geopandas as gpd
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from streamlit_extras.app_logo import add_logo
from streamlit_folium import folium_static

from mapping import create_choropleth
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
    select * from cbsa_boundaries_2021
    """, con=conn)
    st.write(geom_boundaries)
    data = pd.read_sql(
        """
        select * from acs_census_2021_cbsa
        """, con=conn)
    st.write(data)

    data = geom_boundaries.merge(data, on="cbsa", how="inner")
    st.write(data)

    # Display the map
    m = create_choropleth(
        data=data, target_variable="est_gross_rent_occupied_units_paying_rent_median_dollars", geom_granularity="cbsa")
    folium_static(m)


app()
