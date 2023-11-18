import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from streamlit_extras.app_logo import add_logo

from mapping import create_choropleth
from queries import load_cbsa_acs_data, load_cbsa_geom_data
from sidebar import init_sidebar
from utils import reduce_top_margin

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
        This page contains heat maps of the United States. The maps are interactive, so you can zoom in and out and click on the different regions to see the data for that region. 
        To zoom in and out, use the scroll wheel on your mouse, double click on the map, or use the zoom buttons in the top right corner of the map.

        You can also search for a specific location using the search bar in the bottom right corner of the map. 
        The maps are based on the [Selected Housing Characterisitcs dataset from the American Community Survey](https://data.census.gov/table/ACSDP5Y2021.DP04) put together by the [Census Bureau](https://www.census.gov/).
        """)

    # Initalize the sidebar
    init_sidebar()

    # Load boundary data
    geom_boundaries = load_cbsa_geom_data()
    geom_boundaries.rename(columns={"NAMELSAD": "cbsa"}, inplace=True)

    # Load ACS data
    data = load_cbsa_acs_data()

    # Convert the `est_gross_rent_occupied_units_paying_rent_median_dollars` column to numeric
    data["est_gross_rent_occupied_units_paying_rent_median_dollars"] = pd.to_numeric(
        data["est_gross_rent_occupied_units_paying_rent_median_dollars"], errors="coerce")
    data = geom_boundaries.merge(data, on="cbsa", how="inner")

    # Create the choropleth
    create_choropleth(data=data,
                      target_column="est_gross_rent_occupied_units_paying_rent_median_dollars",
                      height=600,
                      aliases=["CBSA", "Median Gross Rent ($)"],
                      colormap_caption="Median Gross Rent ($)")


app()
