import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from streamlit_extras.app_logo import add_logo

from display import display_dataframe
from mapping.create import create_choropleth
from mapping.utils import get_geographic_mapping
from sidebar import init_sidebar
from utils import get_metric_internal_name, reduce_top_margin

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
    **Welcome to Heat Maps of the United States!**

    Explore interactive maps where you can:
    
    - Zoom in and out by using the scroll wheel on your mouse, double-clicking on the map, or using the zoom buttons in the top right corner.
    
    - Click on different regions to view detailed data for that area.
    
    - Search for a specific location using the search bar in the bottom right corner.

    **Data Source (2021):**
    
    The maps are based on the [Selected Housing Characteristics dataset (2021)](https://data.census.gov/table/ACSDP5Y2021.DP04) from the American Community Survey, compiled by the [Census Bureau](https://www.census.gov/).
    """
    )

    # Initalize the sidebar
    metric_display_name, geographic_granularity, submitted1 = init_sidebar()
    metric_internal_name = get_metric_internal_name(metric_display_name)

    # Get mapping information
    granularity_info = get_geographic_mapping(geographic_granularity)
    if granularity_info:
        geom_boundaries = granularity_info["geom_function"]()
        data = granularity_info["data_function"]()
        geographic_granularity_internal_name = granularity_info["on_column"]

        # Clean the data
        data[metric_internal_name] = pd.to_numeric(
            data[metric_internal_name], errors="coerce")
        data = geom_boundaries.merge(
            data, on=granularity_info["on_column"], how="inner")
        data = data[[geographic_granularity_internal_name,
                     metric_internal_name, "geometry"]]

        with st.spinner("Loading map..."):
            # Create the choropleth
            create_choropleth(data=data,
                              target_column=metric_internal_name,
                              height=600,
                              aliases=[geographic_granularity,
                                       metric_display_name],
                              colormap_caption=metric_display_name)

        with st.spinner("Loading data table..."):
            # Display the underlying map data
            display_dataframe(data=data,
                              metric_internal_name=metric_internal_name,
                              metric_display_name=metric_display_name,
                              geographic_granularity_internal_name=geographic_granularity_internal_name,
                              geographic_granularity_display_name=geographic_granularity)


app()
