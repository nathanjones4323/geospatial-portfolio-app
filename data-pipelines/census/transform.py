import json
import re

import numpy as np
import pandas as pd
import requests


def clean_census_data(response: requests.Response, geography="zcta") -> pd.DataFrame:
    data = pd.DataFrame(json.loads(response.text))
    # Set the 1st row as the header
    data.columns = data.iloc[0]
    data = data[1:]
    # Remove the columns that are not needed
    data = data.loc[:, ~data.columns.str.endswith(("EA", "MA", "M"))]
    data.drop(columns=["NAME"], inplace=True)
    # Rename the geography column
    if geography == "zcta":
        name = "zip code tabulation area"
        data.rename(columns={"zip code tabulation area": "zcta"}, inplace=True)
    elif geography == "cbsa":
        name = "metropolitan statistical area/micropolitan statistical area"
        data.rename(columns={
                    "metropolitan statistical area/micropolitan statistical area": "cbsa"}, inplace=True)
    # Replace NULL encoded values with NaN
    data.replace(to_replace="-666666666", value=np.nan, inplace=True)
    return data


def standardize_column_names(column_name):
    """Standardize column names to be lowercase, snake case, and without special characters.

    Args:
        column_name (str): The column name to be standardized

    Returns:
        str: The standardized column name
    """

    # Special characters to remove
    column_name = column_name.replace("!!:", "_")
    column_name = column_name.replace("!!", "_")
    column_name = column_name.replace(" ", "_")
    column_name = column_name.replace("-", "_")
    column_name = column_name.replace("/", "_")
    column_name = column_name.replace(",", "_")
    column_name = column_name.replace("(", "")
    column_name = column_name.replace(")", "")
    column_name = column_name.replace("--", "")
    column_name = column_name.replace(":", "")
    column_name = column_name.replace('"', "")
    column_name = column_name.replace("'", "")

    # Lowercase and remove whitespace
    column_name = column_name.lower().strip()

    # Long strings that make sense to shorten
    column_name = column_name.replace("estimate", "est")
    column_name = column_name.replace("year", "yr")
    column_name = column_name.replace("households", "hh")
    column_name = column_name.replace("total", "")

    # Define for inflation adjusted dollars string pattern
    pattern = r"\((in_\d{4}_inflation_adjusted_dollars)\)"
    column_name = re.sub(pattern, "", column_name)
    # Replace 2+ underscores with 1 underscore
    column_name = re.sub(r"_{2,}", "_", column_name)

    return column_name


def truncate_column_names(df: pd.DataFrame) -> None:
    """Standardizes and truncates the column names of the given `df` by lowercasing and replacing special characters with `_`.

    Args:
        df (pd.DataFrame): Dataframe of Census data you want to truncate columns for
    """
    # Replace strings that match this pattern: "(in_2021_inflation-adjusted_dollars)"
    new_column_names = [standardize_column_names(
        col) for col in df.columns.values]

    df.columns = new_column_names
    return df


def get_human_readable_columns(variable_url: str, data: pd.DataFrame) -> pd.DataFrame:
    # Replace the column names with the human-readable names
    r = requests.get(variable_url)
    variable_names = pd.DataFrame(json.loads(r.text)["variables"]).T
    variable_names.drop(index=["in", "for", "ucgid"], inplace=True)
    variable_names.reset_index(inplace=True)
    variable_names.rename(columns={"index": "variable"}, inplace=True)
    data.rename(columns=variable_names.set_index(
        "variable")["label"].to_dict(), inplace=True)
    # Clean up the column names
    data = truncate_column_names(data)
    return data
