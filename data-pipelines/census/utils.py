import pandas as pd
from load import init_connection
from loguru import logger
from sqlalchemy import exc, text


def create_postgis_extension(conn):
    """Creates the PostGIS extension in the database
    """
    try:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
        conn.commit()
        logger.success("Successfully created PostGIS extension")
    except Exception as e:
        logger.error(f"Error creating PostGIS extension: {e}")


def create_geospatial_schema(conn):
    """Creates the geospatial schema in the database
    """
    try:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS geospatial;"))
        conn.commit()
        logger.success("Successfully created geospatial schema")
    except Exception as e:
        logger.error(f"Error creating geospatial schema: {e}")


def is_table_initialized(table_name: str) -> bool:
    try:
        conn = init_connection()
        query = f"select id from {table_name} limit 1"
        df = pd.read_sql(query, conn)
        if df.empty:
            logger.info(
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
        logger.info(
            f"Table {table_name} does not exist in the DB. Running data pipeline...")
        conn.close()
        return False

    except Exception as e:
        logger.error(f"Could not connect to database: {e}")
        return False


def simplify_cbsa_polygons(conn, schema_name, tolerance=0.001):
    """Creates a simplified version of the CBSA polygons using the Douglas-Peucker algorithm
    """
    query = f"""
    create table if not exists {schema_name}.cbsa_boundaries_2021_simplified as (
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
        from {schema_name}.cbsa_boundaries_2021
        -- Exclude Puerto Rico
        where "NAMELSAD" not like '%%, PR%%'
    );
    """

    conn.execute(text(query))
    conn.commit()

    conn.execute(text(
        f"create index on {schema_name}.cbsa_boundaries_2021_simplified using gist(geometry);"))
    conn.commit()
    conn.close()


def simplify_zcta_polygons(conn, schema_name, tolerance=0.001):
    """Creates a simplified version of the ZCTA polygons using the Douglas-Peucker algorithm
    """
    query = f"""
        create table if not exists {schema_name}.zcta_boundaries_2021_simplified as (
            select
                id,
                "ZCTA5CE20",
                "GEOID20",
                "CLASSFP20",
                "MTFCC20",
                "FUNCSTAT20",
                "ALAND20",
                "AWATER20",
                "INTPTLAT20",
                "INTPTLON20",
                ST_SimplifyPreserveTopology(geometry, {tolerance}) AS geometry
            from {schema_name}.zcta_boundaries_2021
        );
        """

    conn.execute(text(query))
    conn.commit()

    conn.execute(text(
        f"create index on {schema_name}.zcta_boundaries_2021_simplified using gist(geometry);"))
    conn.commit()
    conn.close()


def create_simplified_polygons(conn, tolerance=0.001, geographic_granularity="CBSA"):
    """Creates a simplified version of the polygons to use for mapping
    """
    if geographic_granularity == "CBSA":
        simplify_cbsa_polygons(
            conn, schema_name="geospatial", tolerance=tolerance)

    elif geographic_granularity == "ZCTA":
        simplify_zcta_polygons(
            conn, schema_name="geospatial", tolerance=tolerance)
