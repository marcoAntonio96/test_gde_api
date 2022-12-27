from os import environ
from sqlalchemy import create_engine
import urllib
import logging

def create_db_connection():
    """This Function creates an sql engine,
    we use environmental values to connect
    to the desired database
    
    Parameters
    ----------
    Returns
    -------
    engine: SQL Engine Object with a connection
    to the specified database
    """
    server = environ['SERVER']
    database = environ['DATABASE']
    user = environ['USERNAME']
    password = environ['PASSWORD']

    params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                    f"SERVER={server};"
                                    f"DATABASE={database};"
                                    f"UID={user};"
                                    f"PWD={password}")

    engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
    return engine

def insert_df_to_db(table_name,schema,data):
    """This Function inserts pandas dataframe
    to one sql server database, if the table already exists
    this function append the data with the existing data
    
    Parameters
    ----------
    table_name: string that contains the name
    of the table where we will insert our data
    schema: schema name where our table exists
    data: pandas datafrem that contains
    the data we want to insert

    Returns
    -------
    """
    logging.info('Inserting data...')
    engine = create_db_connection()
    logging.info('Inserting {} values'.format(len(data)))
    data.to_sql(name=table_name,
                con=engine, 
                schema=schema,
                if_exists='append',
                index=False,
                chunksize=1_000
               )
    logging.info('Done')