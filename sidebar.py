import pandas as pd
import streamlit as st


def init_sidebar():
    with st.sidebar.form(key='Form1'):

        # Write some instructions / help for the user inside of the sidebar
        st.sidebar.markdown("""
            You can use these filters to modify what you see in on the map.
                            
            CBSA's are Metropolitan/Micropolitan areas roughly made up of one or more counties.
            
            ZCTA's are the polygon representation of zip codes.
                            """)

        # Init query params
        query_params = st.experimental_get_query_params()

        if "geographic_granularity" not in st.session_state:
            st.session_state["geographic_granularity"] = (
                query_params.get("geographic_granularity", ["CBSA", "ZCTA"])[0]
            )
        geographic_granularity = st.selectbox("Select Geographic Granularity", options=[
                                              "CBSA", "ZCTA"], index=0, help="Select a metric to view on the map", key="geographic_granularity_key")

        # Set up the sidebar filters and widgets
        if "metric_name" not in st.session_state:
            st.session_state["metric_name"] = (
                int(query_params.get("metric_name", [90])[0])
            )
        metric_name = st.selectbox("Select a Metric", value=["Median Rent Price ($)"], min_value=0,
                                   max_value=100, step=1, help="Select a metric to view on the map", key="metric_name_key")

        # Form submit button
        submitted1 = st.form_submit_button(label='Refresh Metrics 🔄')

        return metric_name, geographic_granularity, submitted1
