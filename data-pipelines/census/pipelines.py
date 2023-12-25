import pandas as pd
from extract import (extract_2021_acs_5_year_data,
                     extract_geography_boundaries, extract_zip_to_cbsa)
from load import create_pkey, init_connection, load_boundary_data, load_data
from loguru import logger
from transform import clean_census_data, get_human_readable_columns

from utils import (create_geospatial_schema, create_postgis_extension,
                   create_simplified_polygons, is_table_initialized)


def run_db_init_pipeline():
    # Create DB Connection
    try:
        conn = init_connection()
        logger.success("Successfully connected to DB")
    except Exception as e:
        logger.error(f"Error connecting to DB: {e}")

    # Create PostGIS Extension
    create_postgis_extension(conn)

    # Create Geospatial Schema
    create_geospatial_schema(conn)

    # Close DB Connection
    conn.close()


def run_acs_2021_zcta_pipeline():
    # Check if table is already initialized
    if not is_table_initialized("acs_census_2021_zcta"):
        try:
            r = extract_2021_acs_5_year_data(geography="zcta")
            logger.success(
                "Successfully read 2021 ACS data from the US Census")
        except Exception as e:
            logger.error(
                f"Error reading 2021 ACS data from the US Census: {e}")

        try:
            data = clean_census_data(r, geography="zcta")
            logger.success("Data cleaned successfully")
        except Exception as e:
            logger.error(f"Error cleaning data: {e}")

        try:
            data = get_human_readable_columns(
                "https://api.census.gov/data/2021/acs/acs5/profile/variables.json", data)
            # Do some manual column cleaning to avoid PostgreSQL errors

            data.rename(columns={
                "percent_house_heating_fuel_occupied_housing_units_bottled_tank_or_lp_gas": "percent_house_heating_fuel_occupied_housing_units_gas_tank",
                "percent_house_heating_fuel_occupied_housing_units_fuel_oil_kerosene_etc.": "percent_house_heating_fuel_occupied_housing_units_fuel_oil"
            }, inplace=True)

            logger.success("Data columns cleaned successfully")
        except Exception as e:
            logger.error(f"Error cleaning data columns: {e}")

        # Create DB Connection
        try:
            conn = init_connection()
            logger.success("Successfully connected to DB")
        except Exception as e:
            logger.error(f"Error connecting to DB: {e}")

        try:
            data = data[[
                "zcta",
                "est_gross_rent_occupied_units_paying_rent_median_dollars",
                "percent_housing_tenure_occupied_housing_units_renter_occupied",
                "percent_house_heating_fuel_occupied_housing_units_electricity",
                "percent_house_heating_fuel_occupied_housing_units_other_fuel",
                "percent_house_heating_fuel_occupied_housing_units_fuel_oil",
                "percent_house_heating_fuel_occupied_housing_units_no_fuel_used",
                "percent_house_heating_fuel_occupied_housing_units_coal_or_coke",
                "percent_house_heating_fuel_occupied_housing_units_solar_energy",
                "percent_house_heating_fuel_occupied_housing_units_wood",
                "percent_house_heating_fuel_occupied_housing_units_gas_tank",
                "est_value_owner_occupied_units_median_dollars"
            ]]
            logger.debug(f"Columns:\n{data.columns}")
            load_data(data, conn, schema_name="geospatial",
                      table_name="acs_census_2021_zcta")
        except Exception as e:
            logger.error(
                f"Error writing table acs_census_2021_zcta to DB: {e}")

        try:
            create_pkey(conn, table_name="acs_census_2021_zcta",
                        index_column="id")
        except Exception as e:
            logger.error(f"Error creating primary key: {e}")

        # Close DB Connection
        conn.close()


