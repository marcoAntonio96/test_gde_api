# Historical and Backup data project

This projects use SQL Server database and python to load historical data from xlsx files
and create avro backups of this tables or restore them from a specified backup.

First of all, if you don't have an sql server instance running, you can
create one using a docker container, to do that you need:

Create a network and explicity enable ICC

    docker network create -o com.docker.network.bridge.enable_icc=true [network]

Where network is the name that you want to give to your network.

Then, download the image:

    sudo docker pull mcr.microsoft.com/mssql/server:2022-latest

Run the container:

    sudo docker run --network=NETWORK_NAME -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=YOURPASSWORD" \
    -p 1433:1433 --name DOCKER_NAME --hostname HOSTNAME \
    -d \
    mcr.microsoft.com/mssql/server:2022-latest

Where:

    NETWORK_NAME: The network name that you give to the network that you create
    
    YOURPASSWORD: Your sql password and should follow the SQL Server default password policy, 
    otherwise the container can't set up SQL Server and will stop working. 
    By default, the password must be at least eight characters long and contain 
    characters from three of the following four sets: uppercase letters, lowercase letters, 
    base-10 digits, and symbols.
    
    DOCKERNAME: The name that you want to give to the container
    
    HOSTNAME: The name you want to give to the container

Now, you have a sql server instance running in a docker container.

To know what is your database host, execute:

    docker inspect YOUR_NETWORK_NAME

And look for the container name that you give to the container 
in the previous docker run command
and then you are going to see the ip address of your container.

### Building the image
To build the image that load the data or create/restore the backups
you need to be in the path: 

    test_globant/database

and run the following command:

    docker build -t IMAGE_NAME .

Where:

    IMAGE_NAME: Is the name that you want to give to the docker image

You need an enviroment file to run the container, the env file
has to contain the following variables:

        - SERVER= tcp:IP or server name, if you are using 
        a docker network and database in docker container, 
        use the name of the docker where your database is running
        e.g.:(tcp:MyContainer or tcp:172.172.0.6)
        - DATABASE= Name of the database to be used
        - USERNAME= User with acces to the database
        - PASSWORD= Password of the user with access to the database

## Running the container 

To load historical data run:

    docker run --network=NETWORK_NAME \
    --env-file ENVIRONMENT_FILE_PATH \
    DOCKER_NAME  \
    ./load_data.sh

Where 

    - NETWORK_NAME: The network name that you create at the beggining
    or host if you have an sql server instance running locally or in the cloud

    - ENVIRONMENT_FILE_PATH: The file path where your environment file lives in,
    this file must contain the variables listed above.

    - DOCKER_NAME: The name that you want to give to the docker

The files with historical data are inside the ccontainer,
so you just need to wait until the script ends

To create a backup from existing tables run: 

    docker run --network=NETWORK_NAME \
    --env-file ENVIRONMENT_FILE_PATH \
    -v VOLUME_FILE_PATH \
    DOCKER NAME  \
    ./create_backup.sh TABLE_NAME_1 TABLE_NAME_2 TABLE_NAME_N

Where

    - NETWORK_NAME: The network name that you create at the beggining
    or host if you have an sql server instance running locally or in the cloud.

    - ENVIRONMENT_FILE_PATH: The file path where your environment file lives in,
    this file must contain the variables listed above.

    - VOLUME_FILE_PATH: This path is a directory on your computer
    that is mounted on the container, in this path the backups will be saved.

    - DOCKER_NAME: The name that you want to give to the docker.

    - TABLE_NAME_N: The table names to which the backups will be created

To restore a backup from existing tables run: 

    docker run --network=NETWORK_NAME \
    --env-file ENVIRONMENT_FILE_PATH \
    -v VOLUME_FILE_PATH \
    DOCKER NAME  \
    ./create_backup.sh TABLE_NAME_1 TABLE_NAME_2 TABLE_NAME_N

Where

    - NETWORK_NAME: The network name that you create at the beggining
    or host if you have an sql server instance running locally or in the cloud.

    - ENVIRONMENT_FILE_PATH: The file path where your environment file lives in,
    this file must contain the variables listed above.

    - VOLUME_FILE_PATH: This path is a directory on your computer
    that is mounted on the container, this path must contains
    existing backups files.

    - DOCKER_NAME: The name that you want to give to the docker.

    - TABLE_NAME_N: The table names to be restored
