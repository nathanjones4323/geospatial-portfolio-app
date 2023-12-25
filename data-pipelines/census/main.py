import os

from dotenv import load_dotenv
from loguru import logger
from pipelines import (run_acs_2021_cbsa_pipeline, run_acs_2021_zcta_pipeline,
                       run_cbsa_geography_boundary_pipeline,
                       run_db_init_pipeline,
                       run_polygon_simplification_pipeline,
                       run_zcta_geography_boundary_pipeline,
                       run_zip_to_cbsa_pipeline)

try:
    # Load Environment Variables
    dotenv_path = os.path.dirname(__file__)
    load_dotenv(dotenv_path)
    logger.success("Loaded .env file")
except:
    logger.error("Could not load .env file")

run_db_init_pipeline()

run_acs_2021_zcta_pipeline()

run_acs_2021_cbsa_pipeline()

run_zcta_geography_boundary_pipeline()

run_cbsa_geography_boundary_pipeline()

run_polygon_simplification_pipeline()

run_zip_to_cbsa_pipeline()
