import os

from dotenv import load_dotenv
from extract import extract_acs_data
from load import create_acs_pkey, init_connection, load_acs_data
from loguru import logger
from transform import clean_census_zcta_data, get_human_readable_columns

try:
    r = extract_acs_data()
    logger.success("Successfully read 2021 ACS data from the US Census")
except Exception as e:
    logger.error(f"Error reading 2021 ACS data from the US Census: {e}")


try:
    data = clean_census_zcta_data(r)
    logger.success("Data cleaned successfully")
except Exception as e:
    logger.error(f"Error cleaning data: {e}")


try:
    data = get_human_readable_columns(
        "https://api.census.gov/data/2021/acs/acs5/profile/variables.json", data)
    logger.success("Data columns cleaned successfully")
except Exception as e:
    logger.error(f"Error cleaning data columns: {e}")

try:
    # Load Environment Variables
    dotenv_path = os.path.dirname(__file__)
    load_dotenv(dotenv_path)
    logger.success("Loaded .env file")
except:
    logger.error("Could not load .env file")

# Create DB Connection
try:
    conn = init_connection()
    logger.success("Successfully connected to DB")
except Exception as e:
    logger.error(f"Error connecting to DB: {e}")

try:
    data = data[["zcta", "est_gross_rent_occupied_units_paying_rent_median_dollars"]]
    load_acs_data(data, conn)
    logger.success("Successfully wrote 2021 ACS data to DB")
    create_acs_pkey(conn)
    logger.success("Created primary key on id column")
except Exception as e:
    logger.error(f"Error writing 2021 ACS data to DB: {e}")

# Close DB Connection
conn.close()
