from helpers_db import *
import pandas as pd 
import pandavro as pdv 
import sys

def principal():
    # Verifiyng if we received the need arguments
    if len(sys.argv)>=2:
        table = sys.argv[1]
        conn = create_db_connection()
        # Verifiying if our table already exists
        # if not, we can-t create the backup
        if table_exists(table,conn):
            query = f""" SELECT * FROM dbo.{table}"""
            df = pd.read_sql(query,conn)
            # saving our dataframe to avro file
            # this path is inside the container
            # but it is mapped to a volume,
            # so the result are reflected on our
            # mounting point (the pc or nas that we specified)
            pdv.to_avro(f'/database/backups/files_backups/{table}.avro',df)
        else:
            print(f'La tabla {table} no existe en la base de datos')

    else:
        print('No se recibieron los parametros necesarios para generar el backup')
    
    return 0

if __name__ == '__main__':
    principal()