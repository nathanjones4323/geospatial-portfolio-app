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
        -- Metric 1
            , est_gross_rent_occupied_units_paying_rent_median_dollars
        
        -- Metric 2
            , percent_housing_tenure_occupied_housing_units_renter_occupied
        
        -- Metric 3
            , percent_house_heating_fuel_occupied_housing_units_solar_energy::numeric +
                percent_house_heating_fuel_occupied_housing_units_electricity::numeric +
                percent_house_heating_fuel_occupied_housing_units_no_fuel_used::numeric +
                percent_house_heating_fuel_occupied_housing_units_other_fuel::numeric AS percent_renewable_energy

        -- Metric 4
            , percent_house_heating_fuel_occupied_housing_units_fuel_oil::numeric +
                percent_house_heating_fuel_occupied_housing_units_coal_or_coke::numeric +
                percent_house_heating_fuel_occupied_housing_units_wood::numeric +
                percent_house_heating_fuel_occupied_housing_units_gas_tank::numeric as percent_fossil_fuel

        -- Metric 5
            , est_value_owner_occupied_units_median_dollars
        from geospatial.acs_census_2021_cbsa
        -- where est_gross_rent_occupied_units_paying_rent_median_dollars is not null
        """, con=conn)

    return data


@st.cache_data(show_spinner=False)
def load_zcta_acs_data(cbsa_name: str):

    conn = init_connection()

    data = pd.read_sql(
        """
        select 
            zcta
        -- Metric 1
            , est_gross_rent_occupied_units_paying_rent_median_dollars
        
        -- Metric 2
            , percent_housing_tenure_occupied_housing_units_renter_occupied
    
        -- Metric 3
            , percent_house_heating_fuel_occupied_housing_units_solar_energy::numeric +
                percent_house_heating_fuel_occupied_housing_units_electricity::numeric +
                percent_house_heating_fuel_occupied_housing_units_no_fuel_used::numeric +
                percent_house_heating_fuel_occupied_housing_units_other_fuel::numeric AS percent_renewable_energy

        -- Metric 4
            , percent_house_heating_fuel_occupied_housing_units_fuel_oil::numeric +
                percent_house_heating_fuel_occupied_housing_units_coal_or_coke::numeric +
                percent_house_heating_fuel_occupied_housing_units_wood::numeric +
                percent_house_heating_fuel_occupied_housing_units_gas_tank::numeric as percent_fossil_fuel

            -- Metric 5
            , est_value_owner_occupied_units_median_dollars
        from geospatial.acs_census_2021_zcta
            left join geospatial.zip_to_cbsa
                on geospatial.zip_to_cbsa.zip_code = geospatial.acs_census_2021_zcta.zcta
            left join geospatial.cbsa_boundaries_2021_simplified
                on geospatial.cbsa_boundaries_2021_simplified."CBSAFP" = geospatial.zip_to_cbsa.cbsa_code
        where 1=1
            and geospatial.cbsa_boundaries_2021_simplified."NAMELSAD" =  %(cbsa_name)s
        """,
        con=conn,
        params={"cbsa_name": cbsa_name}
    )

    # conn.close()

    return data
