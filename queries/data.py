import pandas as pd
import streamlit as st

from utils import init_connection


@st.cache_data(show_spinner=False)
def load_cbsa_acs_data():

    conn = init_connection()

    data = pd.read_sql(
        """
        select 
            cbsa
            , est_gross_rent_occupied_units_paying_rent_median_dollars
        from acs_census_2021_cbsa
        where est_gross_rent_occupied_units_paying_rent_median_dollars is not null
        """, con=conn)

    return data


@st.cache_data(show_spinner=False)
def load_zcta_acs_data():

    conn = init_connection()

    data = pd.read_sql(
        """
        select 
            zcta
            , est_gross_rent_occupied_units_paying_rent_median_dollars
        from acs_census_2021_zcta
        where est_gross_rent_occupied_units_paying_rent_median_dollars is not null
        """, con=conn)

    # conn.close()

    return data
