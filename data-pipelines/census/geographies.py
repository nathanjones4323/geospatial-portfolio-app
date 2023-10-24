# This module can be used to download and process shapefiles from the US Census Bureau.
import os

import geopandas as gpd
from loguru import logger
from sqlalchemy import create_engine

logger.debug(os.environ['POSTGRES_USER'])
logger.debug(os.environ['POSTGRES_PASSWORD'])
logger.debug(os.environ['POSTGRES_HOST'])
logger.debug(os.environ['POSTGRES_PORT'])
logger.debug(os.environ['POSTGRES_DB'])

# Read Shapefile
try:
    url = "https://www2.census.gov/geo/tiger/TIGER2020/CBSA/tl_2020_us_cbsa.zip"
    geo_data = gpd.read_file(url)
    logger.success("Successfully read 2020 CBSA shapefile from the US Census")
except Exception as e:
    logger.error(f"Error reading 2020 CBSA shapefile from the US Census: {e}")

# Create DB Connection
try:
    db_user = os.environ['POSTGRES_USER']
    db_pass = os.environ['POSTGRES_PASSWORD']
    db_host = os.environ['POSTGRES_HOST']
    db_port = os.environ['POSTGRES_PORT']
    db_name = os.environ['POSTGRES_DB']

    conn_string = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
    engine = create_engine(url=conn_string)
    conn = engine.connect()
    logger.success("Successfully connected to DB")
except Exception as e:
    logger.error(f"Error connecting to DB: {e}")

try:
    # Dump Data into New Database Table
    geo_data.to_postgis("cbsa_census_2020", conn,
                        if_exists='fail', index=False)

    # Create Primary Key from Index column
    conn.execute('ALTER TABLE cbsa_census_2020 ADD PRIMARY KEY (id);')
    logger.success("Successfully wrote 2020 CBSA shapefile to DB")
except Exception as e:
    logger.error(f"Error writing 2020 CBSA shapefile to DB: {e}")

# Close DB Connection
conn.close()
