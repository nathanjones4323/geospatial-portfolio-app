import os

import geopandas as gpd
import pandas as pd
import streamlit as st

from utils import init_connection


def query_error(df):
    """Throw error message to User if no data is being returned in a given query. Could be due to filter combination or an app bug.

    Args:
        df (pandas.DataFrame): Result set of a `queries.py` function
    """
    if len(df) == 0:
        st.error("No Data Returned **(Do your chosen filters make sense ?)**")
        st.stop()


################################################################################
# Geometry Related (Polygon Boundaries, Lat / Long Points, Etc.)
################################################################################

@st.cache_data(show_spinner=False)
def load_cbsa_geom(__conn):
    cbsa_df = gpd.read_postgis(
        """
    select namelsad as cbsa_name, geom from analytics.cbsa_boundaries where namelsad not like '%%, PR%%'
    """, con=__conn, geom_col="geom")

    return cbsa_df


@st.cache_data(show_spinner=False, ttl=3600*24)
def load_zcta_geom(__conn, cbsa):
    zcta_df = gpd.read_postgis(
        """
    select zcta, geometry as geom
    from analytics.zcta_boundaries_2020
    where 1=1
        and analytics.zcta_boundaries_2020.zcta in
        (
        select distinct analytics.zip_to_zcta_2020.zcta
        from analytics.zip_to_cbsa
            left join analytics.zip_to_zcta_2020
                on analytics.zip_to_zcta_2020.zip_code = analytics.zip_to_cbsa.zip_code
        where 1=1
            and analytics.zip_to_cbsa.cbsa_name = %(cbsa)s
        )
    """, con=__conn, geom_col="geom", params={"cbsa": cbsa})

    cbsa_internal_points = pd.read_sql(
        """
    select intptlat as internal_latitude, intptlon as internal_longitude from analytics.cbsa_boundaries where namelsad = %(cbsa)s
    """, con=__conn, params={"cbsa": cbsa})
    return zcta_df, cbsa_internal_points
