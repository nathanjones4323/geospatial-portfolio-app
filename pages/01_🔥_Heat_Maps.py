import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from streamlit_extras.app_logo import add_logo

from display import display_dataframe
from mapping.create import create_choropleth
from mapping.utils import get_geographic_mapping
from queries.boundaries import get_cbsa_center_point
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
    
    - Click on a CBSA to drill down into it's ZCTAs (Zip Codes) for a more detailed data of the area.
    
    - Search for a specific location's on the map using the search bar in the bottom right corner.

    **Data Source (2021):**
    
    The maps are based on the [Selected Housing Characteristics dataset (2021)](https://data.census.gov/table/ACSDP5Y2021.DP04) from the American Community Survey, compiled by the [Census Bureau](https://www.census.gov/).
    """
    )

    # Initalize the sidebar
    metric_display_name = init_sidebar()
    metric_internal_name = get_metric_internal_name(metric_display_name)

    geographic_granularity = "CBSA"
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
        data.dropna(inplace=True)

        with st.spinner("Loading map..."):
            # Create the choropleth
            last_object_clicked_tooltip = create_choropleth(data=data,
                                                            target_column=metric_internal_name,
                                                            height=600,
                                                            aliases=[geographic_granularity,
                                                                     metric_display_name],
                                                            colormap_caption=metric_display_name,
                                                            cbsa_internal_points=None)
            if last_object_clicked_tooltip["last_object_clicked_tooltip"] is not None:
                cbsa_name = last_object_clicked_tooltip["last_object_clicked_tooltip"]
                cbsa_name = cbsa_name.split("Area")[0].split("CBSA")[
                    1] + "Area"
                cbsa_name = cbsa_name.strip()

        with st.spinner("Loading data table..."):
            # Display the underlying map data
            display_dataframe(data=data,
                              metric_internal_name=metric_internal_name,
                              metric_display_name=metric_display_name,
                              geographic_granularity_internal_name=geographic_granularity_internal_name,
                              geographic_granularity_display_name=geographic_granularity)

        if last_object_clicked_tooltip["last_object_clicked_tooltip"] is not None:
            # Add a divider
            st.divider()

            with st.spinner("Loading drill down map..."):
                st.markdown(f"### ZCTA drill down into {cbsa_name}")
                # Query ZCTAs for the selected CBSA
                zcta_data = get_geographic_mapping(
                    "ZCTA")["data_function"](cbsa_name=cbsa_name)
                zcta_geom_boundaries = get_geographic_mapping("ZCTA")[
                    "geom_function"](cbsa_name=cbsa_name)
                zcta_geographic_granularity_internal_name = get_geographic_mapping("ZCTA")[
                    "on_column"]

                # Clean the data
                zcta_data[metric_internal_name] = pd.to_numeric(
                    zcta_data[metric_internal_name], errors="coerce")
                zcta_data = zcta_geom_boundaries.merge(
                    zcta_data, on=zcta_geographic_granularity_internal_name, how="inner")
                zcta_data = zcta_data[[zcta_geographic_granularity_internal_name,
                                       metric_internal_name, "geometry"]]
                # Create the choropleth
                last_object_clicked_tooltip = create_choropleth(data=zcta_data,
                                                                target_column=metric_internal_name,
                                                                height=600,
                                                                aliases=["ZCTA",
                                                                         metric_display_name],
                                                                colormap_caption=metric_display_name,
                                                                cbsa_internal_points=get_cbsa_center_point(cbsa_name))

                with st.spinner("Loading data table..."):
                    # Display the underlying map data
                    display_dataframe(data=zcta_data,
                                      metric_internal_name=metric_internal_name,
                                      metric_display_name=metric_display_name,
                                      geographic_granularity_internal_name=zcta_geographic_granularity_internal_name,
                                      geographic_granularity_display_name="ZCTA")


app()
