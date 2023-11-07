import os

from sqlalchemy import create_engine, text


def init_connection():
    db_user = os.getenv('POSTGRES_USER')
    db_pass = os.getenv('POSTGRES_PASSWORD')
    db_host = os.getenv('POSTGRES_HOST')
    db_port = os.getenv('POSTGRES_PORT')
    db_name = os.getenv('POSTGRES_DB')

    conn_string = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
    engine = create_engine(url=conn_string)
    conn = engine.connect()
    return conn


def load_acs_data(data, conn):
    # Dump Data into New Database Table
    data.to_sql("acs_census_2021", conn,
                if_exists='fail', index=True)


def create_acs_pkey(conn):
    # Create Primary Key from Index column
    conn.execute(
        text('ALTER TABLE acs_census_2021 ADD PRIMARY KEY (id);'))
