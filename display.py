import pandas as pd
import streamlit as st


def display_dataframe(data: pd.DataFrame, metric_internal_name: str, metric_display_name: str, geographic_granularity_internal_name: str, geographic_granularity_display_name: str):

    # Add a divider
    st.divider()

    st.markdown("### Underlying Map Data")

    # Crearte column config based on the column types
    column_config = {
        geographic_granularity_internal_name: st.column_config.Column(
            label=geographic_granularity_display_name
        ),
        metric_internal_name: st.column_config.NumberColumn(
            label=metric_display_name
        )
    }

    # Drop geometry column if it exists
    if "geometry" in data.columns:
        new_df = data.drop(columns=["geometry"])
    if "geom" in data.columns:
        new_df = data.drop(columns=["geom"])

    display_df = st.dataframe(data=new_df,
                              use_container_width=True,
                              height=300,
                              hide_index=True,
                              column_config=column_config
                              )
    return display_df
