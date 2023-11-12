import os

from dotenv import load_dotenv
from extract import extract_2021_acs_5_year_data, extract_geography_boundaries
from load import create_acs_pkey, init_connection, load_data
from loguru import logger
from transform import clean_census_data, get_human_readable_columns

from utils import is_table_initialized


def run_acs_2021_zcta_pipeline():
    # Check if table is already initialized
    if is_table_initialized("acs_census_2021_zcta"):
        exit()

    try:
        r = extract_2021_acs_5_year_data(geography="zcta")
        logger.success("Successfully read 2021 ACS data from the US Census")
    except Exception as e:
        logger.error(f"Error reading 2021 ACS data from the US Census: {e}")

    try:
        data = clean_census_data(r, geography="zcta")
        logger.success("Data cleaned successfully")
    except Exception as e:
        logger.error(f"Error cleaning data: {e}")

    try:
        data = get_human_readable_columns(
            "https://api.census.gov/data/2021/acs/acs5/profile/variables.json", data)
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
            "zcta", "est_gross_rent_occupied_units_paying_rent_median_dollars"]]
        load_data(data, conn, table_name="acs_census_2021_zcta")
    except Exception as e:
        logger.error(f"Error writing table acs_census_2021_zcta to DB: {e}")

    try:
        create_acs_pkey(conn)
    except Exception as e:
        logger.error(f"Error creating primary key on id column: {e}")

    # Close DB Connection
    conn.close()


def run_acs_2021_cbsa_pipeline():
    # Check if table is already initialized
    if is_table_initialized("acs_census_2021_cbsa"):
        exit()

    try:
        r = extract_2021_acs_5_year_data(geography="cbsa")
        logger.success("Successfully read 2021 ACS data from the US Census")
    except Exception as e:
        logger.error(f"Error reading 2021 ACS data from the US Census: {e}")

    try:
        data = clean_census_data(r, geography="cbsa")
        logger.success("Data cleaned successfully")
    except Exception as e:
        logger.error(f"Error cleaning data: {e}")

    try:
        data = get_human_readable_columns(
            "https://api.census.gov/data/2021/acs/acs5/profile/variables.json", data)
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
            "cbsa", "est_gross_rent_occupied_units_paying_rent_median_dollars"]]
        load_data(data, conn, table_name="acs_census_2021_cbsa")
    except Exception as e:
        logger.error(f"Error writing table acs_census_2021_cbsa to DB: {e}")

    try:
        create_acs_pkey(conn)
    except Exception as e:
        logger.error(f"Error creating primary key on id column: {e}")

    # Close DB Connection
    conn.close()


def run_zcta_geography_boundary_pipeline():
    # Check if table is already initialized
    if is_table_initialized("2021_zcta_boundaries"):
        exit()

    # Read in ZCTA and CBSA Geo Data
    zcta_geo_data = extract_geography_boundaries(geography="zcta")

    # Create DB Connection
    try:
        conn = init_connection()
        logger.success("Successfully connected to DB")
    except Exception as e:
        logger.error(f"Error connecting to DB: {e}")

    # Load Data into DB
    load_data(zcta_geo_data, conn, table_name="2021_zcta_boundaries")


def run_cbsa_geography_boundary_pipeline():
    # Check if table is already initialized
    if is_table_initialized("2021_cbsa_boundaries"):
        exit()

    # Read in ZCTA and CBSA Geo Data
    cbsa_geo_data = extract_geography_boundaries(geography="cbsa")

    # Create DB Connection
    try:
        conn = init_connection()
        logger.success("Successfully connected to DB")
    except Exception as e:
        logger.error(f"Error connecting to DB: {e}")

    # Load Data into DB
    load_data(cbsa_geo_data, conn, table_name="2021_cbsa_boundaries")