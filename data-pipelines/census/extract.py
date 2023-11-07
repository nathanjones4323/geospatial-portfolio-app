import json
import os

import pandas as pd
import requests
from loguru import logger


def extract_acs_data():
    url = "https://api.census.gov/data/2021/acs/acs5/profile?get=group(DP04)&for=zip%20code%20tabulation%20area:*"
    r = requests.get(url)
    return r
