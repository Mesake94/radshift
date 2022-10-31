# custom docker image for freeradius

# Use the official image as a parent image.
FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y freeradius freeradius-utils freeradius-rest
RUN apt install freeradius-postgresql -y

# install python
RUN apt-get install -y python3-pip

# install python dependencies
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# copy .env file
COPY .env .
# copy python file to custom folder
COPY loader.py .

# Run the command to enable the configured modules
# RUN ln -s /etc/freeradius/3.0/mods-available/sql /etc/freeradius/3.0/mods-enabled/sql
# RUN ln -s /etc/freeradius/3.0/mods-available/rest /etc/freeradius/3.0/mods-enabled/rest
# RUN ln -s /etc/freeradius/3.0/mods-available/sqlcounter /etc/freeradius/3.0/mods-enabled/sqlcounter

# Configure the SQL module by copying the custom sql file to the container
# COPY sql /etc/freeradius/3.0/mods-available/sql
# # Configure sql counter module which is used to enforce session limits
# COPY sqlcounter /etc/freeradius/3.0/mods-available/sqlcounter
# # enable the sqlcounter module by copying the file to the enabled folder
# COPY radiusd.conf /etc/freeradius/3.0/radiusd.conf

# # Configure the rest module by copying the custom rest file to the container
# COPY rest /etc/freeradius/3.0/mods-available/rest

# # Configure the site configuration file by copying the custom site file to the container
# COPY default /etc/freeradius/3.0/sites-enabled/default

ADD /3.0 /etc/freeradius/3.0

# ports that the container will listen on
EXPOSE 1812/udp
EXPOSE 1813/udp
EXPOSE 18120/tcp


COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Run the command inside your image filesystem.
ENTRYPOINT ["sh", "entrypoint.sh"]
# CMD ["freeradius", "-X"]





