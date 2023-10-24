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
    db_name = os.environ['POSTGRES_NAME']

    conn_string = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
    engine = create_engine(url=conn_string)

    return engine


def monetize(df, column_list):
    """Appends a new column for each series to the original dataframe with a formatted dollar amount rounded to cents.

    Args:
        df (pandas.DataFrame): pandas Dataframe of desired columns to format in dollars.
    """
    for series in df[column_list]:
        if series == "major_region" or series == "cbsa_name" or series == "zcta":
            df[f"{series}_formatted"] = df[series]
        else:
            df[f"{series}_formatted"] = df[series].apply(lambda x: '-' if (x is None or isnull(
                x)) else ('-$ {:,.2f}'.format(abs(x)) if x < 0 else '$ {:,.2f}'.format(x)))
    return df


def percentize(df, column_list):
    """Appends a new column for each series to the original dataframe with a formatted percentage rounded to 2 decimals.

    Args:
        df (pandas.DataFrame): pandas Dataframe of desired columns to format as a percentage
    """
    for series in df[column_list]:
        if series == "major_region" or series == "cbsa_name" or series == "zcta":
            df[f"{series}_formatted"] = df[series]
        else:
            df[f"{series}_formatted"] = df[series].apply(
                lambda x: '-' if (x is None or isnull(x)) else ('{:,.2f}%'.format(x)))
    return df


def format(df, column_list):
    """Appends a new column for each series to the original dataframe with a comma formatted number rounded to nearest integer.

    Args:
        df (pandas.DataFrame): pandas Dataframe of desired columns to format
    """
    for series in df[column_list]:
        if series == "major_region" or series == "cbsa_name" or series == "zcta":
            df[f"{series}_formatted"] = df[series]
        else:
            df[f"{series}_formatted"] = df[series].apply(
                lambda x: '-' if (x is None or isnull(x)) else ('{:,}'.format(int(x))))
    return df


def float_format(df, column_list):
    """Appends a new column for each series to the original dataframe with a comma formatted number rounded to 2 decimal places.

    Args:
        df (pandas.DataFrame): pandas Dataframe of desired columns to format
    """
    for series in df[column_list]:
        if series == "major_region" or series == "cbsa_name" or series == "zcta":
            df[f"{series}_formatted"] = df[series]
        else:
            df[f"{series}_formatted"] = df[series].apply(
                lambda x: '-' if (x is None or isnull(x)) else ('{:,.2f}'.format(x)))
    return df
