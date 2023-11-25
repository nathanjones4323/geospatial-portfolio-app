import os

import streamlit as st
from pandas import isnull
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

from ..data_pipelines.census.transform import standardize_column_name

# Initialize global variables
METRIC_NAME_MAPPING = {}
SELECTED_METRICS = []


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
        "Median Rent Price ($)": "est_gross_rent_occupied_units_paying_rent_median_dollars",
        "Renter Occupied Housing (%)": "percent_housing_tenure_occupied_housing_units_renter_occupied",
        "Electric, Renewable, or No Heating Source (%)": "percent_renewable_energy",
        "Direct Fossil Fuel Heating Source (%)": "percent_fossil_fuel",
        "Median Home Value ($)": "est_value_owner_occupied_units_median_dollars",
    }
    return mapping.get(display_name, display_name)


# Assuming that transform.py is in the parent directory
def add_metric_mappings(metric_display_name: str, us_census_metric_name: str):

    # Standardize the metric name
    metric_internal_name = standardize_column_name(us_census_metric_name)

    # Add the metric to the internal name <> display name mapping
    METRIC_NAME_MAPPING[metric_display_name] = metric_internal_name

    # Apply custom renaming logic for specific metrics (avoid PostgreSQL name truncation errors)
    if metric_internal_name == "percent_house_heating_fuel_occupied_housing_units_bottled_tank_or_lp_gas":
        metric_internal_name = "percent_house_heating_fuel_occupied_housing_units_gas_tank"

    elif metric_internal_name == "percent_house_heating_fuel_occupied_housing_units_fuel_oil_kerosene_etc.":
        metric_internal_name = "percent_house_heating_fuel_occupied_housing_units_fuel_oil"

    # Add the metric to the list of selected metrics
    SELECTED_METRICS.append(metric_internal_name)


def add_metrics(us_census_metrics: list, metric_display_names: list):
    for metric_display_name, us_census_metric_name in zip(metric_display_names, us_census_metrics):
        add_metric_mappings(metric_display_name, us_census_metric_name)
