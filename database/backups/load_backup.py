from helpers_db import *
import pandas as pd 
import pandavro as pdv 
import sys
import os
from dateutil.parser import isoparse

def clean_hired_employees(df):
    """This Function parse to string a datetime column
    that comes from sql server backup, in order to
    give them a correct format and then parse to correct datetime format
    to be inserted to the desired table
    
    Parameters
    ----------
    df: pandas dataframe with the column to be parsed

    Returns
    -------
    df: pandas dataframe with the column
    to be parsed in datetime iso format
    """
    df['hired_date'] = df.hired_date.apply(lambda x:\
                                isoparse(x.strftime('%Y-%m-%dT%H:%M:%SZ')\
                                .replace('T',' ').replace('Z','.000')))
    
    return df

def principal():
    # verify that we have the needed arguments
    if len(sys.argv)>=2:
        table = sys.argv[1]
        conn = create_db_connection()
        # Read the backup file
        # this file is readed from an external
        # mounting point(pc or nas)
        # but it is mapped to this path
        # via docker volume
        file_path = f'/database/backups/files_backups/{table}.avro'
        # if our file exisit, we proceed to do the restore
        if os.path.exists(file_path):
            df = pdv.from_avro(file_path)

            if table=='hired_employees':
                df = clean_hired_employees(df)
        
            if table_exists(table,conn):
                print('***** La tabla existe en la DB, se sobreescribiran los datos existentes')
                insert_df_to_db(table,'dbo',df)
            else:
                insert_df_to_db(table,'dbo',df)
                print(f'La tabla {table} se ha creado desde un backup')
        else:
            print(f'No se encontro el backup de la tabla {table}')

    else:
        print('No se recibieron los parametros necesarios para reestablecer el backup')
    
    return 0

if __name__ == '__main__':
    principal()