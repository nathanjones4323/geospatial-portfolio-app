import pandas as pd
import streamlit as st


def init_sidebar():
    with st.sidebar.form(key='Form1'):
        # Init query params
        query_params = st.experimental_get_query_params()

        # Set up the sidebar filters and widgets
        if "param_1" not in st.session_state:
            st.session_state["param_1"] = (
                int(query_params.get("param_1", [90])[0])
            )
        param_1 = st.number_input("Select Parameter 1", value=90, min_value=0,
                                  max_value=100, step=1, help="Parameter 1 Tooltip", key="param_1_key")

        if "n_bins" not in st.session_state:
            st.session_state["n_bins"] = (
                int(query_params.get("n_bins", [6])[0])
            )
        n_bins = int(st.number_input("Select # of Bins for Heat Map", min_value=2, max_value=20, step=1,
                     help="ℹ️ [What is a Choropleth](https://en.wikipedia.org/wiki/Choropleth_map)\n\n⚠️ Too many bins can make colors harder to differentiate", key="n_bins"))

        if "remove_nulls" not in st.session_state:
            st.session_state["remove_nulls"] = (
                bool(query_params.get("remove_nulls",
                     ["False"])[0].lower() == "true")
            )
        remove_nulls = st.checkbox("Remove NULLs",
                                   help="✅ to only show Geos that have Non `NULL` values.\n\nOtherwise all Geos are shown", key="remove_nulls")

        # Form submit button
        submitted1 = st.form_submit_button(label='Refresh Metrics 🔄')

        return param_1, n_bins, remove_nulls, submitted1
