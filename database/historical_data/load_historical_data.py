import pandas as pd 
from helpers_db import *
from dateutil.parser import isoparse

# constants with the table names
# the file name, and the desired columns to be inserted
tables = {
    'hired_employees':{
        'file_path':'hired_employees.xlsx',
        'columns': ['id','name','hired_date','department_id','job_id']
    },
    'departments':{
        'file_path':'departments.xlsx',
        'columns': ['id','department']
    },
    'jobs':{
        'file_path':'jobs.xlsx',
        'columns': ['id','job']
    }
}


def principal():
    for table in tables.keys():
        conn = create_db_connection()
        # If the table already exists, we don-t need to upload historical data
        if table_exists(table,conn):
            print(f'La tabla {table} ya existe')
        else:
            # read data from our historical files
            df = pd.read_excel(tables.get(table)['file_path'],engine='openpyxl',\
                names=tables.get(table)['columns'])
            # In order to avoid null values,
            # we drop the rows with null values
            df.dropna(inplace=True)
            df.reset_index(drop=True,inplace=True)
            # If our data has datetime column
            if table=='hired_employees':
                df['hired_date'] = df.hired_date.apply(lambda x:\
                                isoparse(x.replace('T',' ').replace('Z','')))
            
            insert_df_to_db(table,'dbo',df)
            print(f'Data historica de {table} insertada')

    return 0

if __name__ == '__main__':
    principal()