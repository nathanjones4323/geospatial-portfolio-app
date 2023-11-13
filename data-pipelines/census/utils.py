import re

import pandas as pd
from load import init_connection
from loguru import logger
from psycopg2 import errors


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

    except errors.UndefinedTable as e:
        logger.warning(
            f"Data for {table_name} not found in the DB, running data pipeline...")
        conn.close()
        return False

    except Exception as e:
        logger.error(f"Could not connect to database: {e}")
        return False
