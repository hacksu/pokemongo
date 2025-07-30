# Will perform an automatic docker pull
# to link the image that will be used throughout
# this Dockerfile

# argument that creates a env variable the docker uses
# example: docker build --build-arg PASSWORD=supersecurepassword123 -t image_name .
ARG PASSWORD
ENV PASSWORD=${PASSWORD}

FROM mongo:latest

# Sets the working directory for any command
# that follows it in the Dockerfile
WORKDIR /

# RUN executes system commands during the building process
# (useful for installing system packages)
RUN apt-get update && apt-get install -y sudo
RUN apt install -y systemctl python3 python3-venv

# create python app location in the docker
CMD [ "python3", "-m", "venv", "app" ]

# COPY will copy specified localhost files onto the docker
COPY ./src /app/src
COPY ./pokemon_data /app/data

COPY init.sh /root/init.sh
RUN chmod +x /root/init.sh # bash files need to be set as executable

# Commands that will be executed after the build process
CMD [ "/bin/bash", "/root/init.sh" ]
