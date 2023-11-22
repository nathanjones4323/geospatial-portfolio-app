import os

import pandas as pd
from loguru import logger
from sqlalchemy import create_engine, text
from sqlalchemy.engine.base import Connection


def init_connection() -> Connection:
    db_user = os.getenv('POSTGRES_USER')
    db_pass = os.getenv('POSTGRES_PASSWORD')
    db_host = os.getenv('POSTGRES_HOST')
    db_port = os.getenv('POSTGRES_PORT')
    db_name = os.getenv('POSTGRES_DB')

    conn_string = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
    engine = create_engine(url=conn_string)
    conn = engine.connect()
    return conn


def load_data(data, conn, table_name):
    # Dump Data into New Database Table
    data.to_sql(table_name, conn,
                if_exists='fail', index=True, index_label='id')
    logger.success(f"Successfully wrote table {table_name} to DB")


def load_boundary_data(data, conn, table_name):
    data.to_postgis(table_name, conn,
                    if_exists='fail', index=True, index_label='id', chunksize=100)
    logger.success(f"Successfully wrote table {table_name} to DB")


def create_pkey(conn, table_name, index_column):
    try:
        conn = init_connection()
        logger.success("Successfully connected to DB")
    except Exception as e:
        logger.error(f"Error connecting to DB: {e}")
    # Create Primary Key from Index column
    conn.execute(
        text(f'ALTER TABLE {table_name} ADD PRIMARY KEY ({index_column});'))
    conn.commit()
    logger.success(f"Created primary key on {index_column} column")
