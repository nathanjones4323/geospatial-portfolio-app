from queries.boundaries import load_cbsa_geom_data, load_zcta_geom
from queries.data import load_cbsa_acs_data, load_zcta_acs_data


def get_geographic_mapping(geographic_granularity):
    granularity_mapping = {
        "CBSA": {
            "geom_function": load_cbsa_geom_data,
            "data_function": load_cbsa_acs_data,
            "on_column": "cbsa",
        },
        "ZCTA": {
            "geom_function": load_zcta_geom,
            "data_function": load_zcta_acs_data,
            "on_column": "zcta",
        },
        # Add more mappings as needed
    }

    return granularity_mapping.get(geographic_granularity, None)
