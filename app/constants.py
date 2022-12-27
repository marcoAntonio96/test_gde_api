# Valid column names per file/table
cols_hired_employees = ['id','name','hired_date','department_id','job_id']
cols_departments = ['id','department']
cols_jobs = ['id','job']

# Columns to be validated in each table
tables_validations = {
    'hired_employees':{
        'int_columns':['id','department_id','job_id'],
        'string_columns':['name'],
        'datetime_columns':['hired_date']
    },
    'departments':{
        'int_columns':['id'],
        'string_columns':['department'],
    },
    'jobs':{
        'int_columns':['id'],
        'string_columns':['job'],
    },
}