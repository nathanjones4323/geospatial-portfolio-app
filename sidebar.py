import pandas as pd
import streamlit as st


def init_sidebar():
    # Write some instructions / help for the user inside of the sidebar
    st.sidebar.markdown(
        """
        **Filter Options:**

        Adjust these filters to modify what you see on the map.

        Hover over the **(?)** icon to learn more about each filter.

        """
    )

    with st.sidebar.form(key='Form1'):

        # Init query params
        query_params = st.experimental_get_query_params()

        if "geographic_granularity" not in st.session_state:
            st.session_state["geographic_granularity"] = (
                query_params.get("geographic_granularity", ["CBSA", "ZCTA"])[0]
            )
        geographic_granularity = st.selectbox("Select Geographic Granularity", options=[
                                              "CBSA", "ZCTA"], index=0, help="ℹ️[What is a CBSA ?](https://curri.slab.com/posts/definitions-v2hle5l7#hm0ta-cbsa)\n\nℹ️ [What is a ZCTA ?](https://curri.slab.com/posts/definitions-v2hle5l7#h0c1f-zcta-zip-code-tabulated-area)", key="geographic_granularity_key")

        # Set up the sidebar filters and widgets
        if "metric_display_name" not in st.session_state:
            st.session_state["metric_display_name"] = (
                query_params.get("metric_display_name", [
                                 "Median Rent Price ($)"])[0]
            )
        metric_display_name = st.selectbox("Select a Metric", options=[
            "Median Rent Price ($)"], index=0, help="Select a metric to view on the map", key="metric_display_name_key")

        # Form submit button
        submitted1 = st.form_submit_button(label='Refresh Metrics 🔄')

        return metric_display_name, geographic_granularity, submitted1
