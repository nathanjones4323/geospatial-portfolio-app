import geopandas as gpd
import pandas as pd
import streamlit as st

from utils import init_connection


@st.cache_data(show_spinner=False)
def load_cbsa_geom_data():

    conn = init_connection()

    geom_boundaries = gpd.read_postgis(
        """
    select 
        "NAMELSAD"
        , geometry
    from cbsa_boundaries_2021_simplified
    """, con=conn, geom_col="geometry")
    geom_boundaries.rename(columns={"NAMELSAD": "cbsa"}, inplace=True)

    return geom_boundaries


@st.cache_data(show_spinner=False, ttl=3600*24)
def load_zcta_geom():
    conn = init_connection()

    geom_boundaries = gpd.read_postgis(
        """
    select 
        "ZCTA5CE20"
        , geometry
    from zcta_boundaries_2021_simplified
    """, con=conn, geom_col="geometry")
    geom_boundaries.rename(columns={"ZCTA5CE20": "zcta"}, inplace=True)

    return geom_boundaries


def get_cbsa_center_point(cbsa_name) -> list:
    conn = init_connection()

    point = pd.read_sql("""
    select 
        "INTPTLAT"::numeric as internal_latitude
        , "INTPTLON"::numeric as internal_longitude 
    from cbsa_boundaries_2021_simplified
    where "NAMELSAD" = %(cbsa_name)s
    """,
                        con=conn,
                        params={"cbsa_name": cbsa_name},
                        index_col=None)

    # Convert to list
    point = point.values.tolist()[0]

    return point
