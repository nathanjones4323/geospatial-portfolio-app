import json
import os

import geopandas as gpd
import pandas as pd
import requests
from loguru import logger
from sqlalchemy import create_engine


def extract_2021_acs_5_year_data(geography="zcta") -> requests.Response:
    if geography == "zcta":
        geo_url_encoded = "zip%20code%20tabulation%20area:*"
    elif geography == "cbsa":
        geo_url_encoded = "metropolitan%20statistical%20area/micropolitan%20statistical%20area:*"
    url = f"https://api.census.gov/data/2021/acs/acs5/profile?get=group(DP04)&for={geo_url_encoded}"
    r = requests.get(url)
    return r


def extract_geography_boundaries(geography="zcta") -> gpd.GeoDataFrame:
    if geography == "zcta":
        url = "https://www2.census.gov/geo/tiger/TIGER2021/ZCTA520/tl_2021_us_zcta520.zip"
    elif geography == "cbsa":
        url = "https://www2.census.gov/geo/tiger/TIGER2021/CBSA/tl_2021_us_cbsa.zip"
    geo_data = gpd.read_file(url)
    return geo_data


def extract_zip_to_cbsa() -> pd.DataFrame:
    # Read in cross walk data
    url = "https://www.huduser.gov/hudapi/public/usps?type=8&query=All"
    token = os.environ["US_CENSUS_CROSSWALK_API_KEY"]
    headers = {"Authorization": "Bearer {0}".format(token)}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        logger.error("Failure, see status code: {0}".format(
            response.status_code))
    else:
        zip_to_cbsa = pd.DataFrame(response.json()["data"]["results"])

    zip_to_cbsa.rename(columns={"geoid": "zip_code",
                                "cbsa": "cbsa_code"}, inplace=True)

    return zip_to_cbsa
