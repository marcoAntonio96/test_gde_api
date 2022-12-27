from flask import Flask , send_file, jsonify
from flask_restful import Resource, Api, request
from pandas import DataFrame,read_sql
import json
from datetime import datetime
import logging
from helpers import verify_columns,generate_excel_to_download,\
                    validate_string,validate_int, validate_dateTime
from helpers_db import create_db_connection,insert_df_to_db
from constants import tables_validations

app = Flask(__name__)
api = Api(app)
logging.basicConfig(level=logging.INFO)

# Class that process the requests to insert new data
class NewData(Resource):
    def post(self):
        args = json.loads(request.json)
        logging.info(args)
        # For validation purposes, we only need the keys with non empy data
        to_process = {k:v for k,v in args.items() if v!=None}
        # Create our dataframe from the request parameters
        df_to_process = DataFrame.from_dict(to_process)
        # Check if the received parameters match with our tables
        validator,table_name,columns = verify_columns(list(df_to_process.columns))
        
        if validator==True:
            # variable to track the validation process
            status_transaction = True
            # Check if our transaction contains datetime columns type
            if tables_validations.get(table_name).get('datetime_columns',None)!=None:
                cols_to_check = tables_validations.get(table_name).get('datetime_columns')
                validator,df_to_process = validate_dateTime(df_to_process,cols_to_check)
                # if something goes grong, this flag help us to insert
                # the transaction in our log request table
                if validator==False:
                    status_transaction = validator

            # Check if our transaction contains int columns type
            if tables_validations.get(table_name).get('int_columns',None)!=None:
                cols_to_check = tables_validations.get(table_name).get('int_columns')
                validator = validate_int(df_to_process,cols_to_check)
                # if something goes grong, this flag help us to insert
                # the transaction in our log request table
                if validator==False:
                    status_transaction = validator

            # Check if our transaction contains datetime columns type
            if tables_validations.get(table_name).get('string_columns',None)!=None:
                cols_to_check = tables_validations.get(table_name).get('string_columns')
                validator = validate_string(df_to_process,cols_to_check)
                # if something goes grong, this flag help us to insert
                # the transaction in our log request table
                if validator==False:
                    status_transaction = validator

            # If all the validations are ok, inset the data in our desired table
            if status_transaction==True:
                insert_df_to_db(table_name,'dbo',df_to_process[columns])
                status=200
                message='Datos insertados correctamente'
            else:
                # If we have problems in the validation stage
                # insert the data to the transactions logs table
                df_to_insert = DataFrame.from_dict(
                    {
                        'request_time' : [datetime.now()], # we save the time of our transaction
                        'request_payload': [request.json] # we save the received parameters of the request
                    }
                )
                insert_df_to_db('failed_transactions','dbo',df_to_insert)
                status=500
                message='El tipo de datos recibidos no es el correcto, verifique los datos enviados'
        else:
            status=500
            message='Los parametros recibidos, no coinciden con las tablas en base de datos, no se pudo procesar su request.'
        
        data = {
            'status':status,
            'messsage':message
        }
        return jsonify(data)

# Class that process the request to generate the report
# of the hired employees by quarter in 2021 by department and job
class ReportHiredByQuarter(Resource):
    def get(self):
        conn = create_db_connection()
        query = """ 
        WITH data_report AS (
        SELECT 
        	he.id AS id_employee,
        	CONCAT('Q',DATEPART(QUARTER, he.hired_date)) AS quarter_,
        	d.department,
        	j.job
        FROM dbo.hired_employees he
        INNER JOIN dbo.departments d ON he.department_id = d.id
        INNER JOIN dbo.jobs j ON he.job_id = j.id
        WHERE YEAR(he.hired_date)=2021
        )
        SELECT *
        FROM data_report 
        PIVOT (
        count(id_employee)
        FOR quarter_ IN ([Q1],[Q2],[Q3],[Q4])
        ) AS p
        ORDER BY department,job
        """
        df = read_sql(query,conn)
        stream_output = generate_excel_to_download(df)
        suffix_name = datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = f"ReportHiredByQuarter_{suffix_name}.xlsx"
        return send_file(stream_output, download_name=file_name,\
                        as_attachment=True)

# Class that process the request to generate the report
# of the hired employees that has a number of hired employees
# greater than the mean of hired employees by department in 2021
class ReportHiredByDepartment(Resource):
    def get(self):
        conn = create_db_connection()
        query = f""" 
        WITH data_report AS (
        SELECT 
        	d.id,
        	d.department,
        	COUNT(he.id) AS hired
        FROM
         dbo.hired_employees he 
         INNER JOIN dbo.departments d 
         ON he.department_id  = d.id 
         WHERE YEAR(he.hired_date)=2021
         GROUP BY d.id,d.department 
         )
         SELECT id,department, hired
         FROM data_report WHERE hired>(SELECT AVG(hired) FROM data_report)
         ORDER BY hired DESC 
        """
        df = read_sql(query,conn)
        stream_output = generate_excel_to_download(df)
        suffix_name = datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = f"ReportHiredByDepartment{suffix_name}.xlsx"
        return send_file(stream_output, download_name=file_name,\
                        as_attachment=True)

# adding our endpoints
api.add_resource(NewData, '/newData') 
api.add_resource(ReportHiredByQuarter, '/HiredByQuarter') 
api.add_resource(ReportHiredByDepartment, '/HiredByDepartment')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)  # run Flask app
    app.logger.setLevel(logging.INFO)

