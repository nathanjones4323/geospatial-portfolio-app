import streamlit as st


def query_error(df):
    """Throw error message to User if no data is being returned in a given query. Could be due to filter combination or an app bug.

    Args:
        df (pandas.DataFrame): Result set of a `queries.py` function
    """
    if len(df) == 0:
        st.error("No Data Returned **(Do your chosen filters make sense ?)**")
        st.stop()
