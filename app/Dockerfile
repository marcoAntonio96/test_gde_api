FROM python:3.7.7
# adding custom MS repository
RUN apt-get install curl && apt-get clean
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

# install SQL Server drivers
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev mssql-tools && apt-get clean

# install requirements
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . app
WORKDIR app
RUN chmod +x start_server.sh

