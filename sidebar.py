import pandas as pd
import streamlit as st


def init_sidebar():
    # Write some instructions / help for the user inside of the sidebar
    st.sidebar.markdown(
        """
        **Find a metric you want to explore 👇**
        """
    )

    # Init query params
    query_params = st.experimental_get_query_params()

    # Set up the sidebar filters and widgets
    if "metric_display_name" not in st.session_state:
        st.session_state["metric_display_name"] = (
            query_params.get("metric_display_name", [
                "Median Rent Price ($)"])[0]
        )
    metric_display_name = st.sidebar.selectbox("Select a Metric",
                                               options=[
                                                   "Median Rent Price ($)",
                                                   "Renter Occupied Housing (%)",
                                                   "Electric, Renewable, or No Heating Source (%)",
                                                   "Direct Fossil Fuel Heating Source (%)",
                                                   "Median Home Value ($)"
                                               ],
                                               index=0,
                                               help="Select a metric to view on the map",
                                               key="metric_display_name_key")

    st.sidebar.divider()

    st.sidebar.markdown(
        """ℹ️ [What is a CBSA ?](https://en.wikipedia.org/wiki/Core-based_statistical_area)""")

    st.sidebar.markdown(
        """ℹ️ [What is a ZCTA ?](https://www.census.gov/programs-surveys/geography/guidance/geo-areas/zctas.html#:~:text=ZIP%20Code%20Tabulation%20Areas%20or,Plan%20(ZIP)%20Codes%20dataset.)""")

    st.sidebar.divider()

    st.sidebar.markdown(
        """Explore the CBSA map and click on a CBSA to create a drilled down map of the ZCTAs within that CBSA (Heatmaps only).""")

    return metric_display_name
