import re

import pandas as pd


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
    column_name = column_name.replace("--", "")
    column_name = column_name.replace("-", "_")
    column_name = column_name.replace("/", "_")
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
