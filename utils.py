import os

import streamlit as st
from pandas import isnull
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine


def reduce_top_margin():
    st.markdown(
        " <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)


@st.cache_resource
def init_connection() -> Engine:
    """Initalizes a connection to the database

    Returns:
        sqlalchemy.engine.base.Engine: A connection to the database
    """
    db_user = os.environ['POSTGRES_USER']
    db_pass = os.environ['POSTGRES_PASSWORD']
    db_host = os.environ['POSTGRES_HOST']
    db_name = os.environ['POSTGRES_DB']

    conn_string = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
    engine = create_engine(url=conn_string)

    return engine


def title_case_columns(columns: list) -> list:
    """Converts a list of column names to title case

    Args:
        columns (list): A list of column names

    Returns:
        list: A list of column names in title case
    """
    columns = [x.replace('_', ' ').strip().title() for x in columns]
    return columns


def get_metric_internal_name(display_name):
    mapping = {
        "Median Rent Price ($)": "est_gross_rent_occupied_units_paying_rent_median_dollars"
        # Add more mappings here as needed
    }
    return mapping.get(display_name, display_name)