def run_acs_2021_cbsa_pipeline():
    # Check if table is already initialized
    if not is_table_initialized("acs_census_2021_cbsa"):
        try:
            r = extract_2021_acs_5_year_data(geography="cbsa")
            logger.success(
                "Successfully read 2021 ACS data from the US Census")
        except Exception as e:
            logger.error(
                f"Error reading 2021 ACS data from the US Census: {e}")

        try:
            data = clean_census_data(r, geography="cbsa")
            logger.success("Data cleaned successfully")
        except Exception as e:
            logger.error(f"Error cleaning data: {e}")

        try:
            data = get_human_readable_columns(
                "https://api.census.gov/data/2021/acs/acs5/profile/variables.json", data)

            # Do some manual column cleaning to avoid PostgreSQL errors
            data.rename(columns={
                "percent_house_heating_fuel_occupied_housing_units_bottled_tank_or_lp_gas": "percent_house_heating_fuel_occupied_housing_units_gas_tank",
                "percent_house_heating_fuel_occupied_housing_units_fuel_oil_kerosene_etc.": "percent_house_heating_fuel_occupied_housing_units_fuel_oil"
            }, inplace=True)

            logger.success("Data columns cleaned successfully")
        except Exception as e:
            logger.error(f"Error cleaning data columns: {e}")

        # Create DB Connection
        try:
            conn = init_connection()
            logger.success("Successfully connected to DB")
        except Exception as e:
            logger.error(f"Error connecting to DB: {e}")

        try:
            # Select only the columns we want
            data = data[[
                "cbsa",
                "est_gross_rent_occupied_units_paying_rent_median_dollars",
                "percent_housing_tenure_occupied_housing_units_renter_occupied",
                "percent_house_heating_fuel_occupied_housing_units_electricity",
                "percent_house_heating_fuel_occupied_housing_units_other_fuel",
                "percent_house_heating_fuel_occupied_housing_units_fuel_oil",
                "percent_house_heating_fuel_occupied_housing_units_no_fuel_used",
                "percent_house_heating_fuel_occupied_housing_units_coal_or_coke",
                "percent_house_heating_fuel_occupied_housing_units_solar_energy",
                "percent_house_heating_fuel_occupied_housing_units_wood",
                "percent_house_heating_fuel_occupied_housing_units_gas_tank",
                "est_value_owner_occupied_units_median_dollars"
            ]]
            load_data(data, conn, schema_name="geospatial",
                      table_name="acs_census_2021_cbsa")
        except Exception as e:
            logger.error(
                f"Error writing table acs_census_2021_cbsa to DB: {e}")

        try:
            create_pkey(conn, table_name="acs_census_2021_cbsa",
                        index_column="id")
        except Exception as e:
            logger.error(f"Error creating primary key on id column: {e}")

        # Close DB Connection
        conn.close()


def run_zcta_geography_boundary_pipeline():
    # Check if table is already initialized
    if not is_table_initialized("zcta_boundaries_2021"):
        # Read in ZCTA and CBSA Geo Data
        zcta_geo_data = extract_geography_boundaries(geography="zcta")

        # Create DB Connection
        try:
            conn = init_connection()
            logger.success("Successfully connected to DB")
        except Exception as e:
            logger.error(f"Error connecting to DB: {e}")

        try:
            # Load Data into DB
            load_boundary_data(zcta_geo_data, conn,
                               table_name="zcta_boundaries_2021")
        except Exception as e:
            logger.error(
                f"Error writing table zcta_boundaries_2021 to DB: {e}")

        try:
            create_pkey(conn, table_name="zcta_boundaries_2021",
                        index_column="id")
        except Exception as e:
            logger.error(f"Error creating primary key: {e}")


def run_cbsa_geography_boundary_pipeline():
    # Check if table is already initialized
    if not is_table_initialized("cbsa_boundaries_2021"):
        # Read in ZCTA and CBSA Geo Data
        cbsa_geo_data = extract_geography_boundaries(geography="cbsa")

        # Create DB Connection
        try:
            conn = init_connection()
            logger.success("Successfully connected to DB")
        except Exception as e:
            logger.error(f"Error connecting to DB: {e}")

        try:
            # Load Data into DB
            load_boundary_data(cbsa_geo_data, conn,
                               table_name="cbsa_boundaries_2021")
        except Exception as e:
            logger.error(
                f"Error writing table cbsa_boundaries_2021 to DB: {e}")

        try:
            create_pkey(conn, table_name="cbsa_boundaries_2021",
                        index_column="id")
        except Exception as e:
            logger.error(f"Error creating primary key: {e}")


def run_polygon_simplification_pipeline():
    for geography in ["ZCTA", "CBSA"]:
        table_name = f"{geography.lower()}_boundaries_2021_simplified"
        # Check if table is already initialized
        if not is_table_initialized(table_name):
            # Create DB Connection
            try:
                conn = init_connection()
                logger.success("Successfully connected to DB")
            except Exception as e:
                logger.error(f"Error connecting to DB: {e}")

            try:
                # Create new table with simplified polygons
                create_simplified_polygons(
                    conn, tolerance=0.001, geographic_granularity=geography)
                logger.success(
                    f"Successfully created table {table_name}")
            except Exception as e:
                logger.error(
                    f"Error creating table {table_name}: {e}")

            try:
                create_pkey(conn, table_name=table_name,
                            index_column="id")
            except Exception as e:
                logger.error(f"Error creating primary key: {e}")

            # Close DB Connection
            conn.close()


def run_zip_to_cbsa_pipeline():
    if not is_table_initialized("zip_to_cbsa"):

        zip_to_cbsa = extract_zip_to_cbsa()

        # Create DB Connection
        try:
            conn = init_connection()
            logger.success("Successfully connected to DB")
        except Exception as e:
            logger.error(f"Error connecting to DB: {e}")

        try:
            # Load Data into DB
            load_data(zip_to_cbsa, conn, schema_name="geospatial",
                      table_name="zip_to_cbsa")
        except Exception as e:
            logger.error(
                f"Error writing table zip_to_cbsa to DB: {e}")

        try:
            create_pkey(conn, table_name="zip_to_cbsa",
                        index_column="id")
        except Exception as e:
            logger.error(f"Error creating primary key: {e}")
