
# Test Globant API

This project contains an Flask REST API service inside a docker container.

And works with sql server database.

It has three endpoints:

'/newData': Enpoint to upload new data to the tables: jobs,departments or hired_employees

'/HiredByQuarter': Endpoint that downloads a report of the hired employees by quarter in 2021 by department and job


'/HiredByDepartment': of the hired employees that has a number of hired employees
greater than the mean of hired employees by department in 2021

Before to create the docker image, first check the README in 
test_globant/database/README.md
In case you want to work with historical data, if not just go to the next step

To build the image you need to be in the following path
test_globant/app/
and just run:

    docker build -t IMAGE_NAME .

where 

    IMAGE_NAME: Is the name that you want to give to this image.

To run our container: 

    docker run --network=NETWORK_NAME \
    --env-file ENVIRONMENT_FILE \
    -p 5000:5000 --name DOCKER_NAME \
    IMAGE_NAME \
    ./start_server.sh

Where:

    NETWORK_NAME: The network that you want to use, it could be 
    host to use your computer networ or 
    a docker network that you have been already created
    
    ENVIRONMENT_FILE:The file that contains the values 
    for the following variables that the server needs

        - SERVER=tcp:IP or server name, if you are using 
        a docker network and database in docker container, 
        use the name of the docker where your database is running
        e.g.:(tcp:MyContainer or tcp:172.172.0.6)
        - DATABASE=Name of the database to be used
        - USERNAME=User with acces to the database
        - PASSWORD=Password of the user with access to the database

    DOCKER_NAME: The name that you want to give to this container

    IMAGE_NAME: The name that you give to the image when you execute the
    docker build command

How to send requests:

The newData Endpoint, waits for json with the following format:
For departments table:

    '{
        'id':[13,14,15],
        'department':['Suply Chain','Maintenance','Staff']
    }'

For hired_employees table:

    'hired_employees= {
        'id':[4535,4572],
        'name':['Marcelo Gonzalez','Lidia Mendez'],
        'hired_date':['2021-07-27T16:02:08Z','2021-07-27T19:04:09Z'],
        'department_id':[1,1],
        'job_id':[2,2]
    }'

For jobs table:

    '{
        'id':[184,185,186],
        'job':['Recruiter','Manager','Analyst']
    }'

For the reports endpoints, you just need to paste in the browser of your choice
the ip address where the service is exposed and the endpoint that you want 
e.g 

    172.172.0.6/HiredByQuarter
    172.172.0.6/HiredByDepartment

And the files will be downloaded automatically