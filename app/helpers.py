from constants import *
from dateutil.parser import isoparse
from io import BytesIO
import pandas as pd 

def verify_columns(df_cols):
    """This function verifies if the columns in the
    received list match with the columns specified
    in the constants file, in order to check
    that we have the needed columns for the process

    Parameters
    ----------
    df_cols:List of the existing columns 
    in one pandas dataframe

    Returns
    -------
    validator: Boolean value, that indicates if the
    columns amtch with one of the columns list in constants.py
    table_name: string that contains the table name thath match
    with the received columns
    columns: list with the columns that we need to insert
    in the database for each table
    """
    validator = False
    table_name = None
    columns = None

    if len(list(set(cols_departments) - set(df_cols ) )) == 0 :
        validator = True 
        table_name = 'departments'
        columns = cols_departments
    elif len(list(set(cols_hired_employees) - set(df_cols) )) == 0:
        validator = True
        table_name = 'hired_employees'
        columns = cols_hired_employees
    elif len(list(set(cols_jobs) - set(df_cols) )) == 0:
        validator = True
        table_name = 'jobs'
        columns = cols_jobs
    else:
        validator = False

    return validator,table_name,columns

def validate_string(df,cols_to_check):
    """This function validates if
    a column in pandas dataframe is string type

    Parameters
    ----------
    df: Pandas dataframe to be validated
    cols_to_check: list of columns
    that we want to validate in our dataframe

    Returns
    -------
    validator:boolean value that indicates if all 
    of our received columns in cols_to_check 
    are string type

    """
    validator = True
    for col in cols_to_check:
        df['is_string'] = True
        df['is_string'] = df[col].apply(lambda x: True if isinstance(x,str) else False)
        if len(df.loc[df.is_string==False])>0:
            validator = False
    return validator

def validate_int(df,cols_to_check):
    """This function validates if
    a column in pandas dataframe is int type

    Parameters
    ----------
    df: Pandas dataframe to be validated
    cols_to_check: list of columns
    that we want to validate in our dataframe

    Returns
    -------
    validator:boolean value that indicates if all 
    of our received columns in cols_to_check 
    are int type

    """
    validator = True
    for col in cols_to_check:
        if not df[col].dtype=='int64':
            validator = False
    return validator

def parse_str_dateTime(iso_format_str):
    """This function parse a string
    to datetime iso type when possible

    Parameters
    ----------
    iso_format_str: string with the value to be parsed
    we want a format like '2022-12-26T16:09:45Z'
    in order to parse to a correct data type

    Returns
    -------
    new_value: datetime object parsed to iso format
    when it is posible to convert iso_format_str
    iso_format_str: The string that we received when it
    is not possible to parse it
    True/False:boolean value that indicates if our 
    received string has the format that we need
    """
    try:
        print(iso_format_str)
        new_value = isoparse(iso_format_str.replace('T',' ').replace('Z',''))
        return new_value,True
    except Exception as ex:
        return iso_format_str,False

def validate_dateTime(df,cols_to_check):
    """This function validates if
    a column in pandas dataframe is datetime iso type

    Parameters
    ----------
    df: Pandas dataframe to be validated
    cols_to_check: list of columns
    that we want to validate in our dataframe

    Returns
    -------
    validator:boolean value that indicates if all 
    of our received columns in cols_to_check 
    are datetime iso type
    df:pandas dataframe with cols_to_check
    parsed to a datatime iso type that 
    sql server can manage
    """
    validator = True
    for col in cols_to_check:
        df['is_datetime'] = True
        df[[col,'is_datetime']] = df.apply(lambda x: parse_str_dateTime(x[col]),axis=1,result_type="expand")
        if len(df.loc[df.is_datetime==False])>0:
            validator = False
    return validator,df

def generate_excel_to_download(df):
    """This function generates a stream output
    to be sended in our appi as file to be downloaded

    Parameters
    ----------
    df: Pandas dataframe with the data
    to be downloaded by the client

    Returns
    -------
    output: stream object with the excel file 
    ready to be downloaded

    """

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')

    df.to_excel(writer, index = False, sheet_name = "Report")
    workbook = writer.book
    worksheet = writer.sheets["Report"]

    writer.close()

    output.seek(0)
    return output