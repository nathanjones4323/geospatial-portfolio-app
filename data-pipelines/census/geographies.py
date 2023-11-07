# This module can be used to download and process shapefiles from the US Census Bureau.
import os

import geopandas as gpd
from dotenv import load_dotenv
from loguru import logger
from sqlalchemy import create_engine, text

# Load Environment Variables
dotenv_path = os.path.dirname(__file__)
try:
    load_dotenv(dotenv_path)
    logger.success("Loaded .env file")
except:
    logger.error("Could not load .env file")

# Read Shapefile
try:
    url = "https://www2.census.gov/geo/tiger/TIGER2021/CBSA/tl_2021_us_cbsa.zip"
    geo_data = gpd.read_file(url)
    logger.success("Successfully read 2021 CBSA shapefile from the US Census")
except Exception as e:
    logger.error(f"Error reading 2021 CBSA shapefile from the US Census: {e}")

# Clean Data
try:
    geo_data.columns = [x.strip().lower() for x in geo_data.columns]
    geo_data.rename(columns={'geoid': 'geo_id'}, inplace=True)
except Exception as e:
    logger.error(f"Error cleaning dataframe: {e}")


# Create DB Connection
try:
    db_user = os.getenv('POSTGRES_USER')
    db_pass = os.getenv('POSTGRES_PASSWORD')
    db_host = os.getenv('POSTGRES_HOST')
    db_port = os.getenv('POSTGRES_PORT')
    db_name = os.getenv('POSTGRES_DB')

    conn_string = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
    engine = create_engine(url=conn_string)
    conn = engine.connect()
    logger.success("Successfully connected to DB")
except Exception as e:
    logger.error(f"Error connecting to DB: {e}")

try:
    # Dump Data into New Database Table
    geo_data.to_postgis("cbsa_census_2021", conn,
                        if_exists='fail', index=True)
    logger.success("Successfully wrote 2021 CBSA shapefile to DB")

    # Create Primary Key from Index column
    conn.execute(
        text('ALTER TABLE cbsa_census_2021 ADD PRIMARY KEY (id);'))
    logger.success("Created primary key on id column")
except Exception as e:
    logger.error(f"Error writing 2021 CBSA shapefile to DB: {e}")

# Close DB Connection
conn.close()
