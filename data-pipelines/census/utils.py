import pandas as pd
from load import init_connection
from loguru import logger
from sqlalchemy import exc, text


def is_table_initialized(table_name: str) -> bool:
    try:
        conn = init_connection()
        query = f"select id from {table_name} limit 1"
        df = pd.read_sql(query, conn)
        if df.empty:
            logger.warning(
                f"Data for {table_name} not found in the DB, running data pipeline...")
            conn.close()
            return False
        else:
            logger.info(
                f"Data for {table_name} already exists in the DB. Skipping data pipeline.")
            conn.close()
            return True

    except exc.ProgrammingError as e:
        # Handle the case where the table does not exist
        logger.warning(
            f"Table {table_name} does not exist in the DB. Running data pipeline...")
        conn.close()
        return False

    except Exception as e:
        logger.error(f"Could not connect to database: {e}")
        return False


def create_simplified_polygons(conn, tolerance=0.001):
    """Creates a simplified version of the polygons to use for mapping
    """
    query = f"""
    create table if not exists cbsa_boundaries_2021_simplified as (
        select
            id,
            "CSAFP",
            "CBSAFP",
            "GEOID",
            "NAME",
            "NAMELSAD",
            "LSAD",
            "MEMI",
            "MTFCC",
            "ALAND",
            "AWATER",
            "INTPTLAT",
            "INTPTLON",
            ST_SimplifyPreserveTopology(geometry, {tolerance}) AS geometry
        from cbsa_boundaries_2021
    );
    """
    # Log the executed query
    logger.debug(query)

    conn.execute(text(query))
    conn.commit()

    conn.execute(text(
        "create index on cbsa_boundaries_2021_simplified using gist(geometry);"))
    conn.commit()
    conn.close()
